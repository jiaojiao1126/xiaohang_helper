n=int(input())
if(n>=90 and n<=100):
    print("A（优秀）")
elif(n>=80 and n<=89):
    print("B（良好）")
elif(n>=70 and n<=79):
    print("C（中等）")
elif(n>=60 and n<=69):
    print("D（及格）")
elif(n>=0 and n<=59):
    print("E（不及格）")
else:
    print("成绩无效")