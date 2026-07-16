import requests

API_URL = "https://api.siliconflow.cn/v1/chat/completions"
API_KEY = "sk-fzzfbikzcvltveiogdxixyftsokesldzvmeabbqyvhsaanfm"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def ask_ai(prompt):
    data = {
        "model": "Qwen/Qwen2.5-7B-Instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                return f"错误: 没有找到回答，响应: {result}"
        else:
            try:
                error_info = response.json()
                return f"请求失败，状态码: {response.status_code}, 错误信息: {error_info.get('message', '未知错误')}"
            except:
                return f"请求失败，状态码: {response.status_code}, 响应内容: {response.text}"
    except Exception as e:
        return f"发生错误: {e}"


if __name__ == "__main__":
    # 普通 Prompt
    prompt_simple = "什么是函数"

    # 结构化 Prompt（四要素：角色 + 背景 + 任务 + 要求）
    prompt_structured = """
角色：你是一位耐心的编程入门老师
背景：我是一位刚学编程的大学生，对计算机术语不太熟悉
任务：请解释什么是函数
要求：
1. 用通俗易懂的语言，避免专业术语
2. 给出一个生活中的例子帮助理解
3. 回答不超过5句话
"""

    print("=" * 60)
    print("【普通 Prompt】")
    print(f"Prompt: {prompt_simple}")
    print("-" * 60)
    answer_simple = ask_ai(prompt_simple)
    print(f"回答:\n{answer_simple}")
    print()

    print("=" * 60)
    print("【结构化 Prompt（四要素）】")
    print(f"Prompt:\n{prompt_structured}")
    print("-" * 60)
    answer_structured = ask_ai(prompt_structured)
    print(f"回答:\n{answer_structured}")
    print()

    print("=" * 60)
    print("【对比观察记录】")
    print("=" * 60)
    # 观察1：回答风格差异
    # 普通Prompt的回答偏学术化，使用了"模块化"、"复用"、"可读性"、"维护性"等专业术语
    # 结构化Prompt的回答更通俗易懂，使用了"魔法盒子"这样的生动比喻，降低理解门槛

    # 观察2：回答长度与完整性差异
    # 普通Prompt的回答较长且不够完整，末尾突然出现了另一个问题的开头，说明模型可能产生了幻觉
    # 结构化Prompt的回答简洁完整，严格控制在3-4句话，符合"不超过5句话"的要求

    # 观察3：回答重点差异
    # 普通Prompt的回答侧重于函数的技术定义和组成部分，偏向理论知识
    # 结构化Prompt的回答侧重于实际理解，用"做甜品"的生活例子帮助初学者建立直观认知

    # 观察4：语言自然度差异
    # 普通Prompt的回答略显生硬，出现了"性性复性性"这样的重复错误，语言不够流畅
    # 结构化Prompt的回答语言流畅自然，逻辑清晰，更像真人老师在讲解
