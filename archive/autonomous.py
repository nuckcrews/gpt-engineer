from gptop.operator import Operator
from ..engineer.utils import announce


def main():
    operator = Operator("engineer")

    goal = """
    You are a CLI bot that can perform git operations and read and write files.
    Go through the entire `gpt-operator` repository and add make improvements
    to the non-code files.
    Do not commit changes until all files have been processed.
    You will need to clone the repo to access it.
    Once complete, exit the current task.
    """.replace("\n", " ")

    config = {
        "Git Repo": "git@github.com:ncrews35/gpt-operator.git",
        "Your branch": "development",
        "goals": [
            "Improved readability and clarity",
            "Spell corrections"
        ]
    }

    count = 1
    completed_steps = []
    step_results = []
    while True:
        step = operator.step(goal, completed_steps=completed_steps)
        announce(step, prefix="Step: ")
        goal_step = f"Goal: {goal}; " + f"Config: {config}; " + f"Next Step: {step}; " + f"Completed Steps: {completed_steps};"
        found_operations = operator.find(step)
        announce(len(found_operations), prefix="Found Operations: ")
        operations = operator.pick(step, operations=found_operations)
        if not operations:
            step_results.append({
                "step": f"{count}. " + step,
                "result": "Complete"
            })

            completed_steps.append(f"{count}. " + step)
            continue

        announce([op.name for op in operations], prefix="Operations: ")

        op_results = []
        for operation in operations:
            op_input = operator.prepare(goal_step, operation=operation)
            announce(op_input, prefix="Operation Input: ")
            exec_result = operator.execute(operation=operation, input=op_input)
            announce(exec_result, prefix="Operation result: ")
            op_results.append({
                "operation": operation.__dict__,
                "input_data": op_input,
                "result": exec_result
            })

        step_results.append({
            "step": f"{count}. " + step,
            "result": op_results
        })

        completed_steps.append(f"{count}. " + step)
        count += 1