from flask import Flask, render_template, send_from_directory


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/public/<path:path>')
def send_pulic(path):
    return send_from_directory('public', path)



if __name__ == '__main__': app.run(debug=True)
