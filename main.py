from flask import Flask, request, make_response, render_template, redirect, url_for, session
import datetime
import database
import dbconn
import pymysql
import pandas as pd
import crud
import io
import chart
import labels

app = Flask(__name__)

now = datetime.datetime.now()
today = now.strftime("%Y-%m-%d")

#app.config["SECRET_KEY"] = 'd2707fea9778e085491e2dbbc73ff30e'

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'djdhrirhek3393jdhdkeidhekdos03kdowejs828282'

sunny = 'sunny' # sunny table name

@app.after_request
def add_header(resp):
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"

    return resp

@app.route('/')
def home():
    if session :
        return render_template('home.html')
    else :
        return redirect(url_for('login'))

@app.route('/login', methods=["POST","GET"])
def login():
    if request.method == 'POST' and 'email' in request.form :
        email = request.form['email']
        account = dbconn.Database().executeOne(f"select email, name from user where email='{email}'")

        if account :
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['email'] = account['email']
            session['name'] = account['name']
            # Redirect to home page
            return redirect(url_for('home'))
        else :
            return render_template('login.html',err=True)
    else :
        return render_template('login.html', err=False)

@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html', err=False)


@app.route('/assessment')
def assessment():
    if not session :
        return render_template('login.html', err=False)

    # 평가 페이지
    #form = Questions()
    # db update record

    db_class = dbconn.Database()
    sql = "select record from sunny"
    rows = db_class.executeAll(sql)
    records = [r['record'] for r in rows]
    record = 0
    try :
        record = max(records) + 1
    except :
        record += 1

    # insert record
    CRUD = crud.CRUD()
    CRUD.insertDB(sunny, 'record', record)

    CRUD = crud.CRUD()
    CRUD.updateDB(sunny, 'answerdate', today, f'record = {record}')
    CRUD.updateDB(sunny, 'interviewer', session['email'], f'record = {record}')

    datas = dbconn.Database().executeAll(f'select * from {sunny} where record={record};')[0]
    datas = {col: '' if val == None else val for col, val in datas.items()}

    return render_template('assessment.html', today=today, datas=datas)

@app.route('/result/<string:pagetype>', methods=['POST','GET'])
def result(pagetype):
    # 모든 결과 데이터
    if session :
        if request.method == 'POST' :
            result = request.form
            result = dict(result)
            #print(result)

            record = result['record']
            del result['record']

            # update data
            CRUD = crud.CRUD()
            for col, val in result.items() :
                CRUD.updateDB(sunny, col, val, f'record = {record}')

            if pagetype == "assessment" :
                status = "사전 완료"
                CRUD.updateDB(sunny, 'status', f'{status}', f'record = {record}')
            if pagetype == "postquestion" :
                status = "평가 완료"
                CRUD.updateDB(sunny, 'status', f'{status}', f'record = {record}')
                datas = dbconn.Database().executeAll(f'select * from {sunny} where record = {record};')
                df = pd.DataFrame(datas)
                tot = df.loc[0, 'Q1_1':'Q3_5'].sum()

                # 총 평가 점수
                CRUD.updateDB(sunny, 'total', tot, f'record = {record}')

            if pagetype == "final":
                datas = dbconn.Database().executeAll(f'select * from {sunny} where record = {record};')
                df = pd.DataFrame(datas)
                tot = df.loc[0, 'Q1_1':'Q3_5'].sum() + df.loc[0, 'extra_score'].sum()

                # 총 평가 점수
                CRUD.updateDB(sunny, 'total', tot, f'record = {record}')

            # validate
            return render_template('result.html', pagetype=pagetype, record=record)
    else :
        return redirect(url_for('login'))

@app.route('/datacheck', methods=['POST','GET'])
def datacheck():
    if not session :
        return render_template('login.html', err=False)

    # checked delete
    if request.method == 'POST' :
        checked_data = request.form.getlist('checkdata')
        CRUD = crud.CRUD()
        #print(checked_data)
        for record in checked_data :
            CRUD.deleteDB(sunny, f'record={record}')

    # data 확인 페이지
    datas = dbconn.Database().executeAll(f"select * from {sunny} where status='사전 완료' or status='평가 완료' order by record desc ;")
    for idx, d in enumerate(datas) :
        newd = {col:'' if val==None else val for col, val in d.items()}
        datas[idx] = newd

    position_label = labels.posistion_label()

    return render_template('datacheck.html', datas=datas, position_label=position_label)

@app.route('/download')
def download():
    # to excel
    all_data = dbconn.Database().executeAll(f"select * from {sunny} where status='사전 완료' or status='평가 완료' order by record desc;")
    df = pd.DataFrame(all_data)
    df.set_index('record', inplace=True)

    out = io.BytesIO()
    writer = pd.ExcelWriter(out, engine='xlsxwriter')

    df.to_excel(excel_writer=writer, sheet_name="answer")
    writer.save()
    writer.close()

    excel_file =make_response(out.getvalue())
    excel_file.headers["Content-Disposition"] = "attachment; filename=wonderwall_interview_data.xlsx"
    excel_file.headers["Content-type"] = "application/x-xls"

    return excel_file

@app.route('/listcheck/<int:record>')
def listcheck(record):
    if not session :
        return render_template('login.html', err=False)

    # list 확인 페이지
    datas = dbconn.Database().executeAll(f'select * from {sunny} where record={record};')[0]
    datas = {col:'' if val==None else val for col, val in datas.items()}
    return render_template('listcheck.html', datas=datas)

@app.route('/editdata/<int:record>')
def editdata(record):
    if not session :
        return render_template('login.html', err=False)

    # date edit page
    datas = dbconn.Database().executeAll(f'select * from {sunny} where record={record};')[0]
    datas = {col:'' if val==None else val for col, val in datas.items()}
    return render_template('editdata.html', datas=datas)

