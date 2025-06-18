import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import folium
from streamlit_folium import st_folium
from PIL import Image
import numpy as np
import os
from folium.features import CustomIcon

# 폰트 설정
font_path = "fonts/NanumGothic.ttf"
fontprop = fm.FontProperties(fname=font_path) if os.path.exists(font_path) else None
plt.rcParams['axes.unicode_minus'] = False

# 탭 설정
tabs = st.tabs(["📌 주제 배경", "📚 이론적 배경", "📊 위험도 & 시설 통계", "🗺️ 지도 시각화", "💡 해결 방안"])

# ─────────────────────────────
# 1️⃣ 주제 선정 배경
# ─────────────────────────────
with tabs[0]:
    st.title("📍 진주시 범죄")
    st.subheader("1️⃣ 주제 선정 배경")
    st.markdown("- **경상남도 내에서 지역별 범죄 지수** & **진주의 연도별 범죄 지수**")

    img1 = Image.open("data/crime_region.png").resize((400, 350))
    img2 = Image.open("data/crime_year.png").resize((500, 430))
    col1, col2 = st.columns(2)
    col1.image(img1, caption="경상남도의 지역별 범죄지수")
    col2.image(img2, caption="연도별 진주시 범죄 지수")

    st.markdown("👉 진주시의 범죄 특성과 시간·환경적 요인을 분석하여 대책을 제안합니다.")

# ─────────────────────────────
# 2️⃣ 환경적 요인과 이론적 배경
# ─────────────────────────────
with tabs[1]:
    st.subheader("2️⃣ 환경적 요인과 이론적 배경")
    st.markdown("""
    - 국내 연구에 따르면, 범죄 발생에는 시간적, 환경적 요인이 큰 영향을 미칩니다.
    - 대표 이론: **CPTED (범죄예방 환경설계)**
    - 저희는 시간적 요인과 환경적 요인에 집중했습니다.
    [👉 생활안전지도](https://www.safemap.go.kr/)  
    [👉 CPTED 개념](http://www.cpted.kr/?r=home&c=02/0205/020501)  
    [👉 가로등과 범죄율 관련 기사](https://www.yna.co.kr/view/AKR20200108078300004)
    """)

# ─────────────────────────────
# 3️⃣ 위험도 및 시설물 통계 비교
# ─────────────────────────────
with tabs[2]:
    st.subheader("3️⃣ 위험도 vs CCTV & 가로등")

    time_df = pd.read_excel("data/crime_time.xlsx", engine="openpyxl")
    grade_df = pd.read_excel("data/jinju_crime_grade.xlsx", engine="openpyxl")
    lamp_cctv_df = pd.read_excel("data/jinju_cctv_lamp.xlsx", engine="openpyxl")
    merged_df = pd.merge(grade_df, lamp_cctv_df, on="행정동", how="inner")

    target_dongs = ["충무공동", "천전동", "평거동", "하대동", "초장동", "가호동", "상대동"]
    filtered = merged_df[merged_df["행정동"].isin(target_dongs)].copy()
    filtered.sort_values(by="위험등급", ascending=False, inplace=True)

    labels = filtered["행정동"]
    x = np.arange(len(labels))
    width = 0.25
    risk = filtered["위험등급"]
    cctv = filtered["CCTV_개수"] / 100
    lamp = filtered["가로등_개수"] / 100

    fig, ax1 = plt.subplots(figsize=(14, 6))
    ax1.set_ylabel("위험등급 (1~10)", color='red', fontproperties=fontprop)
    ax1.plot(x, risk, color='red', marker='o', label='위험등급')
    ax1.tick_params(axis='y', labelcolor='red')
    ax1.set_ylim(0, 10)
    ax1.set_yticks(np.arange(0, 11, 2))
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=45, fontproperties=fontprop)

    ax2 = ax1.twinx()
    ax2.set_ylabel("시설물 수 (x100)", color='blue', fontproperties=fontprop)
    ax2.bar(x - width/2, cctv, width, label='CCTV (x100)', color='blue')
    ax2.bar(x + width/2, lamp, width, label='가로등 (x100)', color='orange')
    ax2.tick_params(axis='y', labelcolor='blue')
    ax2.set_ylim(0, max(max(cctv), max(lamp)) * 1.2)

    plt.title("위험등급 vs CCTV 및 가로등", fontproperties=fontprop)
    fig.legend(loc="upper right", bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes, prop=fontprop)

    st.pyplot(fig)
    st.markdown("🔎 가로등과 CCTV 수가 적은 지역일수록 위험등급이 높습니다.")

    # 시간대별 발생 그래프
    crime_by_time = time_df.drop(columns=["범죄대분류"]).sum().sort_values(ascending=False)
    fig2, ax = plt.subplots(figsize=(12, 6))
    ax.bar(crime_by_time.index, crime_by_time.values, color='skyblue')

    if fontprop:
        ax.set_title("시간대별 범죄 발생 건수", fontproperties=fontprop)
        ax.set_xlabel("시각대", fontproperties=fontprop)
        ax.set_ylabel("건수", fontproperties=fontprop)
        ax.set_xticklabels(crime_by_time.index, rotation=45, fontproperties=fontprop)

    plt.tight_layout()
    st.markdown("### ⏰ 시간대별 범죄 발생 빈도")
    st.pyplot(fig2)
    st.markdown("🌙 새벽 시간대에 범죄 발생이 많으며, 이때는 가로등이 꺼져 있는 경우가 많습니다.")

# ─────────────────────────────
# 4️⃣ 지도 시각화
# ─────────────────────────────
with tabs[3]:
    st.subheader("4️⃣ 진주시 방범시설 위치 지도")

    cctv_icon = "data/red_marker.png"
    lamp_icon = "data/blue_marker.png"

    col1, col2 = st.columns(2)
    with col1:
        show_cctv = st.checkbox("🔴 CCTV 위치 보기", value=True)
    with col2:
        show_lamp = st.checkbox("🔵 가로등 위치 보기", value=True)

    m = folium.Map(location=[35.1802, 128.1076], zoom_start=13)

    if show_cctv:
        cctv_df = pd.read_excel("data/jinju_cctv.xlsx", engine="openpyxl")
        for _, row in cctv_df.iterrows():
            folium.Marker(
                location=[row["위도"], row["경도"]],
                tooltip="📷 CCTV",
                icon=CustomIcon(cctv_icon, icon_size=(30, 30))
            ).add_to(m)

    if show_lamp:
        lamp_df = pd.read_excel("data/jinju_lamp.xlsx", engine="openpyxl")
        for _, row in lamp_df.iterrows():
            folium.Marker(
                location=[row["위도"], row["경도"]],
                tooltip="💡 가로등",
                icon=CustomIcon(lamp_icon, icon_size=(30, 30))
            ).add_to(m)

    st_data = st_folium(m, width=900, height=500)

# ─────────────────────────────
# 5️⃣ 해결 방안
# ─────────────────────────────
with tabs[4]:
    st.subheader("5️⃣ 해결 방안 제시")
    st.markdown("""
    - 📌 **부족한 지역에 CCTV 추가 설치**
    - 💡 **가로등 설치 및 노후화된 시설 개선**
    - ⏰ **가로등 운영시간 연장 (심야 시간 포함)**
    - ☎️ **안심귀가 콜 서비스 활성화**
    """)
