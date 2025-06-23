#!/usr/bin/env python3
"""
経済データダッシュボードを更新するスクリプト
"""

import pandas as pd
import json
from datetime import datetime
import os

def update_dashboard():
    """
    最新データでダッシュボードを更新
    """
    print("Updating dashboard with latest data...")
    
    # CSVデータの読み込み
    try:
        df = pd.read_csv('economic_data.csv')
        print(f"Loaded data for {len(df)} countries")
    except FileNotFoundError:
        print("economic_data.csv not found. Please run fetch_data.py first.")
        return
    
    # 更新情報の読み込み
    try:
        with open('data_update_info.json', 'r') as f:
            update_info = json.load(f)
    except FileNotFoundError:
        update_info = {
            "last_updated": datetime.now().isoformat(),
            "countries_count": len(df),
            "indicators_count": 7
        }
    
    # HTMLファイルの更新日時を更新
    html_files = ['index.html', 'modern-dashboard-simple.html']
    
    for html_file in html_files:
        if os.path.exists(html_file):
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 更新日時を現在の日時に置換
                current_date = datetime.now().strftime('%Y/%m/%d')
                
                # 複数のパターンで更新日時を検索・置換
                import re
                
                # パターン1: 最終更新: YYYY/MM/DD
                content = re.sub(
                    r'最終更新:\s*\d{4}/\d{1,2}/\d{1,2}',
                    f'最終更新: {current_date}',
                    content
                )
                
                # パターン2: Updated: YYYY-MM-DD
                content = re.sub(
                    r'Updated:\s*\d{4}-\d{1,2}-\d{1,2}',
                    f'Updated: {datetime.now().strftime("%Y-%m-%d")}',
                    content
                )
                
                # パターン3: JavaScript内の日付更新
                content = re.sub(
                    r"document\.getElementById\('lastUpdate'\)\.textContent = new Date\(\)\.toLocaleDateString\('ja-JP'\);",
                    f"document.getElementById('lastUpdate').textContent = '{current_date}';",
                    content
                )
                
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"Updated {html_file}")
                
            except Exception as e:
                print(f"Error updating {html_file}: {e}")
    
    # データ統計の計算
    latest_year_columns = [col for col in df.columns if col.endswith('_2024')]
    gdp_columns = [col for col in latest_year_columns if 'GDP (current US$)' in col]
    pop_columns = [col for col in latest_year_columns if 'Population, total' in col]
    
    if gdp_columns and pop_columns:
        # 主要5カ国のデータを計算（USA, CHN, JPN, DEU, GBR）
        major_countries = ['US', 'CN', 'JP', 'DE', 'GB']
        major_df = df[df['CountryID'].isin(major_countries)]
        
        if not major_df.empty:
            total_gdp = major_df[gdp_columns[0]].sum() if gdp_columns else 0
            total_pop = major_df[pop_columns[0]].sum() if pop_columns else 0
            
            print(f"Major 5 countries total GDP: ${total_gdp/1e12:.1f}T")
            print(f"Major 5 countries total population: {total_pop/1e9:.1f}B")
    
    # README.mdの更新
    readme_content = f"""# 経済データダッシュボード - モダン版

## 概要
世界銀行オープンデータを活用した、モダンでインタラクティブな経済データダッシュボードです。

## 特徴
- 📊 インタラクティブなチャート表示
- 🌙 ダークモード対応
- 📱 レスポンシブデザイン
- 🔄 自動データ更新（毎日15:00 JST）
- 🎨 モダンなUI/UX

## 表示データ
- GDP (current US$)
- 人口
- インフレ率
- 失業率
- 外国直接投資
- 外貨準備高

## 対象国
USA, CHN, JPN, DEU, GBR, FRA, IND, ITA, BRA, CAN

## 技術スタック
- HTML5 + CSS3 + JavaScript
- Chart.js (データ可視化)
- Tailwind CSS (スタイリング)
- GitHub Actions (自動更新)
- GitHub Pages (ホスティング)

## 最終更新
{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S JST')}

## データソース
[World Bank Open Data](https://data.worldbank.org/)

## ライセンス
MIT License
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("README.md updated")
    print("Dashboard update completed successfully!")

if __name__ == "__main__":
    update_dashboard()

