students = [
    {"name": "张三", "age": 18, "score": 85},
    {"name": "李四", "age": 19, "score": 92},
    {"name": "王五", "age": 18, "score": 47},
    {"name": "赵六", "age": 20, "score": 76},
]
def show_all(students):
    for stu in students:
        print(stu)
def find_by_name(students, name):
    for stu in students:
        if stu["name"] == name:
            return stu
    return None
def get_average(students):
    total = 0
    for stu in students:
        total += stu["score"]
    avg = total / len(students)
    return round(avg, 1)
def get_pass_count(students):
    cnt = 0
    for stu in students:
        if stu["score"] >= 60:
            cnt += 1
    return cnts
if __name__ == "__main__":
    print("全部学生信息：")
    show_all(students)
    avg_score = get_average(students)
    pass_num = get_pass_count(students)
    print(f"\n班级平均分：{avg_score}")
    print(f"及格人数：{pass_num}")
