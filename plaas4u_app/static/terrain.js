initialPitch = 65.4976076616079;
initialZoom = 13.678051144949984;
initialBearing = 116.00000000000001;
initialLngLat = [19.032408594723847, -33.62033749723255]

mapboxgl.accessToken = 'pk.eyJ1IjoiamltcGxhbnQtaW5mb3NwYXJrIiwiYSI6ImNrM2l1MWk3MjBiNXkzbXA2N3JwOWttemMifQ.sZg_mO5-QbAoD-A0pzTYpQ';
const map = new mapboxgl.Map({
    container: 'map', // container ID
    style: 'mapbox://styles/jimplant-infospark/ck4iwrpym0kna1ctbwws3pydn', // style URL
    center: initialLngLat, // starting position [lng, lat]
    pitch: initialPitch,
    bearing: initialBearing,
    zoom: initialZoom,
});

map.addControl(new mapboxgl.NavigationControl());
/*
map.on("pitch", (e) => {
    $('#pitch').html('pitch: ' + e.target.getPitch());
});
map.on("zoom", (e) => {
    $('#zoom').html('zoom: ' + e.target.getZoom());
});
map.on("rotate", (e) => {
    $('#bearing').html('bearing: ' + e.target.getBearing());
})
map.on("move", (e) => {
    $('#lnglat').html('lnglat: ' + e.target.getCenter());
})
*/
// Create a default Marker and add it to the map.
//const marker1 = new mapboxgl.Marker()
//    .setLngLat([19.031606074866507, -33.6656488982348])
//    .addTo(map);

 function loadJSON(file, callback) {

    var xobj = new XMLHttpRequest();
        xobj.overrideMimeType("application/json");
    xobj.open('GET', file, true); // Replace 'my_data' with the path to your file
    xobj.onreadystatechange = function () {
          if (xobj.readyState == 4 && xobj.status == "200") {
            // Required use of an anonymous callback as .open will NOT return a value but simply returns undefined in asynchronous mode
            callback(xobj.responseText);
          }
    };
    xobj.send(null);
 }

map.on('load', () => {
    loadJSON('static/geojson.json', function(response) {
      // Parse JSON string into object
        var geo_json = JSON.parse(response);

        map.addSource('wine_points', {
          "type": "geojson",
            "data": {
                "type": "FeatureCollection",
                "features": geo_json
                }
        });

        map.addLayer({
            'id': 'wine_points',
            'type': 'symbol',
            'source': 'wine_points', // reference the data source
            'layout': {
                //'icon-image': 'wine', // reference the image
                'icon-image': ['get', 'icon'],
                'icon-size': 0.15
            }
        });
        // When a click event occurs on a feature in the places layer, open a popup at the
    // location of the feature, with description HTML from its properties.
    map.on('click', 'wine_points', (e) => {
        // Copy coordinates array.
        const coordinates = e.features[0].geometry.coordinates.slice();
        const description = e.features[0].properties.description;

        // Ensure that if the map is zoomed out such that multiple
        // copies of the feature are visible, the popup appears
        // over the copy being pointed to.
        while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
            coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
        }

        new mapboxgl.Popup()
            .setLngLat(coordinates)
            .setHTML(description)
            .addTo(map);
            });


    });
    loadJSON('static/geojsonfruit.json', function(response) {
      // Parse JSON string into object
        var geo_json_fruit = JSON.parse(response);
    });

    map.loadImage(
        'static/cape_dutch_wine.png',
        (error, image) => {
            if (error) throw error;

        // Add the image to the map style.
        map.addImage('wine', image);
        }
     );

    map.loadImage(
        'static/cape_dutch.png',
        (error, image) => {
            if (error) throw error;

        // Add the image to the map style.
        map.addImage('orange', image);
        }
    );

    // Change the cursor to a pointer when the mouse is over the places layer.
    map.on('mouseenter', 'wine_points', () => {
        map.getCanvas().style.cursor = 'pointer';
    });

    // Change it back to a pointer when it leaves.
    map.on('mouseleave', 'wine_points', () => {
        map.getCanvas().style.cursor = '';
    });



});