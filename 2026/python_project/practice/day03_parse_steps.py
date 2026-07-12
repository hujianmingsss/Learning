plan = {
    "steps": [
        {
            "step_id": 1,
            "tool_name": "WeatherTool",
            "args": {"days": 7}
        },
        {
            "step_id": 2,
            "tool_name": "ExplanationTool",
            "depends_on": [1],
            "output_ref": "$answer"
        }
    ]
}

# 要求每个整理后的步骤都包含：

# step_id
# tool_name
# args
# depends_on
# output_ref

def parse_steps(plan):
    parsed_steps = []

    for step in plan["steps"]:
        parsed_step = {
            "step_id": step["step_id"],
            "tool_name": step["tool_name"],
            "args": step.get("args", {}),
            "depends_on": step.get("depends_on", []),
            "output_ref": step.get("output_ref")
        }

        parsed_steps.append(parsed_step)

    return parsed_steps