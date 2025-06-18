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
img1 = Image.open("data/crime_region.png").resize((400, 350))
img2 = Image.open("data/crime_year.png").resize((500, 430))

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

st.markdown("#### 🔢 위험등급 AND CCTV & 가로등 수")

# 데이터 로딩
time_df=pd.read_excel("/workspaces/DS_TP/data/crime_time.xlsx")

# 📂 엑셀 데이터 불러오기
grade_df = pd.read_excel("jinju_crime_grade.xlsx", engine="openpyxl")
lamp_cctv_df = pd.read_excel("jinju_cctv_lamp.xlsx", engine="openpyxl")

# 🔗 데이터 병합
merged_df = pd.merge(grade_df, lamp_cctv_df, on="행정동", how="inner")

# 🎯 대상 행정동 필터링 및 정렬
target_dongs_graph = ["충무공동", "천전동", "평거동", "하대동", "초장동", "가호동", "상대동", "판문동"]
filtered = merged_df[merged_df["행정동"].isin(target_dongs_graph)].copy()
filtered.sort_values(by="위험등급", ascending=False, inplace=True)

# 📊 시각화 데이터
labels = filtered["행정동"]
x = np.arange(len(labels))
width = 0.25
risk = filtered["위험등급"]
cctv = filtered["CCTV_개수"] / 100
lamp = filtered["가로등_개수"] / 100

# 🎨 그래프 생성
fig, ax1 = plt.subplots(figsize=(14, 6))

# 좌측 Y축: 위험등급 (꺾은선)
ax1.set_ylabel("위험등급 (1~10)", color='red')
ax1.plot(x, risk, color='red', marker='o', label='위험등급')
ax1.tick_params(axis='y', labelcolor='red')
ax1.set_ylim(0, 10)
ax1.set_yticks(np.arange(0, 11, 2))

# 우측 Y축: CCTV & 가로등 (막대)
ax2 = ax1.twinx()
ax2.set_ylabel("시설물 수 (x100)", color='blue')
bars_cctv = ax2.bar(x - width/2, cctv, width, label='CCTV (x100)', color='blue')
bars_lamp = ax2.bar(x + width/2, lamp, width, label='가로등 (x100)', color='orange')
ax2.tick_params(axis='y', labelcolor='blue')
ax2.set_ylim(0, max(max(cctv), max(lamp)) * 1.2)

# X축 설정
ax1.set_xticks(x)
ax1.set_xticklabels(labels, rotation=45)

# 제목 및 범례
plt.title("선정된 행정동 위험등급 (선) vs CCTV 및 가로등 수 (막대, x100)")
fig.legend(loc="upper right", bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)

st.markdown("### 📊 위험등급 vs CCTV & 가로등")
st.pyplot(fig)

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
