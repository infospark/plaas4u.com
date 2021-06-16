from flask import Flask
app = Flask(__name__)

@app.route('/')
def root():
    return '<h1>Hello, World!</h1>'

@app.route('/Test')
@app.route('/test')
def test():
    return '<h1>This is a test.</h1>'

@app.route('/farms')
def farms():
    html = "<table>"
    html += "<tr><th>Name</th><th>Size</th></tr>"
    html += "<tr><td>Farm 1</td><td>100Ha</td></tr>"
    html += "<tr><td>Farm 2</td><td>50Ha</td></tr>"
    html += "</table>"
    return html