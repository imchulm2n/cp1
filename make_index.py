import folium
from folium.plugins import MarkerCluster
from folium import Marker
import json
import pandas as pd


# 메인화면 전국지도 그리기
# 각 시도의 중심에 마커, 클릭하면 시도명과 총 점포수가 나오도록함



# 전국 지도 정보를 가진 json파일을 불러온다.
with open ("./data/geometry/sido.json", "r",encoding='utf-8') as f:
    sido_json = json.load(f)

df_sido_code = pd.read_csv('./data/df_sido_code.csv', index_col=0)
df_sido_num = pd.read_csv('./data/df_sido_num.csv', index_col=0)


# 우리나라 지도의 중심 좌표로 기본 맵을 그린다.

m = folium.Map(location=[36, 128], tiles='stamen terrain', zoom_start=7)


# 각 시도의 총 업소 수를 데이터로 컬러맵을 그린다.
folium.Choropleth(
    geo_data=sido_json,
    name="sido_data",
    data=df_sido_num,
    columns=["name",'num'],
    key_on='feature.properties.CTP_KOR_NM',
    fill_color='RdYlGn',
    ).add_to(m)

# 각 시도의 중심에 마커를 그리고 팝업에 시도명과 시도의 총 업소수를 나타낸다.
for i in range(df_sido_code.shape[0]):
    Marker(location = [df_sido_code.iloc[i][2], df_sido_code.iloc[i][3]],
        popup=f"""{df_sido_code.iloc[i][1]}
        {df_sido_num["num"][i]}
        """
        ).add_to(m)

# 그린 지도를 sido.html에 저장한다.
m.save('./templates/sido.html')