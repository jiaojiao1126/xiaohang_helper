import requests

API_URL = "https://api.siliconflow.cn/v1/chat/completions"
API_KEY = "sk-fzzfbikzcvltveiogdxixyftsokesldzvmeabbqyvhsaanfm"


def load_school_data():
    files = ["01_新生入学.md", "02_办事流程.md", "03_电话黄页.md", "04_应急防骗.md"]
    data_dir = "data"
    content = ""
    for fname in files:
        path = f"{data_dir}/{fname}"
        try:
            with open(path, "r", encoding="utf-8") as f:
                content += f"\n\n=== {fname} ===\n" + f.read()
        except FileNotFoundError:
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

    if identity == "新生":
        role = """你是"小航"，郑州航空工业管理学院的校园信息查询 AI 助手。
当前用户身份：大一新生。
你像一位热心的大二学长，语气详细、口语化、多给鼓励。
回答重点：把流程拆成具体步骤，涉及金钱/转账必须按硬规则3提示防骗。"""
    elif identity == "在校生":
        role = """你是"小航"，郑州航空工业管理学院的校园信息查询 AI 助手。
当前用户身份：在校老生。
你像一位办事老司机学长，语气简洁。
回答重点：① 地点 ② 电话 ③ 所需材料 ④ 办结时间。"""
    elif identity == "教师":
        role = """你是"小航"，郑州航空工业管理学院的校园信息查询 AI 助手。
当前用户身份：教师。
语气专业礼貌。
回答重点：① 政策依据 ② 办事窗口 ③ 联系人。"""
    else:
        role = "你是小航校园助手。"

    return f"{role}\n{hard_rules}\n{alias_dict}\n【学校资料】\n{school_data}"


def ask_xiaohang(identity, question, school_data):
    system_prompt = get_system_prompt(identity, school_data)
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "Qwen/Qwen2.5-7B-Instruct",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
    }
    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                answer = result["choices"][0]["message"]["content"]
                return answer
            else:
                return "抱歉，AI响应格式有误"
        else:
            try:
                error_info = response.json()
                return f"请求失败：{error_info.get('message', '未知错误')}"
            except:
                return f"请求失败，状态码: {response.status_code}"
    except Exception as e:
        return f"网络错误：{e}"


if __name__ == "__main__":
    school_data = load_school_data()
    print("=== 小航 · 校园信息查询 AI 助手 ===")
    print("请选择身份：1.新生 2.在校生 3.教师")
    choice = input("输入编号：")
    identity = {"1": "新生", "2": "在校生", "3": "教师"}.get(choice, "新生")
    print(f"当前身份：{identity}")
    question = input("你的问题：")
    answer = ask_xiaohang(identity, question, school_data)
    print(f"\n小航：{answer}")
