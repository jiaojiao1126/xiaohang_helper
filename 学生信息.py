def show_student(student):
    print("学号：", student["id"])
    print("姓名：", student["name"])
    print("专业：", student["major"])
def find_student(students, keyword):
    for student in students:
         if student["name"] == keyword:
            return student
    return None
students = [
    {"id": "2026001", "name": "张三", "major": "人工智能"},
    {"id": "2026002", "name": "李四", "major": "人工智能"},
    {"id": "2026003", "name": "王五", "major": "计算机科学与技术"}
]
try:
    keyword = input("请输入要查询的姓名：")
    result = find_student(students, keyword)
    if result is None:
        print("未找到该学生")
    else:
        show_student(result)
except:
    print("查询过程中出现错误，请检查数据格式。")