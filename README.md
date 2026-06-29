# Options Pricing Engine

A multi-model options pricing engine built with Python and Streamlit.

## Live Demo
[Launch App](https://optionsengine-drnfgn7u4uphtjzt7az4x7.streamlit.app/)

## Models Implemented
- **Black-Scholes** — Analytical pricing for European call/put options with full Greeks (Delta, Gamma, Vega, Theta, Rho)
- **European Monte Carlo** — GBM path simulation with discounted payoff averaging and standard error estimation
- **Asian Monte Carlo** — Path-dependent pricing using arithmetic average price over the simulation period

## Tech Stack
Python, NumPy, SciPy, Matplotlib, Streamlit

## Project Structure
app2.py           # Streamlit frontend

blackscholes.py   # Black-Scholes pricing and Greeks

monte_carlo.py    # Path simulation, European and Asian MC pricing

## Key Concepts
- Geometric Brownian Motion for path simulation
- Risk-neutral pricing and discounted expected payoffs
- Monte Carlo convergence to Black-Scholes for European options
- Path-dependency in exotic option pricing
