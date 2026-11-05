import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("TABLE 9.15 Selected Notifiable Diseases Reported Cases by Cause- 2014 to 2021.csv", skiprows=1)

st.set_page_config(layout = 'wide')

st.title("Selected Notifiable Diseases Reported Cases by Causes (2014 - 2021)")
st.write("The following charts represent the dataset provided by the Philippine Statistics Authority (PSA).")


yearColumns = [str(y) for y in range(2014, 2022)]
for col in yearColumns:
    df[col] = (
        pd.to_numeric(df[col].astype(str).str.replace('...', ''), errors='coerce')
        .fillna(0)
    )

df['totalCounts'] = df[yearColumns].sum(axis=1)
df_sorted = df.sort_values(by = 'totalCounts', ascending = True)


# Horizontal Bar Chart #
fig1 = px.bar(
    df_sorted,
    x = 'totalCounts',
    y = 'Notifiable Diseases',
    orientation = 'h',
    title = 'Total Counts of the Selected Notifiable Diseases Reported Cases',
    log_x = True,
    color_discrete_sequence = ['#1f77b4']
)

fig1.update_xaxes(

    showgrid = True,
    gridwidth = 1,
    gridcolor = 'lightgray'
)

fig1.update_layout(
    xaxis_title = 'Total Counts',
    yaxis_title = 'Selected Notifiable Diseases',
    font = dict(size = 15),
    height = 600,
    margin = dict(l = 20, r = 40, t = 60, b = 50)
)

st.plotly_chart(fig1, use_container_width = True)


# Line Chart #
df_melted = df.melt(
    id_vars = ['Notifiable Diseases'],
    value_vars = yearColumns,
    var_name = 'Year',
    value_name = 'Reported Cases'
)
df_melted['Reported Cases'] = pd.to_numeric(df_melted['Reported Cases'])
df_melted['Year'] = pd.to_numeric(df_melted['Year'])

allDiseases = sorted(df['Notifiable Diseases'].unique())
defaultSelection = ['Cholera', 'Malaria', 'Leptospirosis']
selectedDiseases = st.multiselect(
    'Select Notifiable Diseases: ',
    options = allDiseases,
    default = defaultSelection
)

if selectedDiseases:
    filtered_df = df_melted[
        df_melted['Notifiable Diseases'].isin(selectedDiseases)
    ]

    fig2 = px.line(
        filtered_df,
        x = 'Year',
        y = 'Reported Cases',
        color = 'Notifiable Diseases',
        markers = True,
        title = 'Reported Cases of the Selected Notifiable Diseases per Year',
        labels = {
            'Reported Cases' : 'Reported Cases',
            'Notifiable Diseases' : 'Notifiable Diseases',
        },
        log_y = False
    )

    fig2.update_xaxes(
        tickmode = 'array',
        tickvals = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021],
    )

    fig2.update_layout(
        xaxis_title = 'Year',
        yaxis_title = 'Reported Cases',
        font = dict(size = 15),
        height = 550,
        margin = dict(l = 100, r = 50, t = 100, b = 100)
    )
    st.plotly_chart(fig2, use_container_width = True)

else:
    st.warning("Please select at least one notifiable disease.")