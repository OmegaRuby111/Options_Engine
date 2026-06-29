import numpy as np
from scipy.stats import norm

def black_scholes(r,S,K,days,sigma,option_type):
    "Calculate BS Option price for a call/put option"
    T=days/365
    d1=(np.log(S/K)+(r+sigma**2/2)*T)/(sigma*np.sqrt(T))
    d2=d1-sigma*np.sqrt(T)
    
    if option_type=="C":
        return S*norm.cdf(d1,0,1)-K*np.exp(-r*T)*norm.cdf(d2,0,1)
    elif option_type=="P":
        return K*np.exp(-r*T)*norm.cdf(-d2,0,1)-S*norm.cdf(-d1,0,1)
    else:
        raise ValueError(f"Invalid option_type '{option_type}'. Use 'C' or 'P'.")

def greeks(r,S,K,days,sigma):
    T=days/365
    d1=(np.log(S/K)+(r+sigma**2/2)*T)/(sigma*np.sqrt(T))
    d2=d1-sigma*np.sqrt(T)
    #Delta Call
    delta_call=norm.cdf(d1,0,1)
    delta_put=norm.cdf(-d1,0,1)*(-1)

    #Gamma for put and call
    N=1/np.sqrt(np.pi*2)*np.exp(-0.5*d1**2)
    gamma=(N)/(sigma*S*np.sqrt(T))

    #rho
    #cleaner_rho_put=-K*T*np.exp(-r*T)*norm.cdf(-d2)
    #cleaner_rho_call=K*T*np.exp(-r*T)*norm.cdf(d2)
    rho_call=(K*norm.cdf(d2,0,1)*T)/(np.exp(r*T))
    rho_put=(K*norm.cdf(-d2,0,1)*T)/(-(np.exp(r*T)))

    #vega
    vega=np.sqrt(T)*S*N

    #theta
    c1=-((0.5)/np.sqrt(T))*sigma*S
    c2=(r*K)/(np.exp(r*T))
    theta_call=(c1*N)-(c2*norm.cdf(d2))
    theta_put=(c1*N)+(c2*norm.cdf(-d2))
    return delta_call, delta_put, gamma, rho_call, rho_put, vega, theta_call, theta_put