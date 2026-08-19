import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def binomial_tree_option_pricing(S,K,T,r,sigma,q,N):
    if S <= 0:
        raise ValueError(f"S must be positive, got {S}")
    if K <= 0:
        raise ValueError(f"K must be positive, got {K}")
    if T <= 0:
        raise ValueError(f"T must be positive, got {T}")
    if sigma <= 0:
        raise ValueError(f"sigma must be positive, got {sigma}")
    if not isinstance(N, int) or N < 1:
        raise ValueError(f"N must be a positive integer, got {N}")
    if r < -1 or r > 1:
        raise ValueError(f"r looks out of realistic range (-100% to 100%), got {r}")
    if sigma > 5:
        raise ValueError(f"sigma looks out of realistic range (>500% annualized vol), got {sigma}")
    if q < 0 or q > 1:
        raise ValueError(f"q must be between 0 and 1, got {q}")

    dt=T/N
    u=np.exp(sigma*np.sqrt(dt))
    d=1/u
    p=(np.exp((r-q)*dt)-d)/(u-d)

    j=np.arange(0,N+1)
    S_T=S*u**j*d**(N-j)

    put_payoffs=np.maximum(K-S_T,0)
    call_payoffs=np.maximum(S_T-K,0)

    call_history=[]
    put_history=[]
    S_history=[]

    disc=np.exp(-r*dt)
    V_put=put_payoffs
    V_call=call_payoffs

    S_history.append(S_T)
    put_history.append(put_payoffs)
    call_history.append(call_payoffs)

    for i in range(N-1,-1,-1):
        j=np.arange(i+1)
        S_i=S*u**j*d**(i-j)
        

        continuation_put=disc*(p*V_put[1:]+(1-p)*V_put[:-1])
        exercise_put=np.maximum(K-S_i,0)
        V_put=np.maximum(continuation_put,exercise_put)
        

        continuation_call=disc*(p*V_call[1:]+(1-p)*V_call[:-1])
        exercise_call=np.maximum(S_i-K,0)
        V_call=np.maximum(continuation_call,exercise_call)
        S_history.append(S_i)
        put_history.append(V_put)
        call_history.append(V_call)

    return{
        'put_price':float(V_put[0]),
        'call_price':float(V_call[0]),
        'put_tree':put_history,
        'call_tree':call_history,
        'asset_tree':S_history
    }

