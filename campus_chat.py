import requests
from phone_book import show_phone_book, get_department_info, list_all_departments

API_URL = "https://api.siliconflow.cn/v1/chat/completions"
API_KEY = "sk-fzzfbikzcvltveiogdxixyftsokesldzvmeabbqyvhsaanfm"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

PROMPT_NEW_STUDENT = """
角色：你是一位耐心亲切的新生接待老师
背景：我是刚入学的大一新生，第一次来学校，对校园环境和报到流程不熟悉，很担心出错或被骗
任务：请回答我的问题，帮助我顺利完成报到和适应校园生活
要求：
1. 回答要详细具体，步骤清晰，让我知道每一步该做什么
2. 提醒我注意事项，特别是容易踩坑或被骗的地方
3. 语气亲切温暖，让我感受到学校的关怀
4. 如果涉及到具体地点，请说明详细位置
5. 回答不超过8句话
"""

PROMPT_CURRENT_STUDENT = """
角色：你是一位熟悉校园事务的在校生助手
背景：我是在校学生，经常需要办理各种事务，比如请假、补办证件、缴纳费用等，但不知道具体流程和需要带什么材料
任务：请回答我的问题，帮助我高效办理校园事务
要求：
1. 回答要简洁明了，突出重点
2. 明确说明办理地点、需要携带的材料、办理时间
3. 如果有联系方式，请一并提供
4. 回答不超过6句话
"""

PROMPT_TEACHER = """
角色：你是一位专业的校园行政办事员
背景：我是学校教职工，需要办理教学、科研、人事等方面的事务，需要明确的政策依据和具体联系人
任务：请回答我的问题，提供准确的政策信息和办事指引
要求：
1. 回答要专业准确，引用相关政策文件或规定
2. 明确说明办事流程、所需材料、审批部门和联系人
3. 如果有相关文件链接或附件要求，请一并说明
4. 回答不超过6句话
"""

RECOMMENDED_QUESTIONS = {
    "新生": [
        "报到流程是怎样的？",
        "宿舍怎么分配？",
        "军训需要准备什么？",
        "校园卡在哪里办理？",
        "怎么交学费？",
        "图书馆怎么进？",
        "食堂有几个？在哪里？",
        "报到时要注意什么，防止被骗？"
    ],
    "在校生": [
        "请假流程是什么？",
        "学生证丢了怎么补办？",
        "成绩单在哪里打印？",
        "宿舍报修怎么操作？",
        "图书馆借书有什么规定？",
        "怎么申请奖学金？",
        "校园网怎么开通？",
        "就业指导中心在哪里？"
    ],
    "教师": [
        "课表在哪里查询？",
        "教学成果奖怎么申报？",
        "科研经费怎么报销？",
        "人事档案在哪里查询？",
        "职称评审有什么要求？",
        "实验室怎么预约？",
        "教材领取在哪里？",
        "会议室怎么预约？"
    ]
}


