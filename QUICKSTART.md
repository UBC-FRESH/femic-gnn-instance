# FEMIC GNN Instance Quickstart

1. Read `AGENTS.md` and `ROADMAP.md`.
2. Create and activate a local environment:
   `python -m venv .venv && . .venv/bin/activate`
3. Install the dev requirements:
   `python -m pip install -r requirements-dev.txt`
4. Install the pre-commit hooks:
   `pre-commit install`
5. Run the green dashboard:
   `python scripts/dashboard.py`
6. Run the workflow validator:
   `python scripts/check_workflow.py`
7. Build the prototype (requires the TSA 46/47 base instances):
   `pipeline/build_gnn_model.sh`
8. Serve the local UI:
   `./serve_gnn_calibrated.sh`

The model is a prototype. The boundary is the proposed GNN Statement of Intent
polygon, and the THLB and AAC are derived, non-legal values. See `docs/` and
`notes/reference/` before using an output.
