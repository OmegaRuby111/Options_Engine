import numpy as np
import matplotlib.pyplot as plt 

def simulate_paths(S,r,sigma,n,days):
    z=np.random.standard_normal((n,days))
    T=days/365
    dt=T/days
    drift=(r-0.5*sigma**2)*dt
    diffusion=sigma*np.sqrt(dt)*z
    factor=np.exp(drift+diffusion)
    S_col=np.full((n,1),S)
    paths=np.hstack([S_col,S*np.cumprod(factor,axis=1)])
    time_steps=np.linspace(0,T,days+1)
    return paths,time_steps

def plot_paths(K,paths,time_steps,n_display=50):
    fig, ax = plt.subplots(figsize=(10, 6))
    for i in range(n_display):
        ax.plot(time_steps, paths[i], alpha=0.3, linewidth=0.8)
    ax.axhline(y=K, color='red', linestyle='--', linewidth=1.5, label='Strike Price')
    ax.set_xlabel('Time (Years)')
    ax.set_ylabel('Stock Price')
    ax.set_title('Simulated Price Paths')
    ax.legend()
    return fig

def european_mc_call(K,n,r,days,paths):
    #variables used are paths,K,r,T,n
    T=days/365
    final_prices=paths[:,-1]
    call_payoffs=np.maximum(final_prices-K,0)
    avg_call_payoff=np.mean(call_payoffs)
    discounted_avg_call_payoff=np.exp(-r*T)*avg_call_payoff
    standard_call_error=(np.std(call_payoffs)/np.sqrt(n))*(np.exp(-r*T))
    return discounted_avg_call_payoff,standard_call_error

def european_mc_put(K,n,r,days,paths):
    T=days/365
    final_prices=paths[:,-1]
    put_payoffs=np.maximum(K-final_prices,0)
    avg_put_payoff=np.mean(put_payoffs)
    discounted_avg_put_payoff=np.exp(-r*T)*avg_put_payoff
    standard_put_error=(np.std(put_payoffs)/np.sqrt(n))*(np.exp(-r*T))
    return discounted_avg_put_payoff,standard_put_error

def asian_mc_call(K,n,r,days,paths):
    T=days/365
    avg_prices=np.mean(paths[:,1:],axis=1)
    asian_call_payoff=np.maximum(avg_prices-K,0)
    avg_call_payoff=np.mean(asian_call_payoff)
    discounted_call_payoff=np.exp(-r*T)*avg_call_payoff
    standard_call_error=(np.std(asian_call_payoff)/np.sqrt(n))*(np.exp(-r*T))
    return discounted_call_payoff,standard_call_error

def asian_mc_put(K,n,r,days,paths):
    T=days/365
    avg_prices=np.mean(paths[:,1:],axis=1)
    asian_put_payoff=np.maximum(K-avg_prices,0)
    avg_put_payoff=np.mean(asian_put_payoff)
    discounted_put_payoff=np.exp(-r*T)*avg_put_payoff
    standard_put_error=(np.std(asian_put_payoff)/np.sqrt(n))*(np.exp(-r*T))
    return discounted_put_payoff,standard_put_error