def ask_ai(prompt_template, user_question):
    full_prompt = f"{prompt_template}\n\n我的问题：{user_question}"
    
    data = {
        "model": "Qwen/Qwen2.5-7B-Instruct",
        "messages": [
            {"role": "user", "content": full_prompt}
        ]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                return None
        else:
            return None
    except Exception as e:
        print(f"API调用失败: {e}")
        return None


def show_recommended_questions(role):
    questions = RECOMMENDED_QUESTIONS.get(role, [])
    print(f"\n💡 推荐问题（点击数字提问）：")
    for i, q in enumerate(questions, 1):
        print(f"  {i}. {q}")
    print("  0. 返回上级菜单")


def chat_with_role(role, prompt_template):
    print(f"\n{'='*60}")
    print(f"🎓 {role}专属问答模式")
    print(f"{'='*60}")
    
    while True:
        show_recommended_questions(role)
        
        choice = input("\n请输入问题编号或直接输入问题：")
        
        if choice == "0":
            break
        
        if choice.isdigit() and 1 <= int(choice) <= len(RECOMMENDED_QUESTIONS.get(role, [])):
            user_question = RECOMMENDED_QUESTIONS[role][int(choice) - 1]
        else:
            user_question = choice
        
        print(f"\n你的问题：{user_question}")
        
        answer = ask_ai(prompt_template, user_question)
        
        if answer:
            print(f"\nAI回答：\n{answer}")
        else:
            print("\n❌ AI服务暂时不可用，为您提供电话黄页兜底信息：")
            
            keywords = ["招生办", "教务处", "学生处", "财务处", "图书馆", "后勤处", "校医院", "保卫处"]
            matched_depts = []
            for kw in keywords:
                if kw in user_question:
                    matched_depts.append(kw)
            
            if matched_depts:
                for dept in matched_depts:
                    info = get_department_info(dept)
                    if info:
                        print(f"\n【{dept}】")
                        print(f"  电话: {info['电话']}")
                        print(f"  地址: {info['地址']}")
                        print(f"  服务时间: {info['服务时间']}")
            else:
                print("\n未找到相关部门，以下是常用部门联系方式：")
                for dept in ["招生办", "学生处", "教务处"]:
                    info = get_department_info(dept)
                    if info:
                        print(f"\n【{dept}】")
                        print(f"  电话: {info['电话']}")
                        print(f"  地址: {info['地址']}")
            
            print("\n需要查看完整电话黄页吗？(y/n)")
            if input().lower() == "y":
                show_phone_book()
        
        print("\n" + "="*60)


def show_static_page():
    print(f"\n{'='*60}")
    print("⚠️  系统维护中 - 静态页面")
    print(f"{'='*60}")
    print("\n以下是校园常用服务信息：")
    
    print("\n📌 新生报到指引")
    print("  1. 到行政楼1楼招生办领取报到单")
    print("  2. 到宿舍区办理入住手续")
    print("  3. 到图书馆办理校园卡")
    print("  4. 注意：不要相信校外人员推销")
    
    print("\n📌 在校生办事指南")
    print("  - 学生证补办：学生活动中心1楼")
    print("  - 成绩单打印：教务处201室")
    print("  - 宿舍报修：后勤楼1楼")
    
    print("\n📌 教师办事指引")
    print("  - 教学事务：教务处")
    print("  - 科研事务：科研处")
    print("  - 人事事务：人事处")
    
    print("\n📞 紧急联系方式")
    print("  - 校医院：0371-61912351")
    print("  - 保卫处：0371-61912352")
    print("  - 后勤处：0371-61912350")
    
    show_phone_book()


def main():
    print(f"\n{'='*60}")
    print("🏫 校园智能问答系统")
    print(f"{'='*60}")
    print("\n请选择您的身份：")
    print("  1. 🎒 新生报到")
    print("  2. 📚 在校生办事")
    print("  3. 👨‍🏫 教师办事")
    print("  4. 📞 电话黄页")
    print("  0. 退出")
    
    while True:
        choice = input("\n请输入编号：")
        
        if choice == "1":
            chat_with_role("新生", PROMPT_NEW_STUDENT)
        elif choice == "2":
            chat_with_role("在校生", PROMPT_CURRENT_STUDENT)
        elif choice == "3":
            chat_with_role("教师", PROMPT_TEACHER)
        elif choice == "4":
            show_phone_book()
        elif choice == "0":
            print("\n再见！")
            break
        else:
            print("\n❌ 无效输入，请重新选择")
        
        print(f"\n{'='*60}")
        print("🏫 校园智能问答系统")
        print(f"{'='*60}")
        print("\n请选择您的身份：")
        print("  1. 🎒 新生报到")
        print("  2. 📚 在校生办事")
        print("  3. 👨‍🏫 教师办事")
        print("  4. 📞 电话黄页")
        print("  0. 退出")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ 系统异常，切换到静态页面：{e}")
        show_static_page()
