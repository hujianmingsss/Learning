import json
from pathlib import Path


# 路径转换
# → 打开文件
# → 解析 JSON
# → 判断顶层是不是字典
# → 返回字典
def read_plan(path: str | Path) -> dict[str, object]:
    file_path = Path(path)

    try:
        with file_path.open("r", encoding="utf-8") as file:
            json_data = json.load(file)

    except FileNotFoundError as error:
        raise FileNotFoundError(
            f"文件不存在：{file_path}；原因：{error}"
        ) from error

    except json.JSONDecodeError as error:
        raise ValueError(
            f"JSON解析失败：{file_path}；原因：{error}"
        ) from error

    if not isinstance(json_data, dict):
        raise ValueError(
            f"JSON顶层必须是字典：{file_path}；"
            f"实际类型：{type(json_data).__name__}"
        )

    return json_data