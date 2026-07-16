import random
while True:
    num=random.randint(1,100)
    m=7
    c=0
    while c < m:
        c=c+1
        r=m-c
        g=int(input("请输入数字："))
        if(g>num):
            print(f"猜大了，还剩{r}次")
        elif(g<num):
            print(f"猜小了，还剩{r}次")
        else:
            print(f"恭喜答对！用了{c}次")
            break
        if(c==m):
           print(f"游戏结束，答案是{num}")
    t=input("再来一局吗？（y/n）")
    if(t=='n'):
        break

