from day04_batch_plan_analyzer import (
    read_plan,
    validate_plan,
)
import pytest

def test_validate_plan_accepts_valid_plan():
    plan = {
        "steps": [
            {
                "tool_name": "WeatherTool",
                "args": {},
            }
        ]
    }

    errors = validate_plan(plan)

    assert errors == []


def test_validate_plan_rejects_missing_steps():
    plan = {
        "name": "demo",
    }

    errors = validate_plan(plan)

    assert errors == ["缺少 steps 字段"]
    
def test_read_plan_raises_for_missing_file(tmp_path):
    file_path = tmp_path / "not_exists.json" #创建一个pytest临时json

    with pytest.raises(FileNotFoundError):
        read_plan(file_path)
        
def test_read_plan_raises_for_invalid_json(tmp_path):
    file_path = tmp_path / "invalid.json"

    file_path.write_text(
        '{"steps":',
        encoding="utf-8",
    )

    # 使用 pytest.raises 检查 read_plan(file_path)