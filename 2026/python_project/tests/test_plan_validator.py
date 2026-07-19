"""
任务 8：plan_validator 首批自动化测试
"""
from src.plan_validator import validate_plan

def test_validate_plan_returns_empty_list_for_valid_plan():
    # Arrange：准备一个结构完全合法的计划
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
    
def test_validate_plan_returns_all_discoverable_errors():
    # Arrange：准备一个同时包含多项错误的计划
    plan = {
        "steps": [
            "WeatherTool",
            {
                "tool_name": "",
                "args": [],
            },
            {
                "args": {},
            },
            {
                "tool_name": "IrrigationRuleTool",
            },
        ]
    }

    expected_errors = [
        "steps[0] 必须是字典",
        "steps[1].tool_name 必须是非空字符串",
        "steps[1].args 必须是字典",
        "steps[2] 缺少 tool_name",
        "steps[3] 缺少 args",
    ]

    # Act：校验计划
    actual_errors = validate_plan(plan)

    # Assert：必须一次返回全部可发现错误
    assert actual_errors == expected_errors
    
def test_validate_plan_returns_all_discoverable_errors():
    # Arrange：准备一个同时包含多项错误的计划
    plan = {
        "steps": [
            "WeatherTool",
            {
                "tool_name": "",
                "args": [],
            },
            {
                "args": {},
            },
            {
                "tool_name": "IrrigationRuleTool",
            },
        ]
    }

    expected_errors = [
        "steps[0] 必须是字典",
        "steps[1].tool_name 必须是非空字符串",
        "steps[1].args 必须是字典",
        "steps[2] 缺少 tool_name",
        "steps[3] 缺少 args",
    ]

    # Act：调用校验函数
    actual_errors = validate_plan(plan)

    # Assert：实际结果必须与全部预期错误一致
    assert actual_errors == expected_errors