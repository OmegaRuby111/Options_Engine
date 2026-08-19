import streamlit as st
from blackscholes import black_scholes,greeks
from monte_carlo import simulate_paths,plot_paths,european_mc_call,european_mc_put,asian_mc_call,asian_mc_put
from bt_option_pricing import binomial_tree_option_pricing, compute_greeks, plot_convergence

st.set_page_config(page_title="Options Pricing Engine", layout="wide")
st.title("Options Pricing Engine")

with st.sidebar:
    S=st.number_input("Stock Price(S)",value=100.0)
    K=st.number_input("Strike Price(K)",value=100.0)
    r=st.number_input("Risk Free Rate(r)",value=0.05)
    sigma=st.number_input("Volatility(σ)",value=0.2)
    days=st.number_input("Days to Maturity",value=30,min_value=1)
    n=st.slider("Simulations",min_value=1000,max_value=100000,value=10000,step=1000)
    calculate=st.button("Calculate")
    
if calculate:
    paths,time_steps=simulate_paths(S,r,sigma,n,days)
    tab1,tab2,tab3,tab4=st.tabs(["European (Black-Scholes)", "European (Monte Carlo)", "Asian (Monte Carlo)", "American (Binomial Tree)"])
    
    with tab1:
        call_price = black_scholes(r, S, K, days, sigma, "C")
        put_price = black_scholes(r, S, K, days, sigma, "P")
        col1,col2=st.columns(2)
        with col1:
            st.metric("European Call",f"${call_price:.4f}")
        with col2:
            st.metric("European Put",f"${put_price:.4f}")
        st.subheader("Option Greeks")
        delta_call, delta_put, gamma, rho_call, rho_put, vega, theta_call, theta_put = greeks(r, S, K, days, sigma)
        
        greeks_data = {
            "Greek": ["Delta", "Gamma", "Vega", "Theta", "Rho"],
            "Call": [delta_call, gamma, vega, theta_call, rho_call],
            "Put": [delta_put, gamma, vega, theta_put, rho_put]
        }
        st.dataframe(greeks_data, hide_index=True)

    with tab2:
        eu_call, eu_call_se = european_mc_call(K, n, r, days, paths)
        eu_put, eu_put_se = european_mc_put(K, n, r, days, paths)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("European Call", f"${eu_call:.4f}")
            st.caption(f"Standard Error: {eu_call_se:.4f}")
        with col2:
            st.metric("European Put", f"${eu_put:.4f}")
            st.caption(f"Standard Error: {eu_put_se:.4f}")
        
        st.plotly_chart(plot_paths(K, paths, time_steps), use_container_width=True, key="mc_eu_paths")

    with tab3:
        asian_call, asian_call_se = asian_mc_call(K, n, r, days, paths)
        asian_put, asian_put_se = asian_mc_put(K, n, r, days, paths)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Asian Call", f"${asian_call:.4f}")
            st.caption(f"Standard Error: {asian_call_se:.4f}")
        with col2:
            st.metric("Asian Put", f"${asian_put:.4f}")
            st.caption(f"Standard Error: {asian_put_se:.4f}")
        
        st.plotly_chart(plot_paths(K, paths, time_steps), use_container_width=True, key="mc_asian_paths")

    with tab4:
        T_years = days / 365
        N = 200
        q_div = 0

        result = binomial_tree_option_pricing(S, K, T_years, r, sigma, q_div, N)
        greeks_out = compute_greeks(result, S, K, T_years, r, sigma, q_div, N)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("American Call", f"${result['call_price']:.4f}")
        with col2:
            st.metric("American Put", f"${result['put_price']:.4f}")

        st.subheader("Option Greeks")
        greeks_data_tree = {
            "Greek": ["Delta", "Gamma", "Theta", "Vega", "Rho"],
            "Call": [greeks_out['delta_call'], greeks_out['gamma_call'], greeks_out['theta_call'], greeks_out['vega_call'], greeks_out['rho_call']],
            "Put": [greeks_out['delta_put'], greeks_out['gamma_put'], greeks_out['theta_put'], greeks_out['vega_put'], greeks_out['rho_put']]
        }
        st.dataframe(greeks_data_tree, hide_index=True)

        st.subheader("Convergence to Black-Scholes")
        bs_call_ref = black_scholes(r, S, K, days, sigma, "C")
        bs_put_ref = black_scholes(r, S, K, days, sigma, "P")
        N_values = range(10, 501, 10)
        fig = plot_convergence(S, K, T_years, r, sigma, q_div, N_values, bs_call_ref, bs_put_ref)
        st.plotly_chart(fig, use_container_width=True, key="bt_convergence")
