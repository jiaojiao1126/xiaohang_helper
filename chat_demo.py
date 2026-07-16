import requests

API_URL = "https://api.siliconflow.cn/v1/chat/completions"
API_KEY = "sk-fzzfbikzcvltveiogdxixyftsokesldzvmeabbqyvhsaanfm"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

messages = []
print("AI 学习助手（输入 quit 退出）")
print("=" * 40)

while True:
    user_input = input("\n你：")
    if user_input.lower() == "quit":
        print("再见！")
        break

    messages.append({"role": "user", "content": user_input})

    data = {
        "model": "Qwen/Qwen2.5-7B-Instruct",
        "messages": messages
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                answer = result["choices"][0]["message"]["content"]
                messages.append({"role": "assistant", "content": answer})
                print(f"\nAI：{answer}")
            else:
                print("\nAI：抱歉，我没有找到回答")
                print("响应:", result)
        else:
            print(f"\nAI：请求失败，状态码: {response.status_code}")
            try:
                error_info = response.json()
                print("错误信息:", error_info.get("message", "未知错误"))
            except:
                print("响应内容:", response.text)

    except Exception as e:
        print(f"\nAI：发生错误: {e}")
