import streamlit as st
import requests
from pathlib import Path
from datetime import datetime

API_URL = "https://api.siliconflow.cn/v1/chat/completions"
API_KEY = "sk-fzzfbikzcvltveiogdxixyftsokesldzvmeabbqyvhsaanfm"

@st.cache_data
def load_school_data():
    content = ""
    for md_file in Path("data").glob("*.md"):
        with open(md_file, "r", encoding="utf-8") as f:
            content += f"\n\n=== {md_file.name} ===\n" + f.read()
    return content

def get_system_prompt(identity, school_data):
    hard_rules = """【防幻觉硬规则】必须严格执行！
1. 只能根据【学校资料】回答，资料里没有的问题，直接回复"这个我没收录，建议拨打 0371-61911000 总值班室问一下"
2. 严禁编造电话号码、地址、办公时间、学费金额、人名，必须从【学校资料】中查找
3. 涉及金钱/转账，无条件在回答末尾添加："先联系辅导员核实，任何要求转账的都是诈骗"
4. 涉及心理危机（自杀、不想活、活不下去等），立即回复："12320-5 心理援助 + 学校心理咨询中心（0371-61912356，学生活动中心3楼）+ 告诉辅导员"
5. 被问"查我的成绩/课表/卡余额"等需要接入学校系统的问题，礼貌拒绝："抱歉，我无法接入学校系统查询个人信息，请通过教务系统或一卡通自助机查询"
6. 回答末尾必须标注 [来源:文件名]"""

    alias_dict = """【别名词典】
- "学校""航院""ZUA""郑航" = 郑州航空工业管理学院
- "新校区""龙湖""新校" = 龙子湖校区
- "卡""饭卡""校卡" = 校园一卡通
- "保安""门卫""校警" = 保卫处"""

    roles = {
        "新生": "你是热心的大二学长，语气详细、口语化、多给鼓励，把流程拆成具体步骤",
        "在校生": "你是办事老司机学长，语气简洁，回答重点：①地点 ②电话 ③所需材料 ④办结时间",
        "教师": "你是专业助手，语气专业礼貌，回答重点：①政策依据 ②办事窗口 ③联系人"
    }

    return f"你是'小航'，郑州航院校园信息查询AI助手。当前用户身份：{identity}。{roles[identity]}\n{hard_rules}\n{alias_dict}\n【学校资料】\n{school_data}"

def call_api(system_prompt, question):
    try:
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        data = {"model": "Qwen/Qwen2.5-7B-Instruct", "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": question}]}
        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        return f"请求失败 [{response.status_code}]"
    except Exception as e:
        return f"网络错误: {str(e)}"

KNOWN_TOPICS = [
    "报到", "学费", "缴费", "宿舍", "校园卡", "军训", "图书馆",
    "在读证明", "学生证", "补办", "请假", "成绩单", "报修",
    "差旅", "报销", "课表", "教材", "会议室", "心理", "防骗",
    "保卫处", "教务处", "学生处", "财务处", "校医院", "网络",
    "入学", "证明", "打印", "申请", "奖学金", "就业", "后勤",
    "户口", "迁户口", "落户", "调宿舍", "换宿舍", "学籍", "户籍"
]

def post_check(question, answer):
    if any(kw in question for kw in ["不想活", "自杀", "活不下去", "想死", "抑郁", "绝望"]):
        return "12320-5 心理援助 + 学校心理咨询中心（0371-61912356，学生活动中心3楼）+ 告诉辅导员"
    
    if any(kw in question for kw in ["查我的成绩", "课表", "卡余额", "我的课表", "我的余额", "成绩查询", "查成绩"]):
        return "抱歉，我无法接入学校系统查询个人信息，请通过教务系统或一卡通自助机查询"
    
    has_known_topic = any(topic in question for topic in KNOWN_TOPICS)
    if not has_known_topic and "没收录" not in answer and "0371-61911000" not in answer:
        return "这个我没收录，建议拨打 0371-61911000 总值班室问一下"
    
    return answer

RECOMMENDED = {
    "新生": ["报到流程是怎样的？需要带什么材料？", "学费什么时候交？怎么交？", "宿舍怎么分配？什么时候能入住？", "校园卡在哪里办？有什么功能？"],
    "在校生": ["怎么开在读证明？需要什么材料？", "学生证丢了怎么补办？要多久？", "宿舍报修怎么操作？联系谁？", "成绩单在哪里打印？免费吗？"],
    "教师": ["差旅怎么报销？需要什么材料？", "课表在哪里查询？怎么调整？", "教材怎么领取？什么时候领？", "会议室怎么预约？"]
}

