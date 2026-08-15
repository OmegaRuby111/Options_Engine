# Options Pricing Engine
A multi-model options pricing engine built with Python and Streamlit.
## Live Demo
[Launch App](https://optionsengine-drnfgn7u4uphtjzt7az4x7.streamlit.app/)
## Models Implemented
- **Black-Scholes** — Analytical pricing for European call/put options with full Greeks (Delta, Gamma, Vega, Theta, Rho)
- **European Monte Carlo** — GBM path simulation with discounted payoff averaging and standard error estimation
- **Asian Monte Carlo** — Path-dependent pricing using arithmetic average price over the simulation period
- **American Binomial Tree** — CRR binomial tree pricing with early exercise, full Greeks (Delta/Gamma/Theta read directly from tree nodes, Vega/Rho via bump-and-reprice), and a convergence plot comparing tree price across increasing step counts (N) against the Black-Scholes reference line — visualizing the early-exercise premium on puts
## Tech Stack
Python, NumPy, SciPy, Matplotlib, Streamlit
## Project Structure
app2.py                # Streamlit frontend
blackscholes.py         # Black-Scholes pricing and Greeks
monte_carlo.py           # Path simulation, European and Asian MC pricing
bt_option_pricing.py      # Binomial tree pricing, Greeks, and convergence plotting
## Key Concepts
- Geometric Brownian Motion for path simulation
- Risk-neutral pricing and discounted expected payoffs
- Monte Carlo convergence to Black-Scholes for European options
- Path-dependency in exotic option pricing
- Early exercise and the American vs. European premium
- Binomial tree convergence to Black-Scholes (calls converge fully; puts converge to a level above BS, reflecting the value of early exercise)
