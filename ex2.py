b={"title":"Python入门","author":"张老师","price":59.0,"stock":10}
print("书名：",b["title"],"作者：",b["author"])
b["price"]="49.0（打折）"
print(b)
b["publisher"]="清华大学出版社"
print(b)
del b["stock"]
print(b)
for k,v in b.items():
    print(k,v)