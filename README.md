# Scenario Simulation Node

**AI-supported tool for simulating market/policy uncertainty and generating structured decision memos.**

---

## Overview
This project extends the logic of an AI-Supported Decision-Making capstone. It provides a lightweight simulation node that models business outcomes under uncertainty using Monte Carlo methods, with embedded risk framing and memo generation.

---

## For Recruiters / Strategists
This project demonstrates:
- Strategic scenario modeling under ambiguity
- AI interpretability in decision workflows
- Real-time simulation logic with parameter tuning
- Decision memo generation (text export, structured framing)
- Modular architecture, extensible to LLM/NLP or policy simulators

Use cases include:
- Entry timing assessments
- Policy risk response modeling
- Pricing elasticity tradeoffs

---

##  For Engineers / Analysts
**Stack**: `Python`, `Streamlit`, `Pandas`, `NumPy`, `Matplotlib`

**Core Architecture**
```
 scenario_sim_node/
├── app/
│   ├── modeling.py        # Demand, cost, NPV models + simulation
│   ├── formatter.py       # Statistical summary + memo writer
│   ├── runner.py          # Executes multiple scenario runs
│   ├── ui.py              # Streamlit interface
│   ├── prompt_gen.py      # Scenario prompt generator
│   └── sample_data.py     # Default parameters
├── streamlit_app.py       # Entry point
├── .gitignore
└── README.md
```

---

## Getting Started
### Install dependencies
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run the app
```bash
PYTHONPATH=. streamlit run streamlit_app.py
```

### Requirements
```
streamlit
pandas
numpy
matplotlib
```

---

## Future Extensions
- [ ] LLM-based memo polishing
- [ ] Branching scenario trees
- [ ] Live data input hooks (optional CSV/JSON upload)

---

## 📄 License
MIT License (or add yours here)
