y=int(input("请输入年份："))
m=int(input("请输入月份："))
if(y%4==0 and y%100!=0 or y%400==0):
    n2=29
else:
    n2=28
if(m==1 or m==3 or m==5 or m==7 or m==8 or m==10 or m==12):
    n1=31
    print(f"{y}年{m}月有{n1}天")
if(m==4 or m==6 or m==9 or m==11):
    n3=30
    print(f"{y}年{m}月有{n3}天")
if(m==2):
    print(f"{y}年{m}月有{n2}天")