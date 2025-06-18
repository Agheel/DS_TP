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
from folium.plugins import MarkerCluster

st.set_page_config(layout="wide")

# ─────────────────────────────
# 📦 캐시 처리된 데이터/이미지 로딩 함수
# ─────────────────────────────
@st.cache_data
def load_excel(path):
    return pd.read_excel(path, engine="openpyxl")

@st.cache_data
def load_image(path, size=None):
    img = Image.open(path)
    return img.resize(size) if size else img

@st.cache_resource
def get_font():
    path = "fonts/NanumGothic.ttf"
    return fm.FontProperties(fname=path) if os.path.exists(path) else None

fontprop = get_font()

st.header("📍 진주시 범죄")

# ─────────────────────────────
# 📍 탭 구분
# ─────────────────────────────
tabs = st.tabs(["1️⃣ 주제 선정", "2️⃣ 이론적 배경", "3️⃣ 위험도 비교", "4️⃣ 지도", "5️⃣ 해결방안"])

# ─────────────────────────────
# 1️⃣ 주제 선정 탭
# ─────────────────────────────
with tabs[0]:
    st.markdown("<h3 style='text-align: center;'>1️⃣ 주제 선정 배경</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image(load_image("data/crime_region.png", size=(300, 250)), caption="경상남도의 지역별 범죄지수")
    with col2:
        st.image(load_image("data/crime_year.png", size=(300, 250)), caption="연도별 진주시 범죄 지수")

    st.markdown("""
    <div style='text-align: center;'>
    👉 이러한 배경 속에서, 우리는 진주시의 범죄의 특성을 파악하고 시간적, 환경적 요인을 분석하여 대책을 제안하고 싶습니다.
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────
# 2️⃣ 이론적 배경
# ─────────────────────────────
with tabs[1]:
    st.markdown("<h3 style='text-align: center;'>2️⃣ 환경적 요인과 이론적 배경</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center;'>
    - 국내 연구에 따르면, 범죄 발생에는 시간적, 환경적 요인이 큰 영향을 미친다는 연구 내용이 있습니다.<br>
    - 대표적인 것이 CPTED 이론입니다.<br>
    - CPTED이론(범죄예방이론)은 사람과 시간, 환경적 요인이 범죄 발생에 큰 영향을 끼친다는 이론입니다.<br>
    - 저희는 그 중에서 시간적 요인과 환경적 요인에 중점을 두고 프로젝트를 진행하겠습니다.<br><br>
    🔗 <a href='https://www.safemap.go.kr/' target='_blank'>생활안전지도 바로가기</a><br>
    🔗 <a href='http://www.cpted.kr/?r=home&c=02/0205/020501' target='_blank'>CPTED 개념 보러가기</a><br>
    🔗 <a href='https://www.yna.co.kr/view/AKR20200108078300004' target='_blank'>가로등과 범죄율의 관계 기사</a>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────
# 3️⃣ 위험도 비교
# ─────────────────────────────
with tabs[2]:
    st.markdown("<h3 style='text-align: center;'>3️⃣ 위험도 및 방범시설 비교</h3>", unsafe_allow_html=True)

    grade_df = load_excel("data/jinju_crime_grade.xlsx")
    lamp_cctv_df = load_excel("data/jinju_cctv_lamp.xlsx")
    time_df = load_excel("data/crime_time.xlsx")

    merged_df = pd.merge(grade_df, lamp_cctv_df, on="행정동", how="inner")
    selected = ["충무공동", "천전동", "평거동", "하대동", "초장동", "가호동", "상대동"]
    df = merged_df[merged_df["행정동"].isin(selected)].copy().sort_values(by="위험등급", ascending=False)

    x = np.arange(len(df))
    width = 0.25
    fig1, ax1 = plt.subplots(figsize=(5.5, 3))
    ax1.plot(x, df["위험등급"], color='red', marker='o')
    ax1.set_ylabel("위험등급 (1~10)", color='red', fontproperties=fontprop)
    ax1.set_xticks(x)
    ax1.set_xticklabels(df["행정동"], rotation=45, fontproperties=fontprop)
    ax1.set_ylim(0, 10)
    ax1.tick_params(axis='y', labelcolor='red')

    ax2 = ax1.twinx()
    ax2.bar(x - width/2, df["CCTV_개수"] / 100, width, color='blue', label='CCTV')
    ax2.bar(x + width/2, df["가로등_개수"] / 100, width, color='orange', label='가로등')
    ax2.set_ylabel("시설 수 (x100)", color='blue', fontproperties=fontprop)
    ax2.tick_params(axis='y', labelcolor='blue')

    crime_by_time = time_df.drop(columns=["범죄대분류"]).sum().sort_values(ascending=False)
    fig2, ax = plt.subplots(figsize=(5.5, 3))
    ax.bar(crime_by_time.index, crime_by_time.values, color='skyblue')
    ax.set_title("시간대별 범죄 발생 건수", fontproperties=fontprop)
    ax.set_xlabel("시각대", fontproperties=fontprop)
    ax.set_ylabel("건수", fontproperties=fontprop)
    ax.set_xticks(np.arange(len(crime_by_time)))
    ax.set_xticklabels(crime_by_time.index, rotation=45, fontproperties=fontprop)

    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(fig1)
    with col2:
        st.pyplot(fig2)

# ─────────────────────────────
# 4️⃣ 지도 시각화
# ─────────────────────────────
with tabs[3]:
    st.markdown("<h3 style='text-align: center;'>4️⃣ 진주시 행정구역별 방범시설 지도</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        show_cctv = st.checkbox("🔴 CCTV 위치 보기", value=False)
    with col2:
        show_lamp = st.checkbox("🔵 가로등 위치 보기", value=False)

    if "jinju_map" not in st.session_state:
        st.session_state.jinju_map = folium.Map(location=[35.1802, 128.1076], zoom_start=13, tiles="CartoDB positron")
    m = st.session_state.jinju_map

    if show_cctv:
        cctv_df = load_excel("data/jinju_cctv.xlsx")
        cluster = MarkerCluster().add_to(m)
        for _, row in cctv_df.iterrows():
            folium.Marker(
                location=[row["위도"], row["경도"]],
                tooltip="📷 CCTV",
                icon=folium.Icon(color="red", icon="camera", prefix="fa")
            ).add_to(cluster)

    if show_lamp:
        lamp_df = load_excel("data/jinju_lamp.xlsx")
        cluster = MarkerCluster().add_to(m)
        for _, row in lamp_df.iterrows():
            folium.Marker(
                location=[row["위도"], row["경도"]],
                tooltip="💡 가로등",
                icon=folium.Icon(color="blue", icon="lightbulb-o", prefix="fa")
            ).add_to(cluster)

    st_folium(m, width=800, height=500)
    
# ─────────────────────────────
# 5️⃣ 해결방안
# ─────────────────────────────
with tabs[4]:
    st.markdown("<h3 style='text-align: center;'>5️⃣ 해결 방안 제시</h3>", unsafe_allow_html=True)
    st.markdown("""
### ✅ 해결 방안 제시
- 📌 **부족한 지역에 CCTV 추가 설치**
- 💡 **가로등 설치 및 노후화된 시설 개선**
- ⏰ **가로등 운영시간 연장 (심야 시간 포함)**
- ☎️ **안심귀가 콜 서비스 활성화**
""")
