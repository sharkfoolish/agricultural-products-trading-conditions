# utils.py
import json
from datetime import datetime, timedelta
from urllib import request
import pandas as pd
import colorsys
import streamlit as st
from streamlit_echarts import st_echarts


def get_roc_date(date):
    return f"{date.year - 1911}.{date.month:02d}.{date.day:02d}"


def convert_roc_to_ad(roc_date_str):
    year, month, day = map(int, roc_date_str.split('.'))
    return datetime(year + 1911, month, day)


def generate_green_shades(num_shades):
    green_hue = 0.3
    saturation = 1
    shades = []
    for i in range(num_shades):
        hue = green_hue
        saturation_variation = saturation * (1 - (i / num_shades))
        value = 0.6 + (0.4 * (i / num_shades))
        rgb = colorsys.hsv_to_rgb(hue, saturation_variation, value)
        hex_color = "#{:02x}{:02x}{:02x}".format(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
        shades.append(hex_color)
    return shades


def fetch_data(url):
    with request.urlopen(url) as result:
        return json.load(result)


def process_data(data):
    df = pd.DataFrame(data)

    df['交易日期'] = pd.to_datetime(df['交易日期'].apply(convert_roc_to_ad))
    df['平均價'] = df['平均價'].astype(float)
    df['交易量'] = df['交易量'].astype(int)

    df['月份'] = df['交易日期'].dt.to_period('M')
    df['日期'] = df['交易日期'].dt.date

    recent_avg_price = df.loc[df['交易日期'] == df['交易日期'].max(), '平均價'].mean()
    recent_avg_volume = df.loc[df['交易日期'] == df['交易日期'].max(), '交易量'].mean().astype(int)

    data_table = pd.DataFrame({
        '最近一天的平均價': [recent_avg_price],
        '最近一天的交易量': [recent_avg_volume],
    })
    st.table(data_table)
    return df


def generate_trend_chart(df):
    daily_avg_prices = df.groupby('日期')['平均價'].mean().astype(int).tolist()
    daily_avg_volumes = df.groupby('日期')['交易量'].mean().astype(int).tolist()
    days = sorted(df['日期'].astype(str).unique())

    options_trend = {
        "title": {"text": "每日趨勢圖 (一年以來)"},
        "tooltip": {"trigger": "axis"},
        "grid": {"left": "5%", "right": "5%", "top": "15%", "bottom": "15%", "containLabel": True},
        "xAxis": {
            "type": 'category',
            "data": days,
        },
        "yAxis": [
            {"type": "value", "name": "平均價", "position": "left"},
            {"type": "value", "name": "交易量", "position": "right"},
        ],
        "series": [
            {
                "name": "平均價",
                "data": daily_avg_prices,
                "type": "line",
                "smooth": True,
                "yAxisIndex": 0,
                "itemStyle": {"color": "#6DA854"}
            },
            {
                "name": "交易量",
                "data": daily_avg_volumes,
                "type": "bar",
                "yAxisIndex": 1,
                "itemStyle": {"color": "#cfd2d4"}
            },
        ],
    }
    st_echarts(options=options_trend, height=600, width="100%")


def generate_scatter_chart(df):
    markets = df['市場名稱'].unique()
    colors = generate_green_shades(len(markets))

    scatter_data = []
    for market, color in zip(markets, colors):
        market_data = df[df['市場名稱'] == market].groupby('月份')['平均價'].mean().astype(int)
        scatter_data.append({
            "name": market,
            "type": "scatter",
            "data": [[str(month), price] for month, price in market_data.items()],
            "itemStyle": {"color": color},
        })

    options_scatter = {
        "title": {"text": "各市場每月平均價(一年以來)"},
        "tooltip": {"trigger": "axis"},
        "grid": {"left": "5%", "right": "5%", "top": "15%", "bottom": "15%", "containLabel": True},
        "xAxis": {"type": "category"},
        "yAxis": {"type": "value"},
        "series": scatter_data,
    }
    st_echarts(options=options_scatter, height=600, width="100%")
