from pathlib import Path
import json

# 参数可以是字符串路径，也可以是 Path 对象；
# 只查找当前目录中的 .json 文件；
# 返回由 Path 对象组成的列表；
# 按文件名排序；
# 函数内部不要打印；
# 暂时不用处理目录不存在的问题。
# Path(folder_path)
# glob("*.json")
# sorted(...)


def find_json_files(folder_path: str | Path) -> list[Path]:
    json_files = []

    folder = Path(folder_path)

    for json_file in folder.glob("*.json"):
        json_files.append(json_file)

    jsonfiles = sorted(
        json_files,
        key=lambda file_path: file_path.name,
    )

    # sorted() 不会原地修改原列表，
    # 它会返回一个新的已排序列表。
    return jsonfiles


# 要求：
# 参数可以是字符串路径，也可以是 Path 对象；
# 打开单个 JSON 文件；
# 使用 UTF-8 编码；
# 使用 json.load() 读取；
# 返回解析后的 Python 对象；
# 暂时不捕获非法 JSON 异常；
# 函数内部不要打印。


def read_plan(file_path: str | Path) -> dict[str, object]:
    file_path = Path(file_path)

    try:
        with file_path.open("r", encoding="utf-8") as file:
            plan = json.load(file)

    except FileNotFoundError as error:
        raise FileNotFoundError(
            f"文件不存在：{file_path}"
        ) from error

    except json.JSONDecodeError as error:
        raise ValueError(
            f"JSON格式错误: {file_path}"
        ) from error

    if not isinstance(plan, dict):
        raise ValueError(
            f"顶层结构必须是字典：{file_path}"
        )

    if "steps" not in plan:
        raise ValueError(
            f"缺少steps字段：{file_path}"
        )

    if not isinstance(plan["steps"], list):
        raise ValueError(
            f"steps必须是列表：{file_path}"
        )

    return plan


# 接收计划字典；
# 遍历 plan["steps"]；
# 提取每个 step 中的 tool_name；
# 返回工具名称列表。


def extract_tool_names(
    plan: dict[str, object],
) -> list[str]:
    tool_list = []

    for step in plan["steps"]:
        tool_list.append(step["tool_name"])

    return tool_list


# 接收工具名称列表；
# 返回一个字典；
# 字典的键是工具名称；
# 字典的值是该工具出现的次数；
# 不使用 collections.Counter；
# 函数内部不打印。


def count_tool_usage(
    tool_names: list[str],
) -> dict[str, int]:
    tool_count = {}

    for tool_name in tool_names:
        tool_count[tool_name] = (
            tool_count.get(tool_name, 0) + 1
        )

    return tool_count


# 接收 find_json_files() 返回的路径列表；
# 逐个调用 read_plan(file_path)；
# 合法 JSON 的解析结果加入 valid_plans；
# 非法 JSON 的文件名加入 invalid_plans；
# 返回两个列表。


def collect_plans(
    json_files: list[Path],
) -> tuple[list[dict[str, object]], list[str]]:
    valid_plans = []
    invalid_plans = []

    for file_path in json_files:
        try:
            plan = read_plan(file_path)
            valid_plans.append(plan)

        except ValueError as error:
            print(f"读取失败:{error}")
            invalid_plans.append(file_path.name)

    return valid_plans, invalid_plans


# 接收全部 JSON 文件路径；
# 汇总合法计划中的全部工具名称；
# 统计文件数、步骤数和工具调用次数；
# 返回汇总字典。


def summarize_tool_usage(
    json_files: list[Path],
) -> dict[str, object]:
    valid_plans, invalid_plans = collect_plans(json_files)

    all_tool_names = []

    for plan in valid_plans:
        tool_names = extract_tool_names(plan)
        all_tool_names.extend(tool_names)

    tool_counts = count_tool_usage(all_tool_names)

    summary = {
        "file_count": len(json_files),
        "step_count": len(all_tool_names),
        "tool_counts": tool_counts,
        "invalid_files": invalid_plans,
    }

    return summary


# 接收汇总字典和输出路径；
# 自动创建输出目录；
# 使用 json.dump() 将结果写入 JSON 文件。


def save_summary(
    summary: dict[str, object],
    output_path: str | Path,
) -> None:
    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(
            summary,
            file,
            ensure_ascii=False,
            indent=4,
        )


if __name__ == "__main__":
    data_folder = Path(
        "2026/python_project/practice/day04_data"
    )

    json_files = find_json_files(data_folder)

    for file_path in json_files:
        print(file_path.name)

    plan_path = Path(
        "2026/python_project/practice/day04_data/plan_a.json"
    )

    plan = read_plan(plan_path)

    print(type(plan))
    print(plan)

    tool_names = extract_tool_names(plan)
    print(tool_names)

    tool_count = count_tool_usage(tool_names)
    print(tool_count)

    valid_plans, invalid_plans = collect_plans(json_files)

    print("合法计划数量：", len(valid_plans))
    print("非法文件：", invalid_plans)

    summary = summarize_tool_usage(json_files)

    print("汇总结果：")
    print(summary)

    output_path = Path(
        "2026/python_project/practice/outputs/tool_summary.json"
    )

    save_summary(summary, output_path)

    print("结果已保存到：")
    print(output_path)