PHONE_BOOK = {
    "招生办": {"电话": "0371-61916161", "地址": "行政楼1楼103室"},
    "教务处": {"电话": "0371-61912346", "地址": "行政楼2楼201室"},
    "学生处": {"电话": "0371-61912355", "地址": "学生活动中心1楼"},
    "财务处": {"电话": "0371-61912348", "地址": "行政楼3楼301室"},
    "图书馆": {"电话": "0371-61912349", "地址": "图书馆1楼服务台"},
    "后勤处": {"电话": "0371-61912350", "地址": "后勤楼1楼"},
    "校医院": {"电话": "0371-61912353", "地址": "校医院门诊楼"},
    "保卫处": {"电话": "0371-61912357", "地址": "校门东侧保卫科"},
    "网信中心": {"电话": "0371-61912718", "地址": "信息楼3楼"},
    "心理咨询中心": {"电话": "0371-61912356", "地址": "学生活动中心3楼"},
    "总值班室": {"电话": "0371-61911000", "地址": "行政楼1楼"}
}

def main():
    st.set_page_config(page_title="小航 · 郑州航院智能问答", page_icon="🏫", layout="wide")
    st.title("🏫 小航 · 郑州航空工业管理学院智能问答系统")

    if "page" not in st.session_state:
        st.session_state.page = "home"
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "qa_history" not in st.session_state:
        st.session_state.qa_history = []

    if st.session_state.page == "home":
        st.subheader("请选择您的身份")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🎒 新生", use_container_width=True):
                st.session_state.identity = "新生"
                st.session_state.page = "chat"
                st.rerun()
        with col2:
            if st.button("📚 在校生", use_container_width=True):
                st.session_state.identity = "在校生"
                st.session_state.page = "chat"
                st.rerun()
        with col3:
            if st.button("👨‍🏫 教师", use_container_width=True):
                st.session_state.identity = "教师"
                st.session_state.page = "chat"
                st.rerun()
        
        st.markdown("---")
        st.subheader("📞 校园电话黄页（无需网络）")
        for dept, info in PHONE_BOOK.items():
            st.write(f"**{dept}** | 📱 {info['电话']} | 🏠 {info['地址']}")
        
        st.markdown("---")
        st.subheader("📋 服务边界")
        st.write("✅ 能聊：新生入学、在校生事务、教师事务、通用服务、应急服务")
        st.write("❌ 不能聊：个人信息查询、系统操作、主观评价、闲聊娱乐")

    elif st.session_state.page == "chat":
        st.sidebar.button("🏠 返回首页", on_click=lambda: setattr(st.session_state, "page", "home"))
        st.sidebar.markdown(f"当前身份：**{st.session_state.identity}**")
        if st.sidebar.button("🗑️ 清空对话"):
            st.session_state.chat_history = []
            st.session_state.qa_history = []
            st.rerun()
        
        st.subheader(f"💬 小航（{st.session_state.identity}模式）")
        
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                with st.chat_message("user", avatar="👤"):
                    st.markdown(message["content"])
            else:
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(message["content"])
        
        st.markdown("💡 推荐问题：")
        for i, q in enumerate(RECOMMENDED[st.session_state.identity], 1):
            if st.button(f"{i}. {q}"):
                st.session_state.user_input = q
                st.rerun()
        
        user_question = st.text_input("请输入您的问题：", value=st.session_state.user_input, key="input_field")
        
        if st.button("发送") and user_question:
            st.session_state.user_input = user_question
            current_time = datetime.now().strftime("%H:%M:%S")
            
            st.session_state.chat_history.append({"role": "user", "content": user_question})
            
            with st.chat_message("user", avatar="👤"):
                st.markdown(user_question)
            
            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner("小航正在思考..."):
                    school_data = load_school_data()
                    system_prompt = get_system_prompt(st.session_state.identity, school_data)
                    answer = call_api(system_prompt, user_question)
                
                if "网络错误" in answer or "请求失败" in answer:
                    error_msg = f"❌ AI服务暂时不可用：{answer}"
                    st.error(error_msg)
                    st.markdown("📞 为您提供电话黄页兜底信息：")
                    fallback_info = ""
                    for dept, info in PHONE_BOOK.items():
                        fallback_info += f"**{dept}** | 📱 {info['电话']}\n"
                    st.markdown(fallback_info)
                    full_answer = error_msg + "\n\n📞 为您提供电话黄页兜底信息：\n" + fallback_info
                else:
                    answer = post_check(user_question, answer)
                    st.markdown(answer)
                    full_answer = answer
            
            st.session_state.chat_history.append({"role": "assistant", "content": full_answer})
            
            record = {
                "time": current_time,
                "identity": st.session_state.identity,
                "question": user_question,
                "answer": full_answer
            }
            st.session_state.qa_history.insert(0, record)
        
        if len(st.session_state.qa_history) > 0:
            st.markdown("---")
            col1, col2 = st.columns([4, 1])
            with col1:
                st.subheader("📝 问答历史")
            with col2:
                if st.button("🗑️ 清空历史"):
                    st.session_state.qa_history = []
                    st.rerun()
            
            for record in st.session_state.qa_history:
                st.markdown(f"""
**[{record['time']}] {record['identity']}**  
提问：{record['question']}  
回答：{record['answer'][:100]}{'...' if len(record['answer']) > 100 else ''}
""")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"系统异常：{e}")
        st.markdown("📋 切换到静态页面兜底：")
        st.markdown("## 校园电话黄页")
        for dept, info in PHONE_BOOK.items():
            st.write(f"**{dept}** | 📱 {info['电话']} | 🏠 {info['地址']}")