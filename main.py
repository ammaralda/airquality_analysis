import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns



st.header('Air Quality Dashboard')
st.subheader('(Dongsi Subdistrict, Beijing)')
col_name, col_detail = st.columns(2)
with col_name:

    st.write(
        """
        Created by: Dehan Ammaralda Handiana        
        """
    )

with col_detail:
    st.write(
        """
        24-Hour analysis (Summer Season)
        """
    )

main_dongsi = pd.read_csv("data/PRSA_Data_Dongsi_20130301-20170228.csv")  # read a CSV file inside the 'data" folder next to 'app.py'
summer_dongsi = main_dongsi.loc[(main_dongsi["month"].isin([6,7,8]))]
summer_dongsi = summer_dongsi.dropna()


st.subheader('Data Overview')
dongsi_24 = summer_dongsi.groupby(["hour"], as_index=False).mean(numeric_only = True).drop(['No', 'year', "month", "day"], axis=1)
st.table(dongsi_24)


data_stats = summer_dongsi.describe()
st.subheader('Data Statistic')
st.table(data_stats)


st.subheader('Temperature Changes in 24 hour')
st.bar_chart(data=dongsi_24, x = "hour", y = "TEMP")


min = int(dongsi_24["TEMP"].min())
max = int(dongsi_24["TEMP"].max())
st.markdown(f"**Highest** temperature in a day (summer): ***{max} Celcius***")
st.markdown(f"**Lowest** temperature in a day (summer): ***{min} Celcius***")



st.subheader('PM2.5 - CO Correlation')
ax1 = plt.subplot()
l1, = ax1.plot(dongsi_24["PM2.5"], color='red')
ax2 = ax1.twinx()
l2, = ax2.plot(dongsi_24["CO"], color='orange')
plt.legend([l1, l2], ["PM2.5", "CO"])
st.pyplot(plt.gcf()) # instead of plt.show()

pollution_corr = dongsi_24['PM2.5'].corr(dongsi_24['CO']).round(decimals = 3)
st.markdown(f"Correlation between PM2.5 and Carbon Monoxide (CO): ***{pollution_corr}***")



st.subheader('Level of Optimum Humidity (Temperature - Dewpoint Factor)')
temp_dew = pd.DataFrame(
   {
       "Temp-Dew": dongsi_24["TEMP"] - dongsi_24["DEWP"],
       "Max level": 5
   }
)
st.line_chart(data=temp_dew, y=["Temp-Dew", "Max level"], color=["#e80000", "#85caff"])