"""
formatter.py
Generates structured summaries and decision memos for Scenario Simulation Node.
"""

from datetime import datetime


def summarize_sim(df):
    """Compute mean, median, p10, p90 for key metrics."""
    stats = {}
    metrics = ['revenue', 'profit', 'npv_equiv', 'demand']
    for m in metrics:
        stats[m] = {
            'mean': float(df[m].mean()),
            'median': float(df[m].median()),
            'p10': float(df[m].quantile(0.1)),
            'p90': float(df[m].quantile(0.9))
        }
    return stats


def generate_decision_memo(project_name, scenario_summaries, chosen_option_label):
    """Plain-text decision memo summarizing outcomes and framing risks."""
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
    lines = [
        f"Decision Memo — {project_name}",
        f"Generated: {now}",
        "", 
        "Executive Recommendation:",
        f" - Recommended option: {chosen_option_label}",
        "",
        "Scenario Summaries (key statistics):"
    ]

    for label, s in scenario_summaries.items():
        lines.append(f"\nScenario: {label}")
        lines.append(f" - Expected profit (mean): {s['profit']['mean']:.2f}")
        lines.append(f" - 10th / 90th percentile NPV-equivalent: {s['npv_equiv']['p10']:.2f} / {s['npv_equiv']['p90']:.2f}")
        lines.append(f" - Median revenue: {s['revenue']['median']:.2f}")

    lines.append("\nRisk framing:")
    lines.append(" - Upside: low reg costs, strong demand shocks, lower price elasticity.")
    lines.append(" - Downside: demand collapse, cost overruns, adverse price response.")
    lines.append(" - Uncertainties: policy shifts, early sales velocity, competitor moves.")

    lines.append("\nDecision triggers:")
    lines.append(" - If conversion >120% of base: accelerate.")
    lines.append(" - If reg costs exceed p90: delay or mitigate.")

    return "\n".join(lines)
