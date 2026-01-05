"""
modeling.py
Core outcome modeling logic for Scenario Simulation Node.
Handles:
- demand modeling
- cost modeling
- Monte Carlo scenario simulation
"""

import numpy as np
import pandas as pd


def demand_model(base_demand, price_change_pct, elasticity, demand_shock):
    """Simple linear elasticity demand model with multiplicative demand shock."""
    demand = base_demand * (1 - elasticity * price_change_pct)
    demand = max(demand, 0)
    return demand * demand_shock


def cost_model(base_cost, regulatory_cost_pct, fixed_cost):
    """Total cost = variable cost * (1 + reg %) + fixed cost."""
    return base_cost * (1 + regulatory_cost_pct) + fixed_cost


def run_scenario(params, n_runs=1000, seed=None):
    """Run stochastic simulation for a single scenario."""
    rng = np.random.default_rng(seed)
    results = []

    for _ in range(n_runs):
        price_change = rng.normal(params['price_change_pct'], params['price_volatility'])
        demand_shock = max(0.0, rng.normal(params['demand_shock_mu'], params['demand_shock_sigma']))
        reg_cost_pct = max(0.0, rng.normal(params['regulatory_cost_pct'], params['regulatory_cost_volatility']))

        demand = demand_model(
            params['base_demand'], price_change, params['price_elasticity'], demand_shock
        )

        unit_rev = params['base_price'] * (1 + price_change)
        revenue = demand * unit_rev
        total_cost = cost_model(demand * params['variable_cost'], reg_cost_pct, params['fixed_cost'])
        profit = revenue - total_cost

        # NPV of flat profit stream
        r = params['discount_rate']
        t = params['horizon_periods']
        npv = profit * (1 - (1 + r) ** -t) / r if r > 0 else profit * t

        results.append({
            'price_change': price_change,
            'demand_shock': demand_shock,
            'regulatory_cost_pct': reg_cost_pct,
            'demand': demand,
            'unit_revenue': unit_rev,
            'revenue': revenue,
            'total_cost': total_cost,
            'profit': profit,
            'npv_equiv': npv
        })

    return pd.DataFrame(results)
