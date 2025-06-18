import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
from PIL import Image
import numpy as np

#st.set_page_config(layout="wide")

st.title("📍 진주시 범죄")

# ─────────────────────────────
# 1. 주제 선정 이유
# ─────────────────────────────        
st.subheader("1️⃣ 주제 선정 배경")

st.markdown("""
- **경상남도 내에서 지역별 범죄 지수** & **진주의 연도별 범죄 지수**
""")

# 이미지 불러오기 및 리사이즈
img1 = Image.open("/workspaces/DS_TP/data/crime_region.png").resize((400, 350))
img2 = Image.open("/workspaces/DS_TP/data/crime_year.png").resize((500, 430))

# 열 2개 생성
col1, col2 = st.columns(2)

with col1:
    st.image(img1, caption="경상남도의 지역별 범죄지수")

with col2:
    st.image(img2, caption="연도별 진주시 범죄 지수")

# 추가 설명

st.markdown("""
👉 이러한 배경 속에서, 우리는 진주시의 범죄의 특성을 파악하고 시간적, 환경적 요인을 분석하여 대책을 제안하고 싶습니다.
""")

# ─────────────────────────────
# 2. 시간적, 환경적 요인과 이론적 배경
# ─────────────────────────────
st.subheader("2️⃣ 환경적 요인과 이론적 배경")

st.markdown("""
- 국내 연구에 따르면, 범죄 발생에는 시간적, 환경적 요인이 큰 영향을 미친다는 연구 내용이 있습니다.
- 대표적인 것이 CPTED 이론입니다.
- CPTED이론(범죄예방이론)은 사람과 시간, 환경적 요인이 범죄 발생에 큰 영향을 끼친다는 이론입니다.
- 저희는 그 중에서 시간적 요인과 환경적 요인에 중점을 두고 프로젝트를 진행하겠습니다. 
       
[👉 생활안전지도 바로가기](https://www.safemap.go.kr/)       
[👉 CPTED 개념 보러가기](http://www.cpted.kr/?r=home&c=02/0205/020501)  
[👉 가로등과 범죄율의 관계 기사](https://www.yna.co.kr/view/AKR20200108078300004)
""")

# ─────────────────────────────
# 3. 위험도 및 시설물 통계 비교
# ─────────────────────────────
st.markdown("진주시 행정동별 위험도 및 방범 시설 비교")

# 데이터 로딩
grade_df = pd.read_excel("/workspaces/DS_TP/data/jinju_crime_grade.xlsx")
lamp_cctv_df = pd.read_excel("/workspaces/DS_TP/data/jinju_cctv_lamp.xlsx")
time_df=pd.read_excel("/workspaces/DS_TP/data/crime_time.xlsx")

# 병합
merged_df = pd.merge(grade_df, lamp_cctv_df, on="행정동", how="inner")

# 그래프
st.markdown("#### 🔢 위험등급 AND CCTV & 가로등 수")

# 값 준비
import plotly.graph_objects as go

target_dongs_graph = ["충무공동", "천전동", "평거동", "하대동", "초장동", "가호동", "상대동", "상봉동"]
filtered = merged_df[merged_df["행정동"].isin(target_dongs_graph)].copy()
filtered.sort_values(by="위험등급", ascending=False, inplace=True)

# 시각화 데이터 준비
labels = filtered["행정동"]
risk = filtered["위험등급"]
cctv = filtered["CCTV_개수"] / 100
lamp = filtered["가로등_개수"] / 100

# Plotly 그래프 구성
fig = go.Figure()

# 위험등급 (꺾은선)
fig.add_trace(go.Scatter(
    x=labels,
    y=risk,
    mode='lines+markers',
    name='위험등급',
    line=dict(color='red'),
    yaxis='y1'
))

# CCTV (막대)
fig.add_trace(go.Bar(
    x=labels,
    y=cctv,
    name='CCTV (x100)',
    marker_color='blue',
    yaxis='y2',
    offsetgroup=1
))

# 가로등 (막대)
fig.add_trace(go.Bar(
    x=labels,
    y=lamp,
    name='가로등 (x100)',
    marker_color='orange',
    yaxis='y2',
    offsetgroup=2
))

# 레이아웃
fig.update_layout(
    title='선정된 행정동 위험등급 (선) vs CCTV 및 가로등 수 (막대, x100)',
    xaxis=dict(title='행정동'),
    yaxis=dict(
        title='위험등급 (1~10)',
        range=[0, 10],
        tick0=0,
        dtick=2
    ),
    yaxis2=dict(
        title='시설물 수 (x100)',
        overlaying='y',
        side='right'
    ),
    legend=dict(x=1, y=1),
    bargap=0.2,
    width=1000,
    height=500
)

# 그래프 출력
st.plotly_chart(fig)

st.markdown("**시간대별 범죄 발생 건수**")

#여기에는 시간대별 범죄 발생 건수를 나타내는 그래프

st.markdown("진주시는 범죄율이 높은데 비해 가로등과 CCTV가 적은 곳이 존재함")

# ─────────────────────────────
# 4. 행정구역 + 시설 위치 지도
# ─────────────────────────────
st.subheader("4️⃣ 진주시 시설물 지도")

st.markdown("""
- 아래 지도는 **행정동 경계와 함께 CCTV 및 가로등 위치**를 표시합니다.
- 원하는 필터를 선택해서 볼 수 있습니다.
""")

# 지도 필터
show_cctv = st.checkbox("CCTV 위치 보기", value=False)
show_lamp = st.checkbox("가로등 위치 보기", value=False)

# 지도 데이터 예시 로딩 (위도/경도 포함된 CSV 필요)
cctv_data = pd.read_excel("/workspaces/DS_TP/data/jinju_cctv.xlsx", engine='openpyxl')
lamp_data = pd.read_excel("/workspaces/DS_TP/data/jinju_lamp.xlsx", engine='openpyxl')

map_center = [35.1802, 128.1076]  # 진주시 중심 좌표
m = folium.Map(location=map_center, zoom_start=13)

if show_cctv:
    for _, row in cctv_data.iterrows():
        folium.CircleMarker(
            location=[row['위도'], row['경도']],
            radius=3,
            color='blue',
            fill=True,
            fill_opacity=0.7,
            tooltip="CCTV"
        ).add_to(m)

if show_lamp:
    for _, row in lamp_data.iterrows():
        folium.CircleMarker(
            location=[row['위도'], row['경도']],
            radius=2,
            color='orange',
            fill=True,
            fill_opacity=0.6,
            tooltip="가로등"
        ).add_to(m)

st_data = st_folium(m, width=1000, height=600)

# ─────────────────────────────
# 5. 해결방안 제시
# ─────────────────────────────
st.subheader("5️⃣ 해결 방안 제시")

st.markdown("""
- 📌 **부족한 지역에 CCTV 추가 설치**
- 💡 **가로등 설치 및 노후화된 시설 개선**
- ⏰ **가로등 운영시간 연장 (심야 시간 포함)**
- ☎️ **안심귀가 콜 서비스 활성화** 
""")
