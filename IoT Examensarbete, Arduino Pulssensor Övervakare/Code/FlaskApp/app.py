from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)


script_dir = os.path.dirname(os.path.abspath(__file__))


json_file_path = os.path.join(script_dir, 'sorted_data_1.json')

with open(json_file_path, 'r') as file:
    data = [json.loads(line) for line in file]


@app.route('/path/to/app,/')
def index():
    return render_template('index.html', data=data)



@app.route('/data')
def get_data():
    return jsonify(data)

@app.route('/app/<path:custom_path>')
def custom_path(custom_path):
    return render_template('custom_template.html', custom_path=custom_path)




if __name__ == '__main__':
    app.run(debug=True)
    
    
    
# https://open.spotify.com/track/1klMdOiawDp93BwvSaYghi?si=8438b53ba83e4e88