def compute_greeks(result,S,K,T,r,sigma,q,N):
    if S <= 0:
        raise ValueError(f"S must be positive, got {S}")
    if K <= 0:
        raise ValueError(f"K must be positive, got {K}")
    if T <= 0:
        raise ValueError(f"T must be positive, got {T}")
    if sigma <= 0:
        raise ValueError(f"sigma must be positive, got {sigma}")
    if not isinstance(N, int) or N < 1:
        raise ValueError(f"N must be a positive integer, got {N}")
    if r < -1 or r > 1:
        raise ValueError(f"r looks out of realistic range (-100% to 100%), got {r}")
    if sigma > 5:
        raise ValueError(f"sigma looks out of realistic range (>500% annualized vol), got {sigma}")
    if q < 0 or q > 1:
        raise ValueError(f"q must be between 0 and 1, got {q}")
    if N < 2:
        raise ValueError(f"N must be at least 2 for Greeks (need step-1 and step-2 nodes for delta/gamma/theta), got {N}")

    dt=T/N
    S_history=result.get('asset_tree')
    put_history=result.get('put_tree')
    call_history=result.get('call_tree')
    step_0=S_history[-1]
    step_1=S_history[-2]
    step_2=S_history[-3]

    S_d,S_u=S_history[-2]
    V_put_d,V_put_u=put_history[-2]
    V_call_d,V_call_u=call_history[-2]

    S_dd,S_ud,S_uu=S_history[-3]
    V_put_dd,V_put_ud,V_put_uu=put_history[-3]
    V_call_dd,V_call_ud,V_call_uu=call_history[-3]

    delta_call=(V_call_u-V_call_d)/(S_u-S_d)
    delta_put=(V_put_u-V_put_d)/(S_u-S_d)

    var3=0.5*(S_uu-S_dd)

    var1_call=(V_call_uu-V_call_ud)/(S_uu-S_ud)
    var2_call=(V_call_ud-V_call_dd)/(S_ud-S_dd)
    gamma_call=(var1_call-var2_call)/(var3)

    var1_put=(V_put_uu-V_put_ud)/(S_uu-S_ud)
    var2_put=(V_put_ud-V_put_dd)/(S_ud-S_dd)
    gamma_put=(var1_put-var2_put)/(var3)

    theta_call=(V_call_ud-result['call_price'])/(2*dt)
    theta_put=(V_put_ud-result['put_price'])/(2*dt)

    h=0.0001

    vega_result_1=binomial_tree_option_pricing(S,K,T,r,sigma+h,q,N)
    vega_result_2=binomial_tree_option_pricing(S,K,T,r,sigma-h,q,N)

    vega_call=(vega_result_1.get('call_price')-vega_result_2.get('call_price'))/(2*h)
    vega_put=(vega_result_1.get('put_price')-vega_result_2.get('put_price'))/(2*h)

    rho_result_1=binomial_tree_option_pricing(S,K,T,r+h,sigma,q,N)
    rho_result_2=binomial_tree_option_pricing(S,K,T,r-h,sigma,q,N)
    
    rho_call=(rho_result_1.get('call_price')-rho_result_2.get('call_price'))/(2*h)
    rho_put=(rho_result_1.get('put_price')-rho_result_2.get('put_price'))/(2*h)

    return {
    'delta_call': delta_call, 'delta_put': delta_put,
    'gamma_call': gamma_call, 'gamma_put': gamma_put,
    'theta_call': theta_call, 'theta_put': theta_put,
    'vega_call': vega_call, 'vega_put': vega_put,
    'rho_call': rho_call, 'rho_put': rho_put
}

def plot_convergence(S,K,T,r,sigma,q,N_values,bs_call,bs_put):
    tree_calls=[]
    tree_puts=[]
    N_list = list(N_values)
    for N in N_list:
        data=binomial_tree_option_pricing(S,K,T,r,sigma,q,N)
        tree_calls.append(data.get('call_price'))
        tree_puts.append(data.get('put_price'))

    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=("Call: Convergence to Black-Scholes", "Put: Convergence to Black-Scholes")
    )

    # Call Subplot
    fig.add_trace(
        go.Scatter(
            x=N_list,
            y=tree_calls,
            mode='lines+markers',
            name='Tree (American Call)',
            line=dict(color='#1f77b4', width=2),
            marker=dict(size=4)
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=[N_list[0], N_list[-1]],
            y=[bs_call, bs_call],
            mode='lines',
            name='Black-Scholes (European Call)',
            line=dict(color='red', width=2, dash='dash')
        ),
        row=1, col=1
    )

    # Put Subplot
    fig.add_trace(
        go.Scatter(
            x=N_list,
            y=tree_puts,
            mode='lines+markers',
            name='Tree (American Put)',
            line=dict(color='#2ca02c', width=2),
            marker=dict(size=4)
        ),
        row=1, col=2
    )
    fig.add_trace(
        go.Scatter(
            x=[N_list[0], N_list[-1]],
            y=[bs_put, bs_put],
            mode='lines',
            name='Black-Scholes (European Put)',
            line=dict(color='red', width=2, dash='dash')
        ),
        row=1, col=2
    )

    fig.update_xaxes(title_text="N (steps)", row=1, col=1)
    fig.update_yaxes(title_text="Price ($)", row=1, col=1)
    fig.update_xaxes(title_text="N (steps)", row=1, col=2)
    fig.update_yaxes(title_text="Price ($)", row=1, col=2)

    fig.update_layout(
        title_text="Binomial Tree Convergence to Black-Scholes",
        template="plotly_white",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="center", x=0.5)
    )

    return fig
