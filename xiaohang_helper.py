import requests
import os
import sys


def load_school_data(data_dir="data"):
    files = ["01_新生入学.md", "02_办事流程.md", "03_电话黄页.md", "04_应急防骗.md"]
    content = ""
    for fname in files:
        path = os.path.join(data_dir, fname)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                content += f"\n\n=== {fname} ===\n" + f.read()
        else:
            print(f"⚠ 文件不存在：{path}")
    return content


def get_system_prompt(identity, school_data):
    alias_dict = """
【别名词典】
- "学校""航院""ZUA""郑航" = 郑州航空工业管理学院
- "新校区""龙湖""新校" = 龙子湖校区
- "卡""饭卡""校卡" = 校园一卡通
- "保安""门卫""校警" = 保卫处
- "迁户口""落户" = 户籍迁入/迁出
- "调宿舍""换宿舍" = 宿舍调整申请
- "证明""在读证明" = 在校学籍证明
"""

    hard_rules = """
【防幻觉硬规则】-必须严格执行！
1. 只能根据【学校资料】回答，资料里没有的问题，直接回复"这个我没收录，建议拨打 0371-61911000 总值班室问一下"，不要回答其他内容
2. 严禁编造电话号码、地址、办公时间、学费金额、人名，必须从【学校资料】中查找
3. 涉及金钱/转账，无条件在回答末尾添加提示："先联系辅导员核实，任何要求转账的都是诈骗"
4. 涉及心理危机（自杀、不想活、活不下去等），立即回复："12320-5 心理援助 + 学校心理咨询中心（0371-61912356，学生活动中心3楼）+ 告诉辅导员"，不要回答其他内容
5. 被问"查我的成绩/课表/卡余额"等需要接入学校系统的问题，礼貌拒绝："抱歉，我无法接入学校系统查询个人信息，请通过教务系统或一卡通自助机查询"，不要回答其他内容
6. 回答末尾必须标注 [来源:文件名]，例如 [来源:01_新生入学.md]
"""

    role_templates = {
        "新生": """你是"小航"，郑州航空工业管理学院的校园信息查询 AI 助手。
当前用户身份：大一新生。
你像一位热心的大二学长，语气详细、口语化、多给鼓励。
回答重点：把流程拆成具体步骤，涉及金钱/转账必须按硬规则3提示防骗。""",
        
        "在校生": """你是"小航"，郑州航空工业管理学院的校园信息查询 AI 助手。
当前用户身份：在校老生。
你像一位办事老司机学长，语气简洁。
回答重点：① 地点 ② 电话 ③ 所需材料 ④ 办结时间。""",
        
        "教师": """你是"小航"，郑州航空工业管理学院的校园信息查询 AI 助手。
当前用户身份：教师。
语气专业礼貌。
回答重点：① 政策依据 ② 办事窗口 ③ 联系人。"""
    }

    role = role_templates.get(identity, "你是小航校园助手。")
    return f"{role}\n{hard_rules}\n{alias_dict}\n【学校资料】\n{school_data}"


def call_api(system_prompt, user_question):
    API_URL = "https://api.siliconflow.cn/v1/chat/completions"
    API_KEY = "sk-fzzfbikzcvltveiogdxixyftsokesldzvmeabbqyvhsaanfm"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "Qwen/Qwen2.5-7B-Instruct",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_question}
        ]
    }
    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            return "响应格式错误"
        return f"请求失败 [{response.status_code}]"
    except Exception as e:
        return f"网络错误: {str(e)}"


def ask_xiaohang(identity, question, school_data):
    system_prompt = get_system_prompt(identity, school_data)
    return call_api(system_prompt, question)


PHONE_BOOK = {
    "招生办": {"电话": "0371-61912345", "地址": "行政楼1楼101室", "服务时间": "周一至周五 8:30-17:30"},
    "教务处": {"电话": "0371-61912346", "地址": "行政楼2楼201室", "服务时间": "周一至周五 8:30-17:30"},
    "学生处": {"电话": "0371-61912347", "地址": "学生活动中心1楼", "服务时间": "周一至周日 9:00-18:00"},
    "财务处": {"电话": "0371-61912348", "地址": "行政楼3楼301室", "服务时间": "周一至周五 8:30-17:30"},
    "图书馆": {"电话": "0371-61912349", "地址": "图书馆1楼服务台", "服务时间": "周一至周日 8:00-22:00"},
    "后勤处": {"电话": "0371-61912350", "地址": "后勤楼1楼", "服务时间": "24小时"},
    "校医院": {"电话": "0371-61912351", "地址": "校医院门诊楼", "服务时间": "24小时"},
    "保卫处": {"电话": "0371-61912352", "地址": "校门东侧保卫科", "服务时间": "24小时"},
    "网络中心": {"电话": "0371-61912353", "地址": "信息楼3楼", "服务时间": "周一至周五 8:30-17:30"},
    "就业指导中心": {"电话": "0371-61912354", "地址": "学生活动中心2楼", "服务时间": "周一至周五 8:30-17:30"},
    "心理咨询中心": {"电话": "0371-61912356", "地址": "学生活动中心3楼", "服务时间": "周一至周五 9:00-17:00"},
    "总值班室": {"电话": "0371-61911000", "地址": "行政楼1楼", "服务时间": "24小时"}
}


