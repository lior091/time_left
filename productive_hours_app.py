import streamlit as st
import plotly.graph_objects as go

def calculate_productive_hours(current_age, life_expectancy, sleep_hours):
    # Calculate the total number of years from age 18 to the median death age
    years_remaining = life_expectancy - current_age
    
    # Calculate the total years of sleep
    years_of_sleep = years_remaining * sleep_hours / 24

    # Assume 20 days of vacation per year
    vacation_days = 20
    years_of_vacation = years_remaining * vacation_days / 365

    # Calculate the total awake and productive hours
    productive_hours = (years_remaining - years_of_sleep - years_of_vacation) * 365 * (24 - sleep_hours)

    return int(productive_hours)

def plot_productive_hours(current_age, life_expectancy, sleep_hours):
    ages = list(range(18, life_expectancy + 1))
    productive_hours_list = []

    for age in ages:
        productive_hours = calculate_productive_hours(age, life_expectancy, sleep_hours)
        productive_hours_list.append(productive_hours)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ages, y=productive_hours_list, mode='lines'))
    fig.update_layout(
        title="Productive Hours Left Over Time",
        xaxis_title="Age",
        yaxis_title="Productive Hours Left",
        xaxis_range=[18, life_expectancy],
        yaxis_range=[0, max(productive_hours_list) * 1.1],  # Add 10% padding to the y-axis range
        annotations=[
            dict(
                x=current_age,
                y=productive_hours_list[current_age - 18],
                xref="x",
                yref="y",
                text=f"Age: {current_age}, Productive Hours Left: {productive_hours_list[current_age - 18]:,}",
                showarrow=True,
                arrowhead=3,
                font=dict(color="black"),
                bgcolor="rgba(255, 255, 255, 0.8)",
            )
        ]
    )

    return fig

def main():
    st.title("'_It's not that we have little time, but more that we waste a good deal of it._'")
    st.markdown("-Seneca")
    st.subheader("Productive Hours Calculator")

    # Input fields
    current_age = st.number_input("Enter your current age", min_value=18, value=18)
    life_expectancy = st.number_input("Enter the median life expectancy", min_value=18, value=73, help="73 is based on the World Health Organization's global estimate")
    sleep_hours = st.number_input("Enter the sleep hours per day", min_value=1, max_value=24, value=8)

    if st.button("Calculate"):
        productive_hours = calculate_productive_hours(current_age, life_expectancy, sleep_hours)
        fig = plot_productive_hours(current_age, life_expectancy, sleep_hours)
        st.plotly_chart(fig, use_container_width=True)
        
        st.info(f"You have approximately **{productive_hours:,}** productive hours left.")

if __name__ == "__main__":
    main()