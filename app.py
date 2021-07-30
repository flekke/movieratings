from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('mongodb://test:test@localhost', 27017)
db = client.dbhomework


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')


# API 역할을 하는 부분
@app.route('/api/list', methods=['GET'])
def show_stars():
    mystars = list(db.mystar_v.find({}, {'_id': False}).sort('like',-1))
    #위의 mystars는 아래코드에서 쓰려고 잠깐 담는 변수야. 클라이언트쪽이랑 헷갈리지 말아야해.

    # 1. db에서 mystar 목록 전체를 검색합니다. ID는 제외하고 like 가 많은 순으로 정렬합니다.
    # 참고) find({},{'_id':False}), sort()를 활용하면 굿!
    # 2. 성공하면 success 메시지와 함께 stars_list 목록을 클라이언트에 전달합니다.
    return jsonify({'result': 'success', 'mystars': mystars})


@app.route('/api/like', methods=['POST'])
def like_star():
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    # 2. mystar 목록에서 find_one으로 name이 name_receive와 일치하는 star를 찾습니다.
    # 3. star의 like 에 1을 더해준 new_like 변수를 만듭니다.
    # 4. mystar 목록에서 name이 name_receive인 문서의 like 를 new_like로 변경합니다.
    # 참고: '$set' 활용하기!
    # 5. 성공하면 success 메시지를 반환합니다.

    name_receive = request.form['name_give']

    current_like = db.mystar_v.find_one({'name': name_receive})['like']


    new_like = current_like+1
    db.mystar_v.update_one({'name': name_receive}, {'$set': {'like':new_like}})

    return jsonify({'result': 'success', 'msg': 'thanks!'})


@app.route('/api/delete', methods=['POST'])
def delete_star():
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    # 2. mystar 목록에서 delete_one으로 name이 name_receive와 일치하는 star를 제거합니다.
    # 3. 성공하면 success 메시지를 반환합니다.
    name_receive2 = request.form['name_give']

    current_like2 = db.mystar_v.find_one({'name': name_receive2})['like']

    new_like2 = current_like2 - 1
    db.mystar_v.update_one({'name': name_receive2}, {'$set': {'like': new_like2}})

    return jsonify({'result': 'success', 'msg': 'thanks!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=4000, debug=True)