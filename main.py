from flask import Flask, render_template, jsonify
import json
from TwitterManager import Twitter , hashtag


Tapp=Twitter(hashtag)

Tapp.searchKey(hashtag)
Tapp.getTweet()
Tapp.logger()
Tapp.browser.quit()


app = Flask(__name__)

with open('tweetlistlike.json', 'r', encoding='utf-8') as file:
    data=json.load(file)


@app.route('/')
def index():
    
    return render_template('index.html', datas = data)

if __name__ == '__main__':
    
    app.run(debug=True, use_reloader=False)
