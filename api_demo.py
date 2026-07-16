import requests

API_URL = "https://api.siliconflow.cn/v1/chat/completions"
API_KEY = "sk-fzzfbikzcvltveiogdxixyftsokesldzvmeabbqyvhsaanfm"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "Qwen/Qwen2-7B-Instruct",
    "messages": [
        {"role": "user", "content": "请用3句话介绍郑州航空工业管理学院"}
    ]
}

response = requests.post(API_URL, headers=headers, json=data)

if response.status_code == 200:
    result = response.json()
    if "choices" in result and len(result["choices"]) > 0:
        answer = result["choices"][0]["message"]["content"]
        print("回答:", answer)
    else:
        print("错误: 没有找到回答")
        print("响应:", result)
else:
    print(f"请求失败，状态码: {response.status_code}")
    try:
        error_info = response.json()
        print("错误信息:", error_info.get("message", "未知错误"))
    except:
        print("响应内容:", response.text)
