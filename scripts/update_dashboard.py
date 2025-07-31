
#!/usr/bin/env python3
"""
経済データダッシュボードを更新するスクリプト
"""

import pandas as pd
import json
from datetime import datetime
import os
import plotly.express as px
import plotly.io as pio

# HTMLファイルを保存するディレクトリ
OUTPUT_DIR = "./docs"

def update_dashboard():
    # 出力ディレクトリが存在しない場合は作成
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # economic_data.csvを読み込む
    df_raw = pd.read_csv("economic_data.csv")

    # データを整形し、年ごとのデータを時系列データに変換
    # 各指標の列名パターンを定義
    indicators = {
        'GDP (current US$)': 'GDP (current US$)',
        'Population, total': 'Population, total',
        'Unemployment, total (% of total labor force) (modeled ILO estimate)': 'Unemployment, total (% of total labor force) (modeled ILO estimate)',
        'Total reserves (includes gold, current US$)': 'Total reserves (includes gold, current US$)'
    }

    # 最終的なデータフレームを格納するリスト
    df_list = []

    for country_id in df_raw['CountryID'].unique():
        country_data = df_raw[df_raw['CountryID'] == country_id].iloc[0]
        
        for year in range(2015, 2025): # 2015年から2024年まで
            row = {'CountryID': country_id, 'Date': datetime(year, 1, 1)}
            for indicator_key, indicator_name in indicators.items():
                col_name = f'{indicator_key}_{year}'
                if col_name in country_data:
                    row[indicator_name] = country_data[col_name]
                else:
                    row[indicator_name] = None # データがない場合はNone
            df_list.append(row)

    df = pd.DataFrame(df_list)
    df['Date'] = pd.to_datetime(df['Date'])

    # グラフ生成
    # GDP over Time (例として最初の国のみ表示)
    first_country_id = df['CountryID'].iloc[0]
    fig_gdp_over_time = px.line(df[df['CountryID'] == first_country_id], x='Date', y='GDP (current US$)', title=f'GDP Over Time ({first_country_id})')
    pio.write_html(fig_gdp_over_time, file=os.path.join(OUTPUT_DIR, 'gdp_over_time.html'), auto_open=False)

    # Population over Time
    fig_population_over_time = px.line(df[df['CountryID'] == first_country_id], x='Date', y='Population, total', title=f'Population Over Time ({first_country_id})')
    pio.write_html(fig_population_over_time, file=os.path.join(OUTPUT_DIR, 'population_over_time.html'), auto_open=False)

    # Unemployment Trend
    fig_unemployment_trend = px.line(df[df['CountryID'] == first_country_id], x='Date', y='Unemployment, total (% of total labor force) (modeled ILO estimate)', title=f'Unemployment Trend ({first_country_id})')
    pio.write_html(fig_unemployment_trend, file=os.path.join(OUTPUT_DIR, 'unemployment_trend.html'), auto_open=False)

    # Reserves Trend
    fig_reserves_trend = px.line(df[df['CountryID'] == first_country_id], x='Date', y='Total reserves (includes gold, current US$)', title=f'Total Reserves Trend ({first_country_id})')
    pio.write_html(fig_reserves_trend, file=os.path.join(OUTPUT_DIR, 'reserves_trend.html'), auto_open=False)

    # GDP vs Population Scatter
    fig_gdp_vs_population = px.scatter(df, x='Population, total', y='GDP (current US$)', size='GDP (current US$)', color='CountryID', hover_name='CountryID', title='GDP vs Population')
    pio.write_html(fig_gdp_vs_population, file=os.path.join(OUTPUT_DIR, 'gdp_vs_population.html'), auto_open=False)

    print(f"Dashboard updated. HTML files saved to {OUTPUT_DIR}/")

if __name__ == "__main__":
    update_dashboard()


