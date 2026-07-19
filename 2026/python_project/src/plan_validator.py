"""
任务 7：输入校验

本模块负责校验计划结构。
不读取文件，不写入文件，不修改输入对象。
"""


def validate_plan(plan: object) -> list[str]:
    errors: list[str] = []

    # 检查计划顶层是否为字典
    if not isinstance(plan, dict):
        errors.append("计划顶层必须是字典")
        return errors

    # 检查 steps 是否存在
    if "steps" not in plan:
        errors.append("缺少 steps")
        return errors

    # 检查 steps 是否为列表
    steps = plan["steps"]

    if not isinstance(steps, list):
        errors.append("steps 必须是列表")
        return errors

    # 遍历每个步骤
    for index, step in enumerate(steps):

        # 检查步骤是否为字典
        if not isinstance(step, dict):
            errors.append(
                f"steps[{index}] 必须是字典"
            )
            continue

        # 检查 tool_name 是否存在
        if "tool_name" not in step:
            errors.append(
                f"steps[{index}] 缺少 tool_name"
            )
        else:
            tool_name = step["tool_name"]

            # 检查 tool_name 是否为非空字符串
            if (
                not isinstance(tool_name, str)
                or tool_name.strip() == ""
            ):
                errors.append(
                    f"steps[{index}].tool_name "
                    "必须是非空字符串"
                )

        # 检查 args 是否存在
        if "args" not in step:
            errors.append(
                f"steps[{index}] 缺少 args"
            )

        # 检查 args 是否为字典
        elif not isinstance(step["args"], dict):
            errors.append(
                f"steps[{index}].args 必须是字典"
            )

    return errors