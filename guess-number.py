import random
num = random.randint(1,100)
while 1:
    n=int(input("输入一个数在1到100之间："))
    if n>num:
        print("数字偏大")
    elif n<num:
        print("数字偏小")
    else:
        print("猜对啦")
        break