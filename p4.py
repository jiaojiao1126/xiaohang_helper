s=input()
n=len(s)
sum=0
if(n>=8):
    sum=sum+1
for i in s:
    if(i.isdigit()):
        sum=sum+1
    elif(i.isupper()):
        sum=sum+1
    elif(i.lower()):
        sum=sum+1
    else:
        sum=sum+1
if(sum>=0 and sum<=1):
    print("弱")
elif(sum>=2 and sum<=3):
    print("中")
else:
    print("强")

