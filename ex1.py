fruits=["苹果","香蕉","橘子"]
n=len(fruits)
print(n)
fruits.append("西瓜")
print(fruits)
fruits.insert(1,"葡萄")
print(fruits)
fruits.remove("橘子")
print(fruits)
for f in fruits:
    print(f)
def find_fruit(fruits,fruit):
    if fruit in fruits:
        return True
    else:
        return False
def find_fruit2(fruits):
        print(fruits)


