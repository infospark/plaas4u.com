from flask import Flask, render_template, request
from plaas4u_app import Farms

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    filtered_farms = Farms.get_farm_from_json()
    # Get Min_Size - if there nothing there assume min size of 0
    min_size = Farms.extract_float_from_string(request.form["min_size"])
    # Get Max_Price - if there nothing there assume max price of 99999999
    max_price = Farms.extract_float_from_string(request.form["max_price"], 99999999)

    min_ha_to_wine = Farms.extract_float_from_string(request.form["min_ha_to_wine"], 99999999)

    has_wine = False
    if "has_wine" in request.form:
        has_wine = True

    filtered_farms = Farms.filter_dict_by_min_max(filtered_farms, "size", "hectares", min_size, 99999999)
    filtered_farms = Farms.filter_dict_by_min_max(filtered_farms, "price", "rand", 0, max_price)
    if has_wine:
        filtered_farms = Farms.filter_dict_by_property(filtered_farms, "wine")
        filtered_farms = Farms.filter_dict_by_min_max(filtered_farms, "wine", "hectares", min_ha_to_wine, 99999999)

    html = render_template('search.html', farm_list=filtered_farms)
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

@app.route('/index')
def terrain():
    return render_template('index.html')
