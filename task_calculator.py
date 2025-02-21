import streamlit as st
import pandas as pd

# スマホ対応のレイアウト調整
st.set_page_config(page_title="タスク報酬計算アプリ", layout="centered")

# タイトル
st.title("タスク報酬計算アプリ")

# 為替レート設定
exchange_rate = st.number_input("為替レート (1 USD = ? JPY)", value=150.0, step=0.1)

# タスクデータ
st.subheader("タスク情報を入力")
data = {
    "タスク名": [
        "3D Bridges - Ext", "3D Highways - Ext", "3D Key Areas - Buildings - Ext", "3D Piers v2", "3D Rails - Ext", "3D_Tunnels", 
        "Active Tagging", "Address Verification", "AFM Concept Explain Eval 2", "Assistant Response: Select", "Audio Evaluation", 
        "Autocomplete", "Broad Match Ratings", "Business Name Annotation", "colored_lanes_annot", "Crosswalk Annotation", "Driving Navigation - 3D Maps", 
        "Email Categorization Japanese Language", "Fact Verification", "Intersections_3D", "Lane Marking Annotation", "Localization quality review", 
        "Maps_Search_2.0", "Mexican Cultural Relevance of Concepts", "music_caption_multilanguage", "Name Translation", "Painted_Medians_Annotation", 
        "Photo Search Satisfaction", "Physical_Medians_Annotation", "POI Closures", "POI Evaluation", "POI Existence", "Question-Answering response correctness evaluation", 
        "Reg_marking_annotation", "RSM_annot_glyph", "RSM_annot_text", "SafetyNet Image Classification", "Search 2.0", "Search Ads Close Variants", "Search Ads Relevance", 
        "Search SBS", "Siri Named Entities", "Speed Limit Eval v2", "Time Sensitive Emails Categorization Japanese Language", "Transition quality", "WebImagesSingleSideImageSatisfaction"
    ],
    "時間(秒)": [300, 180, 240, 180, 180, 300, 240, 135, 600, 120, 10, 90, 45, 80, 240, 240, 120, 45, 240, 180, 1000, 30, 90, 60, 180, 30, 240, 137, 240, 476, 120, 240, 30, 240, 180, 180, 40, 90, 45, 120, 60, 10, 300, 60, 90, 120],
    "報酬(USD)": [0.500, 0.300, 0.400, 0.300, 0.300, 0.500, 0.400, 0.277, 1.000, 0.200, 0.017, 0.150, 0.075, 0.133, 0.400, 0.400, 0.200, 0.075, 0.400, 0.300, 1.667, 0.050, 0.150, 0.100, 0.300, 0.050, 0.400, 0.228, 0.400, 0.793, 0.200, 0.400, 0.050, 0.400, 0.300, 0.300, 0.067, 0.195, 0.075, 0.200, 0.100, 0.017, 0.500, 0.100, 0.150, 0.200]
}
df = pd.DataFrame(data)

# ユーザー入力（データ貼り付け）
st.subheader("タスクデータを貼り付け")
input_text = st.text_area("タスク名\t作業時間(秒)\t評価数", "")

if input_text:
    lines = input_text.strip().split("\n")
    input_data = []
    for line in lines:
        parts = line.split("\t")
        if len(parts) == 3:
            task_name, time_allocated, total_surveys = parts
            try:
                time_allocated = int(time_allocated.replace("s", ""))
                total_surveys = int(total_surveys)
                input_data.append([task_name, time_allocated, total_surveys])
            except ValueError:
                st.error("数値の変換に失敗しました。入力フォーマットを確認してください。")
    
    if input_data:
        input_df = pd.DataFrame(input_data, columns=["タスク名", "作業時間(秒)", "評価数"])
        result_df = input_df.merge(df, on="タスク名", how="left")
        result_df.dropna(inplace=True)
        result_df["合計報酬(USD)"] = result_df["報酬(USD)"] * result_df["評価数"]
        result_df["合計報酬(JPY)"] = result_df["合計報酬(USD)"] * exchange_rate
        
        st.subheader("計算結果")
        st.dataframe(result_df[["タスク名", "作業時間(秒)", "評価数", "報酬(USD)", "合計報酬(USD)", "合計報酬(JPY)"]], use_container_width=True)
        
        total_usd = result_df["合計報酬(USD)"].sum()
        total_jpy = result_df["合計報酬(JPY)"].sum()
        
        st.subheader("総合計")
        st.write(f"**総合計報酬: {total_usd:.2f} USD / {total_jpy:.2f} JPY**")
# Task Calculator Script
