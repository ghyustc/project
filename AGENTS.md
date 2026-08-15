# AGENTS.md

## First step
The repository contains `enterprise_quant_codex_seed.zip`, which is the complete tested seed project. Before making product changes:
1. Extract the archive.
2. Move the contents of `enterprise_quant_demo/` into the repository root, preserving `.env.example` and `.gitignore`.
3. Remove the extracted wrapper directory and the zip after the source files are committed.
4. Run `python -m pip install -e ".[dev]"` and `pytest` to establish the baseline.

## Mission
Turn this repository into a polished, paper-trading-first quantitative research application that a non-technical user can run and understand without manually calling APIs.

## Safety boundary
- Default to backtesting and paper trading only.
- Do not enable live-money trading by default.
- Never hard-code API keys, exchange secrets, wallet seeds, or credentials.
- Any future live broker/exchange adapter must be disabled unless explicitly configured and must preserve pre-trade risk checks and the global kill switch.
- Do not market sample results as expected returns or investment advice.

## Product priorities
1. A simple local web UI is the primary user experience. Swagger remains a developer tool.
2. One-command startup for macOS should be supported, ideally `make dev` or `docker compose up --build`.
3. The user should be able to choose a dataset, edit strategy/risk parameters, start a backtest, and see results without using the terminal after startup.
4. Show an equity curve, drawdown curve, headline metrics, orders/fills, risk events, and run history.
5. Keep the existing event-ordering invariant: a signal formed on bar N may fill no earlier than bar N+1.
6. Preserve deterministic/reproducible runs and auditable persisted records.

## Engineering rules
- Python >= 3.12.
- Keep FastAPI and the existing domain/backtest/risk separation unless there is a strong reason to refactor it.
- Favor small, typed modules and explicit domain objects over large framework-heavy abstractions.
- Add tests for every behavior change. Run `pytest` before considering a task complete.
- Do not silently weaken existing risk limits or path traversal protections.
- Avoid introducing a database/network service solely for local development unless it clearly improves the product. SQLite is acceptable for v1.
- Avoid future-data leakage in all strategies and indicators.
- If adding third-party market data, isolate it behind an adapter and retain CSV/offline operation.

## Baseline commands
```bash
python -m pip install -e ".[dev]"
pytest
python -m quant_platform.cli backtest --csv data/sample_btcusd.csv
python -m quant_platform.cli serve
```

## Acceptance checks
- `pytest` passes.
- App starts from a clean checkout using documented commands.
- A non-technical user can run the bundled sample backtest from the web UI.
- The sample run can be reopened from history and its metrics/equity/orders/fills are visible.
- Risk halt state is visible in the UI.
- No secrets are committed.
