# Codex task: finish the first usable product version

Implement a user-friendly v1 on top of the existing tested quant engine. Work autonomously, run the test suite frequently, and leave the repository in a runnable state.

## Goal
A user who does not understand Python or Swagger should be able to clone/open the project, start it with one documented command, use a browser to run a paper/backtest workflow, and understand the result.

## Required work

### 1. Web dashboard
Add a clean local dashboard served by the application. It may use a lightweight frontend approach; avoid unnecessary build complexity.

The dashboard must provide:
- system health/status;
- dataset selection, with the bundled sample preselected;
- form fields for initial cash, fast/slow windows, allocation, fee/slippage, and risk limits;
- a clear “Run backtest” action;
- loading/error/success states;
- headline metrics: final equity, total return, max drawdown, Sharpe, realized PnL, fees, fills, win rate and profit factor;
- equity curve and drawdown visualization;
- tables for orders, fills and risk events;
- run history and ability to reopen a past run;
- visible kill-switch/risk-halt status.

### 2. Friendly startup
Provide one primary startup path for macOS/Linux. Prefer one of:
- `make dev`; or
- `python -m quant_platform.cli app`; or
- a documented `docker compose up --build` path.

The primary command should start both API and UI. README instructions should not require the user to manually invoke Swagger endpoints.

### 3. Real historical data adapter, offline-safe
Add an optional adapter/command to download public OHLCV historical market data from a reputable exchange or market-data source without credentials where possible. Keep it isolated from the backtest engine.
- Validate and normalize into the existing CSV schema.
- Make failures explicit.
- Keep the bundled synthetic data and all tests independent of network access.
- Do not add live order execution.

### 4. Strategy structure
Keep the moving-average strategy as a demo, but define a clean strategy interface so additional strategies can be added without editing the backtest engine. Add at least one additional simple research strategy for demonstration, with tests and no look-ahead bias.

### 5. Reliability and observability
- Preserve request IDs and structured logs.
- Keep path traversal protections.
- Keep idempotent order behavior and existing risk behavior.
- Add useful validation messages for invalid parameter combinations such as fast window >= slow window.
- Ensure persistence directories are created safely.

### 6. CI and quality
Add GitHub Actions CI for Python 3.12+ that installs dependencies and runs tests. Add a linter/type-check step if it can be introduced without destabilizing the project.

### 7. Documentation
Rewrite README around the non-technical workflow first:
1. install/start;
2. open dashboard;
3. run sample backtest;
4. interpret metrics;
5. optional advanced/API usage.

Explicitly state that synthetic/sample performance is not indicative of future returns and live trading is disabled.

## Do not do
- Do not connect or trade a real account.
- Do not store exchange keys.
- Do not bypass exchange, platform, geographic, or compliance restrictions.
- Do not remove tests just to make CI green.
- Do not claim profitability.

## Definition of done
- Clean checkout -> documented install -> one startup command -> browser dashboard works.
- Sample backtest completes from the dashboard.
- Results, charts, orders/fills and history render correctly.
- Existing tests pass and new coverage is added.
- CI workflow is included.
- README is accurate and concise.
