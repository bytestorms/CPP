import streamlit as st
import pandas as pd
import numpy as np
from numformat import numerize


st.title('Continuous Pension Plan')

st.sidebar.subheader('Choose your yearly investment amount:')
invest = int(st.sidebar.number_input("INR ", 20000, 200000, 60000, 5000))

st.sidebar.subheader('Choose yearly return of market index:')
interest = st.sidebar.slider("Select Percentage:", 5.0, 15.0, 6.5, 0.5)
st.sidebar.text(f"Selected Rate of return: {interest} %")

st.sidebar.subheader('How many years before pension start?')
pension_after = st.sidebar.slider("Select year:", 4, 40, 5, 1)

st.sidebar.subheader('Percentage of capital to use as pension:')
pension_frac = st.sidebar.slider("Select Percentage:", 5., 15., 10., 0.1)

st.subheader('Length of projection:')
proj_yr = int(st.number_input("Number of years:", 5, 50, 10, 5))
# start_yr = st.selectbox("Number of years:", list(range(5, 101, 5)), 10)

st.subheader("Summary")
st.markdown(f"Yearly Investment: `₹ {numerize(int(invest))}`")
st.markdown(f"Yearly Return from a market index: `{interest} %` ")
st.markdown(f"Yearly pension is collected as `{pension_frac} %` of capital")
st.markdown(f"Projecting for `{proj_yr} years`")
st.markdown(f"Pension starts after `{pension_after} years`")


st.header("Outcome")

start_yr = 2022
pension_after += start_yr
stop_yr = proj_yr + start_yr

results = []

portfolio = 0
total_invest = 0
total_pension = 0

for y in range(start_yr, stop_yr + 1):
    portfolio = (1+interest/100)*portfolio + invest
    total_invest += invest
    
    if y >= pension_after:
        pension_pm = portfolio * (pension_frac/100)/12
    else:
        pension_pm = 0
        
    results.append(
        {
            'Year': y,
            'Invest this year': invest,
            'Total Invested': total_invest,
            'Valuation': round(portfolio),
            'Valuation after pension': round(portfolio - pension_pm*12),
            'Pension (monthly)': round(pension_pm)
        }
    )
    if y>= pension_after:
        total_pension += pension_pm*12
        portfolio -= pension_pm*12

df = pd.DataFrame(results)
df = df.set_index("Year")
st.table(df)

st.header("Maturity")
cols = st.columns(3)
cols[0].metric("Total Invested", f"₹ {numerize(total_invest)}")
cols[1].metric("Total Recieved", f"₹ {numerize(portfolio + total_pension)}")
cols[2].metric("Valuation", f"{(portfolio + total_pension)/total_invest:0.0%}")

cols = st.columns(3)

cols[1].metric("Maturity Amount", f"₹ {numerize(round(portfolio))}", delta = numerize(round(portfolio - total_invest)))
cols[2].metric("Valuation", f"{(portfolio)/total_invest:0.0%}")