def show_phone_book():
    print("\n" + "=" * 60)
    print("📞 校园电话黄页")
    print("=" * 60)
    for dept, info in PHONE_BOOK.items():
        print(f"\n【{dept}】")
        print(f"  电话: {info['电话']}")
        print(f"  地址: {info['地址']}")
        print(f"  服务时间: {info['服务时间']}")
    print("\n" + "=" * 60)


RECOMMENDED_QUESTIONS = {
    "新生": [
        "报到流程是怎样的？需要带什么材料？",
        "学费什么时候交？怎么交？",
        "宿舍怎么分配？什么时候能入住？",
        "校园卡在哪里办？有什么功能？"
    ],
    "在校生": [
        "怎么开在读证明？需要什么材料？",
        "学生证丢了怎么补办？要多久？",
        "宿舍报修怎么操作？联系谁？",
        "成绩单在哪里打印？免费吗？"
    ],
    "教师": [
        "差旅怎么报销？需要什么材料？",
        "课表在哪里查询？怎么调整？",
        "教材怎么领取？什么时候领？",
        "会议室怎么预约？有哪些会议室？"
    ]
}


KNOWN_TOPICS = [
    "报到", "学费", "缴费", "宿舍", "校园卡", "军训", "图书馆",
    "在读证明", "学生证", "补办", "请假", "成绩单", "报修",
    "差旅", "报销", "课表", "教材", "会议室", "心理", "防骗",
    "保卫处", "教务处", "学生处", "财务处", "校医院", "网络",
    "入学", "证明", "打印", "申请", "奖学金", "就业", "后勤"
]


def post_check_answer(question, answer):
    crisis_keywords = ["不想活", "自杀", "活不下去", "想死", "抑郁", "绝望"]
    info_keywords = ["查我的成绩", "课表", "卡余额", "成绩查询", "我的课表", "我的余额", "查成绩"]
    
    for kw in crisis_keywords:
        if kw in question:
            return "12320-5 心理援助 + 学校心理咨询中心（0371-61912356，学生活动中心3楼）+ 告诉辅导员"
    
    for kw in info_keywords:
        if kw in question:
            return "抱歉，我无法接入学校系统查询个人信息，请通过教务系统或一卡通自助机查询"
    
    has_known_topic = any(topic in question for topic in KNOWN_TOPICS)
    if not has_known_topic and "没收录" not in answer and "0371-61911000" not in answer:
        return "这个我没收录，建议拨打 0371-61911000 总值班室问一下"
    
    return answer


def show_boundary():
    print("\n" + "="*60)
    print("📋 服务边界声明")
    print("="*60)
    
    print("\n✅ 能聊的内容：")
    can_chat = [
        "新生入学：报到流程、缴费方式、宿舍分配、校园卡办理",
        "在校生事务：证明办理、证件补办、请假流程、成绩单打印",
        "教师事务：差旅报销、课表查询、教材领取、会议室预约",
        "通用服务：图书馆、食堂、校园网、校医院、保卫处",
        "应急服务：心理援助、防骗提醒、紧急联系方式"
    ]
    for item in can_chat:
        print(f"   - {item}")
    
    print("\n❌ 不能聊的内容：")
    cannot_chat = [
        "个人信息查询：成绩、课表、一卡通余额、个人档案（无法接入系统）",
        "系统操作：选课、缴费、请假审批、成绩申诉（需在官方系统操作）",
        "主观评价：饭菜口味、教学水平、设施好坏（无客观答案）",
        "闲聊娱乐：天气、新闻、笑话、情感问题（超出服务范围）",
        "非法违规：作弊、代考、违法活动（违反校规校纪）",
        "资料未收录：电话、地址、时间、费用等（严禁编造）"
    ]
    for item in cannot_chat:
        print(f"   - {item}")
    
    print("\n📅 数据更新日期：")
    data_update = {
        "01_新生入学.md": "2026年7月14日",
        "02_办事流程.md": "2026年7月14日",
        "03_电话黄页.md": "2026年7月14日",
        "04_应急防骗.md": "2026年7月14日"
    }
    for fname, date in data_update.items():
        print(f"   - {fname}: {date}")
    
    print("\n⚠️ 免责声明：系统回答仅供参考，最终以学校官方通知为准")
    print("="*60)


