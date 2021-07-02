from flask import Flask, render_template, request
from plaas4u_app import Farms

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    farm_list = Farms.get_farms_from_csv()
    # Get Min_Size - if there nothing there assume min size of 0
    min_size = Farms.extract_float_from_string(request.form["min_size"], 0)
    # Get Max_Price - if there nothing there assume max price of 99999999
    max_price = Farms.extract_float_from_string(request.form["max_price"], 99999999)

    # TODO: Discuss the way we keep reusing the farm_list here with Nico
    farm_list = Farms.filter_by_min_max(farm_list, "Size (ha)", min_size, 99999999)
    farm_list = Farms.filter_by_min_max(farm_list, "Price (Rand)", 0, max_price)
    html = render_template('search.html', farm_list=farm_list)
    return html

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