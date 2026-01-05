"""
sample_data.py
Synthetic baseline parameters for scenario modeling demo.
"""

def sample_params():
    return {
        'base_price': 100.0,
        'base_demand': 1000.0,
        'variable_cost': 40.0,
        'fixed_cost': 20000.0,
        'price_change_pct': 0.0,
        'price_volatility': 0.05,
        'demand_shock_mu': 1.0,
        'demand_shock_sigma': 0.15,
        'regulatory_cost_pct': 0.05,
        'regulatory_cost_volatility': 0.02,
        'price_elasticity': 0.8,
        'discount_rate': 0.08,
        'horizon_periods': 12
    }
