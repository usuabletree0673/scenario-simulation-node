"""
prompt_gen.py
Generates scenario prompts for human use or LLM input.
"""

def construct_prompt(project_name, params, scenario_label):
    """Creates a natural-language summary of inputs for documentation or LLM use."""
    lines = [
        f"Project: {project_name}",
        f"Scenario: {scenario_label}",
        "Inputs:"
    ]
    for k, v in params.items():
        lines.append(f" - {k}: {v}")
    return "\n".join(lines)