def chat_interactive(school_data):
    print("\n" + "="*60)
    print("🏫 小航 · 郑州航空工业管理学院智能问答系统")
    print("="*60)
    
    while True:
        print("\n请选择身份：")
        print("  1. 🎒 新生")
        print("  2. 📚 在校生")
        print("  3. 👨‍🏫 教师")
        print("  4. 📋 服务边界声明")
        print("  5. 📞 电话黄页")
        print("  0. 退出")
        
        choice = input("\n输入编号：")
        
        if choice == "0":
            print("\n再见！")
            break
        
        if choice == "4":
            show_boundary()
            continue
        
        if choice == "5":
            show_phone_book()
            continue
        
        identity = {"1": "新生", "2": "在校生", "3": "教师"}.get(choice)
        if not identity:
            print("❌ 无效输入，请重新选择")
            continue
        
        print(f"\n当前身份：{identity}")
        print(f"\n💡 推荐问题（输入编号快速提问）：")
        questions = RECOMMENDED_QUESTIONS.get(identity, [])
        for i, q in enumerate(questions, 1):
            print(f"   {i}. {q}")
        print("   0. 返回上级菜单")
        
        q_choice = input("\n输入问题编号或直接输入问题：")
        
        if q_choice == "0":
            continue
        
        if q_choice.isdigit() and 1 <= int(q_choice) <= len(questions):
            question = questions[int(q_choice) - 1]
        else:
            question = q_choice
        
        print(f"\n你的问题：{question}")
        
        answer = ask_xiaohang(identity, question, school_data)
        
        if "网络错误" in answer or "请求失败" in answer:
            print(f"\n❌ AI服务暂时不可用")
            print("📞 为您提供电话黄页兜底信息：")
            
            matched_depts = []
            for dept in PHONE_BOOK.keys():
                if dept in question:
                    matched_depts.append(dept)
            
            if matched_depts:
                for dept in matched_depts:
                    info = PHONE_BOOK[dept]
                    print(f"\n【{dept}】")
                    print(f"   电话: {info['电话']}")
                    print(f"   地址: {info['地址']}")
                    print(f"   服务时间: {info['服务时间']}")
            else:
                print("\n未找到相关部门，以下是常用部门：")
                for dept in ["招生办", "学生处", "教务处"]:
                    info = PHONE_BOOK[dept]
                    print(f"\n【{dept}】")
                    print(f"   电话: {info['电话']}")
                    print(f"   地址: {info['地址']}")
        else:
            answer = post_check_answer(question, answer)
            print(f"\n小航：\n{answer}")
        
        print("\n" + "="*60)


def run_tests(school_data):
    test_cases = [
        ("新生", "学费什么时候交"),
        ("在校生", "怎么开在读证明"),
        ("教师", "差旅怎么报销"),
        ("新生", "查我的成绩"),
        ("在校生", "我不想活了"),
        ("教师", "食堂几点开门"),
    ]
    
    print("\n" + "="*60)
    print("🧪 自动测试模式 - 验证6个验收用例")
    print("="*60)
    
    for identity, question in test_cases:
        print(f"\n{'='*60}")
        print(f"身份：{identity} | 问题：{question}")
        print(f"{'='*60}")
        
        answer = ask_xiaohang(identity, question, school_data)
        answer = post_check_answer(question, answer)
        
        print(f"回答：\n{answer}")
        
        check_result = []
        if identity == "新生" and question == "学费什么时候交":
            if "学费" in answer or "缴费" in answer:
                check_result.append("✓ 回答包含学费相关内容")
            if "先联系辅导员" in answer or "诈骗" in answer:
                check_result.append("✓ 包含防骗提示")
            if "[来源" in answer:
                check_result.append("✓ 来源标注")
        
        elif identity == "在校生" and question == "怎么开在读证明":
            if "教务处" in answer:
                check_result.append("✓ 包含办理地点")
            if "0371" in answer:
                check_result.append("✓ 包含联系电话")
            if "[来源" in answer:
                check_result.append("✓ 来源标注")
        
        elif identity == "教师" and question == "差旅怎么报销":
            if "财务处" in answer or "报销" in answer:
                check_result.append("✓ 包含报销相关内容")
            if "政策" in answer or "依据" in answer:
                check_result.append("✓ 包含政策依据")
            if "[来源" in answer:
                check_result.append("✓ 来源标注")
        
        elif "查我的成绩" in question:
            if "无法接入" in answer or "抱歉" in answer:
                check_result.append("✓ 硬规则5生效：拒绝查询个人信息")
        
        elif "不想活了" in question:
            if "12320" in answer:
                check_result.append("✓ 硬规则4生效：心理危机干预")
        
        elif "食堂几点开门" in question:
            if "没收录" in answer or "0371-61911000" in answer:
                check_result.append("✓ 硬规则1生效：资料缺失处理")
        
        if check_result:
            for r in check_result:
                print(f"\n{r}")
        else:
            print("\n⚠️ 未检测到预期行为")


def main():
    school_data = load_school_data()
    
    if not school_data:
        print("❌ 未加载到学校资料，请检查data文件夹")
        return
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests(school_data)
    else:
        chat_interactive(school_data)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ 系统异常：{e}")
        print("\n📋 切换到静态页面兜底：")
        show_boundary()
        show_phone_book()
