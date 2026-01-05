"""
ui.py
Streamlit interface wrapper for Scenario Simulation Node.
Handles sidebar controls, scenario configuration, and result visualization.
"""

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from app.runner import run_all_scenarios
from app.formatter import generate_decision_memo
from app.sample_data import sample_params


def render_ui():
    st.set_page_config(page_title="Scenario Simulation Node", layout="wide")
    st.title("Scenario Simulation Node — Builder Mode")
    st.markdown("Simulate market/policy uncertainty and generate structured decision memos.")

    with st.sidebar:
        st.header("Controls")
        project_name = st.text_input("Project Name", "Scenario Simulation Node")
        n_runs = st.slider("Monte Carlo runs", 200, 5000, 1000, step=200)
        seed = st.number_input("RNG Seed (0 = random)", min_value=0, value=0)

        st.header("Baseline Parameters")
        defaults = sample_params()
        base_price = st.number_input("Base Price", value=defaults['base_price'])
        base_demand = st.number_input("Base Demand", value=defaults['base_demand'])
        var_cost = st.number_input("Variable Cost", value=defaults['variable_cost'])
        fixed_cost = st.number_input("Fixed Cost", value=defaults['fixed_cost'])
        price_elasticity = st.slider("Price Elasticity", 0.0, 3.0, defaults['price_elasticity'], step=0.05)
        discount_rate = st.slider("Discount Rate", 0.0, 0.5, defaults['discount_rate'], step=0.01)
        horizon = st.slider("Horizon (Periods)", 1, 60, defaults['horizon_periods'])

        st.header("Scenarios")
        opt_mu = st.number_input("Optimistic Demand Shock (mu)", value=1.10)
        opt_price = st.number_input("Optimistic Price Change (pct)", value=-0.05)
        opt_reg = st.number_input("Optimistic Reg Cost Pct", value=0.03)

        base_mu = st.number_input("Baseline Demand Shock (mu)", value=1.0)
        base_price_ch = st.number_input("Baseline Price Change (pct)", value=0.00)
        base_reg = st.number_input("Baseline Reg Cost Pct", value=0.05)

        pes_mu = st.number_input("Pessimistic Demand Shock (mu)", value=0.80)
        pes_price = st.number_input("Pessimistic Price Change (pct)", value=0.05)
        pes_reg = st.number_input("Pessimistic Reg Cost Pct", value=0.10)

        run_flag = st.button("Run Simulations")

    if run_flag:
        template = {
            'base_price': base_price,
            'base_demand': base_demand,
            'variable_cost': var_cost,
            'fixed_cost': fixed_cost,
            'price_elasticity': price_elasticity,
            'discount_rate': discount_rate,
            'horizon_periods': horizon,
            'price_volatility': 0.06,
            'demand_shock_sigma': 0.18,
            'regulatory_cost_volatility': 0.03
        }

        scenarios = {
            'Optimistic': {**template, 'price_change_pct': opt_price, 'demand_shock_mu': opt_mu, 'regulatory_cost_pct': opt_reg},
            'Baseline':   {**template, 'price_change_pct': base_price_ch, 'demand_shock_mu': base_mu, 'regulatory_cost_pct': base_reg},
            'Pessimistic':{**template, 'price_change_pct': pes_price, 'demand_shock_mu': pes_mu, 'regulatory_cost_pct': pes_reg},
        }

        outputs, summaries, _ = run_all_scenarios(project_name, scenarios, n_runs=n_runs, seed=(None if seed == 0 else int(seed)))

        st.subheader("Summary Table")
        summary_table = pd.DataFrame([
            {'Scenario': k, 'Mean Profit': v['profit']['mean'], 'Mean NPV': v['npv_equiv']['mean']}
            for k, v in summaries.items()
        ])
        st.table(summary_table.set_index("Scenario"))

        st.subheader("Profit Distribution")
        fig, ax = plt.subplots()
        for label, df in outputs.items():
            ax.hist(df['profit'], bins=50, alpha=0.5, label=label)
        ax.set_xlabel("Profit per period")
        ax.set_ylabel("Frequency")
        ax.legend()
        st.pyplot(fig)

        chosen = st.selectbox("Recommended Scenario", list(scenarios.keys()))
        memo = generate_decision_memo(project_name, summaries, chosen)

        st.subheader("Decision Memo")
        st.code(memo)

        csv_data = pd.concat([df.assign(scenario=k) for k, df in outputs.items()])
        st.download_button("Download CSV", csv_data.to_csv(index=False), file_name="scenario_results.csv")
        st.download_button("Download Memo", memo, file_name="decision_memo.txt")

    else:
        st.info("Use the sidebar to configure scenarios and click 'Run Simulations'.")
