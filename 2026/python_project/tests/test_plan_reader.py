import json
import pytest
from src.plan_reader import read_plan

def test_read_plan_raises_file_not_found_error_with_path(tmp_path):
    #构造一个确定不存在的文件
    missing_path = tmp_path/ "missing_plan.json"
    #调用函数并捕获异常
    with pytest.raises(FileNotFoundError) as error_info:
        read_plan(missing_path)
    #异常信息必须包含出错路径
    assert str(missing_path) in str(error_info.value)
    
def test_read_plan_raises_value_error_for_invalid_json(tmp_path):
    # Arrange：创建一个存在语法错误的 JSON 文件
    invalid_json_path = tmp_path / "invalid_plan.json"

    invalid_json_path.write_text(
        '{"steps": [}',
        encoding="utf-8",
    )

    # Act + Assert：调用函数并捕获 ValueError
    with pytest.raises(ValueError) as error_info:
        read_plan(invalid_json_path)

    # Assert：错误信息包含文件路径
    assert str(invalid_json_path) in str(error_info.value)

    # Assert：保留原始 JSONDecodeError 异常上下文
    assert isinstance(
        error_info.value.__cause__,
        json.JSONDecodeError,
    )
    
def test_read_plan_rejects_non_dict_top_level(tmp_path):
    # Arrange：创建顶层为列表的合法 JSON 文件
    invalid_structure_path = tmp_path / "list_plan.json"

    invalid_structure_path.write_text(
        '["WeatherTool", "SoilMoistureTool"]',
        encoding="utf-8",
    )

    # Act + Assert：顶层不是字典时必须抛出 ValueError
    with pytest.raises(ValueError) as error_info:
        read_plan(invalid_structure_path)

    # Assert：异常信息包含文件路径
    assert str(invalid_structure_path) in str(error_info.value)

    # Assert：异常信息指出实际类型为 list
    assert "list" in str(error_info.value)
    
def test_read_plan_returns_valid_json_dict(tmp_path):
    # Arrange：准备合法计划和临时 JSON 文件
    expected_plan = {
        "steps": [
            {
                "tool_name": "WeatherTool",
                "args": {
                    "location": "昌吉",
                },
            }
        ]
    }

    plan_path = tmp_path / "valid_plan.json"

    plan_path.write_text(
        json.dumps(expected_plan, ensure_ascii=False),
        encoding="utf-8",
    )

    # Act：读取临时 JSON 文件
    actual_plan = read_plan(plan_path)

    # Assert：读取结果必须与写入内容一致
    assert actual_plan == expected_plan