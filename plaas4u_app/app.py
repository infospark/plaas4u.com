from flask import Flask
from plaas4u_app import playing
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
    farms = playing.get_farms_from_csv()
    for f in farms:
        html += f"<tr><td>Farm {f['Listing number']}</td><td>{f['Size (ha)']}Ha</td></tr>"
    html += "</table>"
    return html