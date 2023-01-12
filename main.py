from flask import Flask, render_template, request, redirect
from make_map import sido_map_make
from dropdown_list import df_sgg_list, df_mid_code
app = Flask(__name__)


# 메인페이지
@app.route("/")
def home():
    return render_template("index.html")

# 업소 정보 검색 페이지
# 업종과 시도명을 선택할 수 있다.
@app.route("/search/")
def search():
    return render_template("sido.html", df_sgg_list=df_sgg_list, df_mid_code=df_mid_code)

# 업소 정보 결과 페이지
# 업소 정보 검색 페이지에서 선택한 업종과 시도명에 해당하는 지도에 
# 업소 위치마다 마커를 그리고 팝업창에 상호명과 도로명주소가 나타난다.
@app.route("/resultsearch/")
def resultsearch():
    kind = request.args.get("kind")
    sido = request.args.get("sido")
    sido_map_make(kind, sido)
    return render_template("map.html",kind=kind,sido=sido, df_sgg_list=df_sgg_list, df_mid_code=df_mid_code)

# 시도별 상권 분석 데이터를 보여준다.
@app.route("/analysis/")
def analysis():
    return render_template("analysis_data.html")

if __name__ == '__main__': # Debug Mode ON
    app.run(debug=True)


