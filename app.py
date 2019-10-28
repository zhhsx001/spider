from flask import Flask,url_for


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def show_title():
    return index.html


@app.route('/submit')
def accept_title():
    print('submiting')
    print('func run')
    print('end')
    return 'submiting'


@app.route('/test')
def test():
    print(url_for('accept_title'))
    return 'absftest'


app.run()