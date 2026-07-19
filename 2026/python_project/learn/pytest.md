pytest 是 Python 的自动化测试工具。它的作用不是运行主程序，而是用一组固定输入检查函数行为是否符合预期。

def add(a: int, b: int) -> int:
    return a + b

def test_add(): #用test_普通函数名命名，因为pytest 默认识别以 test_ 开头的函数
    result = add(2, 3)
    assert result == 5 #断言。 assert 条件
    
测试文件也通常以 test_ 开头  比如test_batch_plan_analyzer.py

有些函数遇到非法输入不会抛异常，而是返回错误列表。
validate_plan(plan)缺少 steps 时返回：["缺少 steps 字段"]

此时测试可以写成：
def test_validate_plan_rejects_missing_steps():
    plan = {
        "name": "demo",
    }

    errors = validate_plan(plan)

    assert errors == ["缺少 steps 字段"]

这里不是检查异常，而是检查返回值
因此要区分两种失败方式：

validate_plan()
→ 返回错误列表

read_plan()
→ 某些情况下抛出异常

# 异常路径测试
pytest.raises()

with pytest.raises(异常类型):
    可能抛出异常的代码

例如
with pytest.raises(ValueError):
    int("abc")
含义是我认为int("abc")会抛出 ValueError 异常，如果没有抛出异常，测试失败，抛出其他异常也会失败。
和
try:
    read_plan(file_path)
except FileNotFoundError:
    pass
作用差不多，但是try...except...是运行时的异常处理，而pytest.raises()是测试时的异常断言。
因为如果 read_plan() 根本没有抛异常，代码也可能正常结束，测试不会自动失败。
需要额外写很多逻辑：
try:
    read_plan(file_path)
except FileNotFoundError:
    pass
else:
    assert False

pytest.raises() 已经替你完成了这套判断，而且更清楚更标准
with pytest.raises(FileNotFoundError):
    read_plan(file_path)

tmp_path
tmp_path 是 pytest 提供的临时目录。
测试函数只要声明参数：

def test_something(tmp_path):

pytest 就会自动创建一个临时 Path 对象传入。

你不需要自己调用：

tmp_path = ...

例如
def test_create_file(tmp_path):
    file_path = tmp_path / "data.txt"

    file_path.write_text(
        "hello",
        encoding="utf-8",
    )

    assert file_path.exists()

pytest 会自动提供类似这样的目录：

/tmp/pytest-of-user/pytest-0/test_create_file0/

测试结束后由 pytest 管理。

还可以创建临时json文件：
合法json文件：
file_path = tmp_path / "plan.json"

file_path.write_text(
    '{"steps": []}',
    encoding="utf-8",
)
非法json文件：
file_path = tmp_path / "invalid.json"

file_path.write_text(
    '{"steps":',
    encoding="utf-8",
)

然后调用read_plan(file_path)，不需要用open()，read_plan()内部会自己打开文件。