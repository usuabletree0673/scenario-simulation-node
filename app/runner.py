"""
runner.py
Executes simulation scenarios using modeling and formatting modules.
Coordinates parameter setup, scenario runs, and result summaries.
"""

from app.modeling import run_scenario
from app.formatter import summarize_sim
from app.prompt_gen import construct_prompt


def run_all_scenarios(project_name, scenario_params_dict, n_runs=1000, seed=None):
    """
    Runs all scenarios and returns:
    - scenario_outputs: {label: DataFrame}
    - scenario_summaries: {label: dict of stats}
    - scenario_prompts: {label: str}
    """
    outputs = {}
    summaries = {}
    prompts = {}

    for label, params in scenario_params_dict.items():
        prompt = construct_prompt(project_name, params, label)
        df = run_scenario(params, n_runs=n_runs, seed=seed)
        summ = summarize_sim(df)

        outputs[label] = df
        summaries[label] = summ
        prompts[label] = prompt

    return outputs, summaries, prompts
