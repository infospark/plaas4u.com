from flask import Flask, render_template
from plaas4u_app import Farms
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/farms')
def farms():
    html = "<table>"
    html += "<tr><th>Name</th><th>Size</th></tr>"
    farms = Farms.get_farms_from_csv()
    for f in farms:
        html += f"<tr><td>Farm {f['Listing number']}</td><td>{f['Size (ha)']}Ha</td></tr>"
    html += "</table>"
    return html