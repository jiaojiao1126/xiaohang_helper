n=input("请输入一个正整数：")
sum=0
j=0
o=0
for i in n:
    i2=int(i)
    sum=sum+i2
    if(i2%2==0):
        o=o+1
    else:
        j=j+1
print(f"各位数字之和：{sum}")
print(f"奇数个数：{j},偶数个数：{o}")
t=len(n)
if(n==n[::-1]):
    print("是回文数")
else:
    print("不是回文数")