@app.route('/deletedata/<int:record>')
def deletedata(record):
    if not session :
        return render_template('login.html', err=False)

    # date delete page
    CRUD = crud.CRUD()
    CRUD.deleteDB(sunny, f'record={record}')
    return redirect(url_for('datacheck'))


@app.route('/showboard/<int:record>')
def showboard(record):
    if not session :
        return render_template('login.html', err=False)

    all_datas = dbconn.Database().executeAll(f'select * from {sunny};')
    df = pd.DataFrame(all_datas)

    datas = dbconn.Database().executeAll(f'select * from {sunny} where record={record};')[0]
    datas = {col:'' if val==None else val for col, val in datas.items()}

    Q1_df = df.loc[df['record']==record,['pname','Q1_1','Q1_2','Q1_3','Q1_4','Q1_5']]
    Q1_df.columns = ['pname','마케팅 이해도','분석/전략적 사고','트렌드 파악 능력','콘텐츠 생산 능력','브랜드 캠페인 경험']

    Q2_df = df.loc[df['record'] == record, ['pname', 'Q2_1', 'Q2_2', 'Q2_3', 'Q2_4', 'Q2_5']]
    Q2_df.columns = ['pname', '직무 관련 경험', '업종 관련 경험', '서비스 관심/이해도', '학습 능력', '협업 능력']

    Q3_df = df.loc[df['record'] == record, ['pname', 'Q3_1', 'Q3_2', 'Q3_3', 'Q3_4', 'Q3_5']]
    Q3_df.columns = ['pname', '커리어 선명도', '문제 해결 능력', '학습 능력', '적극성', '성실도']

    spider = {}
    spider['Q1'] = ["마케팅 역량", chart.spider_chart(Q1_df.to_dict('list'))]
    spider['Q2'] = ["직무 적합성", chart.spider_chart(Q2_df.to_dict('list'))]
    spider['Q3'] = ["성장 가능성", chart.spider_chart(Q3_df.to_dict('list'))]

    return render_template('showboard.html',spider=spider, datas=datas)

@app.route('/compareboard', methods=['POST','GET'])
def compareboard():
    if not session :
        return render_template('login.html', err=False)

    datas = dbconn.Database().executeAll(f"select * from {sunny} where status='사전 완료' or status='평가 완료' order by record desc ;")
    for idx, d in enumerate(datas) :
        newd = {col:'' if val==None else val for col, val in d.items()}
        datas[idx] = newd

    position_label = labels.posistion_label()

    if request.method == 'POST' :
        checked_data = request.form.getlist('checkdata')
        checked_data = [int(i) for i in checked_data ]
        all_datas = dbconn.Database().executeAll(f'select * from {sunny};')
        df = pd.DataFrame(all_datas)

        Q1_df = df.loc[df['record'].isin(checked_data),['pname','Q1_1','Q1_2','Q1_3','Q1_4','Q1_5']]
        print(Q1_df.to_dict('list'))
        Q1_df.columns = ['pname','마케팅 이해도','분석/전략적 사고','트렌드 파악 능력','콘텐츠 생산 능력','브랜드 캠페인 경험']

        Q2_df = df.loc[df['record'].isin(checked_data), ['pname', 'Q2_1', 'Q2_2', 'Q2_3', 'Q2_4', 'Q2_5']]
        Q2_df.columns = ['pname', '직무 관련 경험', '업종 관련 경험', '서비스 관심/이해도', '학습 능력', '협업 능력']

        Q3_df = df.loc[df['record'].isin(checked_data), ['pname', 'Q3_1', 'Q3_2', 'Q3_3', 'Q3_4', 'Q3_5']]
        Q3_df.columns = ['pname', '커리어 선명도', '문제 해결 능력', '학습 능력', '적극성', '성실도']

        spider = {}
        spider['Q1'] = ["마케팅 역량", chart.spider_chart(Q1_df.to_dict('list'))]
        spider['Q2'] = ["직무 적합성", chart.spider_chart(Q2_df.to_dict('list'))]
        spider['Q3'] = ["성장 가능성", chart.spider_chart(Q3_df.to_dict('list'))]

        return render_template('compare.html',spider=spider, datas=datas)

    else :
        return render_template('datacheck.html', datas=datas, position_label=position_label)


@app.route('/postQuestion/<int:record>')
def postQuestion(record):
    if not session :
        return render_template('login.html', err=False)
        
    # list 확인 페이지
    Qdict = {
        "Q1" : {
            "big_title" : "마케팅 역량",
            "rows" : {
                1 : "(디지털) 마케팅 이해도",
                2 : "(데이터 기반) 분석/전략적 사고",
                3 : "트렌드 파악 능력",
                4 : "콘텐츠 생산 능력",
                5 : "브랜드 캠페인 경험"
            }
        },
        "Q2": {
            "big_title": "직무 적합성",
            "rows": {
                1: "직무 관련 경험",
                2: "업종 관련 경험(콘텐츠/서비스)",
                3: "서비스 관심/이해도",
                4: "커뮤니케이션 능력",
                5: "협업 능력"
            }
        },
        "Q3": {
            "big_title": "성장 가능성",
            "rows": {
                1: "커리어 선명도",
                2: "문제 해결 능력",
                3: "학습 능력",
                4: "적극성",
                5: "성실도"
            }
        }
    }
    datas = dbconn.Database().executeAll(f'select * from {sunny} where record={record};')[0]
    datas = {col:'' if val==None else val for col, val in datas.items()}
    return render_template('postQuestion.html', Qdict=Qdict, datas=datas)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)