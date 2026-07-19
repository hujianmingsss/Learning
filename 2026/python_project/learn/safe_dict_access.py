#.get()方法实现安全访问

student = {
    "name" : "Li Ming",
    "score" : 88
}

print(student["name"]) #Li Ming 
#print(student["age"])
#程序无法执行，会报错：KeyError: 'age'  ,因为 "age"不存在

#[]一般含义是：我确定这个键必须存在，请直接取值，如果这个值不存在的话，程序会报错
#使用 .get() 安全访问，程序不会报错
print(student.get("age")) #None
print(student.get("age", 0)) #0 ,如果访问的键不存在，就输出0

#还可以使用列表默认值：
student = {
    "name": "Li Ming"
}
courses = student.get("courses", []) #没有"courses"键，返回默认值[],这里是返回了空列表

#用if判断来确定键是否存在是一个检查字段的方式，可以加强程序健壮性
if "score" in student:
    print("存在 score 字段")

if "age" not in student:
    print("缺少 age 字段")
    
#即"score" in student 判断字段是否存在，如果存在就返回true，不存在返回false
