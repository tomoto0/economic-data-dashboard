#!/usr/bin/env python3
"""
経済データダッシュボードを更新するスクリプト
"""

import pandas as pd
import json
from datetime import datetime
import os
import google.generativeai as genai

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def generate_summary(data_frame):
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = f"""
    以下の経済データに基づいて、主要なトレンドと洞察をまとめた簡潔な要約を生成してください。
    データは以下の通りです：
    {data_frame.to_string()}
    
    要約は、一般の読者にも理解しやすいように、専門用語を避け、約200文字程度で記述してください。
    """
    response = model.generate_content(prompt)
    return response.text

def update_dashboard():
    pass