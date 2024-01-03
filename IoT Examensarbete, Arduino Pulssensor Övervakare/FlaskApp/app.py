from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.get_data().decode('utf-8')
    print(f'Received data: {data}')

    return 'Data received successfully'

if __name__ == '__main__':
    app.run(debug=True)
