def celsius_to_fahrenheti(c):
    f=c*9/5+32
    return f
def fahrenheit_to_celsius(f):
    c=(f-32)*5/9
    return round(c,1)
while True:
    print("1.摄氏转华氏 2.华氏转摄氏 3.退出")
    n=input("请选择：")
    if(n=='1'):
            try:
                c=float(input("请输入摄氏温度："))
                a=celsius_to_fahrenheti(c)
                print(f"华氏温度:{a}")
            except:
                print("请输入有效数字")
    elif(n=='2'):
            try:
               f=float(input("请输入华氏温度"))
               b=fahrenheit_to_celsius(f)
               print(f"摄氏温度:{b}")
            except:
                print("请输入有效数字")
    elif(n=='3'):
            print("程序结束")
            break
    else:
        print("请输入有效数字")



