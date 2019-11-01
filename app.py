from flask import Flask, url_for, render_template, request, flash, redirect
import pandas as pd

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def show_title():
    if request.method == 'POST':
        return redirect('accept_title')
    df = pd.read_csv('df_test.csv')
    df = df[['url', 'title']]
    return render_template('index.html', tables=df)


@app.route('/complete', methods=['GET', 'POST'])
def accept_title():
    result = []
    for key in request.form.keys():
        print(key)
        result.append(key)
    result = pd.Series(result)
    print(result)
    result.to_csv('choices.csv', header=None, encoding='utf8')
    return 'submitting '


if __name__ == '__main__':
    app.run()