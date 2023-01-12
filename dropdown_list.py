import pandas as pd


df_sido_code =pd.read_csv('./data/df_sido_code.csv', index_col=0)
df_sgg_code = pd.read_csv('./data/df_sgg_code.csv', index_col=0)
df_hjd_code = pd.read_csv('./data/df_hjd_code.csv', index_col=0)
df_mid_code = pd.read_csv('./data/df_mid_code.csv', index_col=0)
    


df_sgg_list = {}

for i in range(len(df_sido_code["code"])):
    df_sgg_list[df_sido_code["name"][i]] = list(df_sgg_code["name"][(df_sgg_code['code'] >=df_sido_code["code"][i]*1000) & (df_sgg_code['code'] <(df_sido_code["code"][i]+1)*1000)].values)

df_hjd_list = {}

for i in range(len(df_sgg_code["code"])):
    df_hjd_list[df_sgg_code["name"][i]] = list(df_hjd_code["name"][(df_hjd_code['code'] >=df_sgg_code["code"][i]*100000) & (df_hjd_code['code'] <(df_sgg_code["code"][i]+1)*100000)].values)
    