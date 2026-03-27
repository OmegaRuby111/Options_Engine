# Black-Scholes Option Pricing Model

## Overview
This project implements the Black-Scholes model for pricing European options. It focuses on applying mathematical finance concepts such as stochastic processes, Brownian motion, and partial differential equations to compute theoretical option prices.

## Features
- Pricing of European Call and Put options
- Implementation of Black-Scholes closed-form formula
- Computation of key parameters:
  - Spot price (S)
  - Strike price (K)
  - Risk-free rate (r)
  - Volatility (σ)
  - Time to maturity (T)
- Numerical evaluation using Python
- 
## Tech Stack
- Python
- NumPy
- SciPy (for normal distribution functions)
- Matplotlib (optional visualization)

## Model Description
The Black-Scholes formula assumes that the underlying asset follows a Geometric Brownian Motion and derives a closed-form solution for European option pricing.

Call Option Price:
C = S·N(d1) − K·e^(−rT)·N(d2)

Put Option Price:
P = K·e^(−rT)·N(−d2) − S·N(−d1)

Where:
- d1 and d2 are functions of S, K, r, σ, and T
- N(.) is the cumulative distribution function of the standard normal distribution

## 🚀 How to Run
1. Clone the repository
2. Open the notebook:
