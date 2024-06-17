import time
import streamlit as st
from datetime import datetime, timedelta
from utils import get_roc_date, fetch_data, show_progress_bar, process_data, generate_trend_chart, generate_scatter_chart

st.page_link("app.py", label="回到首頁", icon="🏠")
st.title("玉米🌽")
bar = st.progress(0, '從『政府資料開放平臺-農產品交易行情』載入資料...')

current = get_roc_date(datetime.now())
two_years_ago = get_roc_date(datetime.now() - timedelta(days=365))
url = f'https://data.moa.gov.tw/Service/OpenData/FromM/FarmTransData.aspx?StartDate={two_years_ago}&EndDate={current}&CropCode=FY6'
data = fetch_data(url)

for i in range(100):
    bar.progress(i + 1, f'目前進度 {i + 1} %')
    time.sleep(0.01)

df = process_data(data)

generate_trend_chart(df)
generate_scatter_chart(df)
