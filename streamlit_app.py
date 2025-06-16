import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

st.title("📍 진주시 범죄주의구간 분석 및 해결 방안")

# ─────────────────────────────
# 1. 주제 선정 이유
# ─────────────────────────────
st.subheader("1️⃣ 주제 선정 배경")

st.markdown("""
- 아래 이미지는 **경상남도 내에서 진주시의 범죄지수가 상대적으로 높음**을 보여줍니다.
""")

st.image("data/crime_region.png", caption="경상남도의 지역별 범죄지수", use_column_width=True)

st.markdown("""
- 또 다른 자료는 **진주시의 범죄가 연도별로 증가하고 있는 추세**를 나타냅니다.

st.image("data/crime_year.png", caption="연도별 진주시 범죄 지수", use_column_width=True) 

👉 이러한 배경 속에서, 우리는 진주시의 범죄의 특성을 파악하고 시간적, 환경적 요인을 분석하여 대책을 제안하고 싶습니다.
""")

# ─────────────────────────────
# 2. 환경적 요인과 이론적 배경
# ─────────────────────────────
st.subheader("2️⃣ 환경적 요인과 이론적 배경")

st.markdown("""
- 국내 연구에 따르면, **범죄 발생에는 환경적 요인이 큰 영향을 미친다**는 논문 다수가 존재합니다.
- 특히 CPTED 이론 (환경설계를 통한 범죄예방)은 매우 효과적인 전략으로 간주됩니다.
- 아래는 [범죄예방디자인연구정보센터]의 관련 개념 정리입니다:

📝 _[여기에 논문 요약 또는 이론 설명 이미지 혹은 인용 내용 삽입]_ 

""")

# ─────────────────────────────
# 3. 위험도 및 시설물 통계 비교
# ─────────────────────────────
st.subheader("3️⃣ 진주시 행정동별 위험도 및 방범 시설 비교")

st.markdown("위험등급과 CCTV 및 가로등 설치 현황을 행정동별로 비교한 그래프입니다.")

# 데이터 로딩
grade_df = pd.read_excel("jinju_14dong_crime_grade.xlsx")
facility_df = pd.read_csv("lamp_cctv_by_14dong.csv")

# 병합
merged_df = pd.merge(grade_df, facility_df, on="행정동", how="inner")

# 그래프
st.markdown("#### 🔢 위험등급 vs CCTV & 가로등 수")
fig, ax = plt.subplots(figsize=(12, 5))
merged_df.plot(kind='bar', x='행정동', y=['위험등급', 'CCTV 개수', '가로등 개수'], ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# ─────────────────────────────
# 4. 행정구역 + 시설 위치 지도
# ─────────────────────────────
st.subheader("4️⃣ 지도 기반 시각화")

st.markdown("""
- 아래 지도는 **행정동 경계와 함께 CCTV 및 가로등 위치**를 표시합니다.
- 사용자 인터랙션을 통해 원하는 항목만 선택해 볼 수 있도록 구현됩니다.
""")

# 지도 필터
show_cctv = st.checkbox("CCTV 위치 보기", value=True)
show_lamp = st.checkbox("가로등 위치 보기", value=True)

# 지도 데이터 예시 로딩 (위도/경도 포함된 CSV 필요)
cctv_data = pd.read_csv("jinju_cctv.csv", encoding="cp949")
lamp_data = pd.read_csv("jinju_lamp.csv", encoding="cp949")

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

🖼️ _[여기에 각 해결방안을 시각적으로 보여줄 수 있는 이미지들 삽입]_ 
""")
