


# python server
# 1) flask:마이크로 웹 프레임워트 : 작아
# 2) Django: 모든 기능이 포함되어 flask보다 무거움
# 우측 하단 Python -> hm 선택하기 
# Ctrl+Shift+P 



from flask import Flask # route 경로, run 서버 실행 
from flask import render_template # html 로드
from flask import request # 사용자가 보내는 정보
from flask import redirect, make_response

#aws.py 안에 있는 detect~ 함수만 가져다가 쓰기
from aws import detect_labels_local_file
from aws import compare_faces as cf # 호출하는 클래스의 함수와 동일한 이름이라 alias 줘서 구분했음

# 파일 이름 보안 처리 라이브러리
from werkzeug.utils import secure_filename
# IPv4: IP version 4
# 8bit*4 형식
# 

import os
# static 폴더가 없으면 만들기
if not os.path.exists("static"):
    os.mkdir("static")

app = Flask(__name__)
@app.route("/")
def index():
    # return "웹페이지"
    # return render_template("exam06.html")
    return render_template("index.html")

@app.route("/login", methods=["GET"])
def login():
    if request.method == "GET":
      
        # 페이지 이동: redirect
            # 관련 라이브러리 ---> flask.redirect
        # 페이지가 이동하더라도
        # 정보를 남겨 사용 ??
        login_id = request.args["login_id"]
        login_pw = request.args["login_pw"]
        # 로그인 성공 판단 여부
        if login_id == "arkrg" and login_pw == "1234":
            # 로그인 성공
            response = make_response(redirect("/login/success"))
            # ㄴ 응답개체 ㄴ정보를 저장할 수 있는 moment
            response.set_cookie("user", login_id)
            return response
        else:
            #ㄺㅇㅅㅍ
            return redirect("/")
    return "로그인 성공"

@app.route("/login/success", methods =["GET"])
def login_success():
    login_id = request.cookies.get("user")
    return f"{login_id}님 환영합니다2"

@app.route("/secret", methods =["POST"])
def box():
    try:
        if request.method == "POST":
            hidden = request.form["hidden"]
            return f"비밀: {hidden}"
    except:
        return "데이터 전송 실패"

@app.route("/detect", methods =["POST"])
def detect_label():
    #객체 탐지하는 파이썬 파일을 불러와서 사용 --> 모듈화
    #flask에서 보안 규칙상 파일 이름을 secure 처리 해야 함
    #    ㄴ secure_filename 
    if request.method == "POST":
        file = request.files["file"]
        # file을 static 폴더에 저장하고
        # 보안처리
        file_name = secure_filename(file.filename)
        file.save("static/" + file_name)
        # 해당 경로를 detect_lo~ 함수에 전달
        r = detect_labels_local_file("static/"+file_name)
    return r


@app.route("/compare", methods =["POST"])
def compare_faces(): 
    # / detect랑 내용 비슷
    # 1. compare로 오는 file1, file2 받아서 static폴더에 저장
    # 2. secure_filename 사용하기
    # 3. aws.py 얼굴비교 aws 코드
    # 결과를 통에 웹 페이지에
    # 동일 인물일 확률은 ~입니다.
    # 4.aws.py 안에 함수 불러와서
    # exam01.py 사용하기 
    if request.method == "POST":
        file1 = request.files["file1"]
        file2 = request.files["file2"]
    
        file1_filename = secure_filename(file1.filename)
        file2_filename = secure_filename(file2.filename)

        file1.save("static/" + file1_filename)
        file2.save("static/" + file2_filename)

        r = cf("static/"+file1_filename, "static/"+file2_filename)
        return r

if __name__ == "__main__":
    app.run(host="0.0.0.0")

