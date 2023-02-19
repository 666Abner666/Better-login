from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
import pymongo

app = Flask(__name__)
app.debug = True
app.secret_key = 'secret_key'
client = MongoClient()
db = client['example']
users = db['users']

# 连接MongoDB
client = pymongo.MongoClient(
    "mongodb+srv://Abner:<Abner666>@virus2.lshuthg.mongodb.net/?retryWrites=true&w=majority")
# db = client.test
db = client['mydatabase']

users = db['users']

# 定义数据库
# mydb = client["mydatabase"]

# 定义集合
# mycol = mydb["customers"]

# 插入数据
mydict = { "name": "John", "address": "Highway 37" }
x = users.insert_one(mydict)
# x = mycol.insert_one(mydict)

# 查询数据
for x in users.find():
  print(x)

# 已经注册用户的列表
users = [
    {'id': '1', 'username': 'xiaotong', 'password': '123456'},
    {'id': '2', 'username': 'xiaomei', 'password': '000000'},
    {'id': '3', 'username': 'xiaoming', 'password': '888888'}
]


def find(username):
    '''
        根据用户名查找是否已经注册，如果是，返回用户的全部信息，如果不是，返回None
    '''
    for user in users:
        if user['username'] == username:
            return user
    return None


@app.route('/')
def index():
    return render_template('index.html')
    # return "111"


@app.route('/register', methods=['GET', 'POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        # 判断注册用户是否以存在
        user = find(username)
        if user is not None:
            return render_template('index.html', msg='已被注册')

        else:  # 未被注册的情况
            user = {'id': len(users)+1, 'username': username,
                    'password': password}
            users.append(user)
            return render_template('index.html', msg='注册成功')

    # user = {'username': username, 'password': password}
    # users.insert_one(user)
    # return redirect(url_for('index'))


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = find(username)
    if user is None:
        return render_template('index.html', username=username, user_msg='用户名不存在')
    if user['password'] != password:
        return render_template('index.html', username=username, pass_msg='密码错误，请重试')
    return render_template('index.html')

    # user = users.find_one({'username': username, 'password': password})
    # if user:
    #     session['username'] = username
    # return redirect(url_for('index'))


@app.route('/login', methods=['GET'])
def login2():
    return render_template('index.html')


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# if __name__ == '__main__':
#     app.run(host='127.0.0.1', port=8000)


# app.run(host='127.0.0.1', port=8000)
