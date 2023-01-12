import folium
from folium.plugins import MarkerCluster
from folium import Marker
import json
import pandas as pd


# 업종과 시도명을 입력했을 때, folium 맵 만들기
# 입력한 업종과 시도의 모든 업소마다 마커가 찍히고 클러스터해서 보여준다.



# 지도의 정보를 json 파일로 불러온다.
with open ("./data/geometry/sido.json", "r",encoding='utf-8') as f:
    sido_json = json.load(f)


df_sido_code = pd.read_csv('./data/df_sido_code.csv', index_col=0)
df_sido_num = pd.read_csv('./data/df_sido_num.csv', index_col=0)
df = pd.read_csv('./data/df.csv', index_col=0)
df_mid_code = pd.read_csv('./data/df_mid_code.csv', index_col=0)
df_shop = pd.read_csv('./data/df_shop.csv', index_col=0)


def sido_map_make(kind, sido):
    # 기본맵을 만든다. 
    # 좌표는 각 시도의 중심 좌표
    # tile 스타일은 stamen terrain
    m = folium.Map(location=[df_sido_code.loc[df_sido_code["name"]==sido]["lat"].values[0],df_sido_code.loc[df_sido_code["name"]==sido]["lon"].values[0]], tiles='stamen terrain', zoom_start=7)

    # result 딕셔너리에 함수 매개변수 kind와 sido를 받아서
    # 매개변수의 코드를 찾고 그 코드에 해당하는 업소정보를 받아온다.
    result= {}

    result[sido+kind]= df.loc[(df["시도코드"]==df_sido_code["code"].loc[df_sido_code["name"]==sido].values[0]) & (df["상권업종중분류코드"]==df_mid_code["code"].loc[df_mid_code["name"]==kind].values[0])]
    
    # 시도 데이터와 각 시도의 총 업소수를 맵에 표시한다.
    folium.Choropleth(
    geo_data=sido_json,
    name="sido_data",
    data=df_sido_num,
    columns=["name",'num'],
    key_on='feature.properties.CTP_KOR_NM',
    fill_color='RdYlGn',
    ).add_to(m)
    
    #위에서 받은 업소정보를 받아서 기본맵에 매개변수에 해당하는 업소의 마커를 찍는다.
    mc = MarkerCluster()
    for i in range(result[sido+kind].shape[0]):
        mc.add_child(
            Marker(location = [df_shop["lat"].loc[df_shop["code"]==result[sido+kind]["상가업소번호"].values[i]].values[0],
         df_shop["lon"].loc[df_shop["code"]==result[sido+kind]["상가업소번호"].values[i]].values[0]],
        popup=f"""{df_shop["name"].loc[df_shop["code"]==result[sido+kind]["상가업소번호"].values[i]].values[0]}
        {df_shop["address"].loc[df_shop["code"]==result[sido+kind]["상가업소번호"].values[i]].values[0]}
        """
        ))
        
    m.add_child(mc)

    
    # 그린 지도를 result.html에 저장한다.
    m.save(f'./templates/result.html')