import streamlit as st
from datetime import datetime, timedelta
from utils import get_roc_date, fetch_data, show_progress_bar, process_data, generate_trend_chart, generate_scatter_chart

st.page_link("app.py", label="回到首頁", icon="🏠")
st.title("花椰菜🥦")

current = get_roc_date(datetime.now())
two_years_ago = get_roc_date(datetime.now() - timedelta(days=365))
url = f'https://data.moa.gov.tw/Service/OpenData/FromM/FarmTransData.aspx?StartDate={two_years_ago}&EndDate={current}&CropCode=LB1'
data = fetch_data(url)

show_progress_bar()

df = process_data(data)

generate_trend_chart(df)
generate_scatter_chart(df)
