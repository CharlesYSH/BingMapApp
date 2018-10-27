

function loadMapScenario() {
	map = new Microsoft.Maps.Map(document.getElementById('myMap'), {center: new Microsoft.Maps.Location(23.725, 121),
		zoom: 8, showDashboard: false});
		
	//directionsManager = new Microsoft.Maps.Directions.DirectionsManager(map);
	Microsoft.Maps.Events.addHandler(map, 'dblclick', function (e) { handleArgs('mapClick', e); });
	Microsoft.Maps.Events.addHandler(map, 'click', function (e) { handleArgs('mapClick', e); });
}


function handleArgs(id, e) {
	//alert((e.getY()));
	var point = new Microsoft.Maps.Point(e.getX(), e.getY());
    var locTemp = e.target.tryPixelToLocation(point);
    var eventLocation = new Microsoft.Maps.Location(locTemp.latitude, locTemp.longitude);
	
	//alert(eventLocation);
}


/*
function searchroute(){
	Microsoft.Maps.loadModule('Microsoft.Maps.Directions', function () {
		var directionsManager = new Microsoft.Maps.Directions.DirectionsManager(map);
		// Set Route Mode to driving
		directionsManager.setRequestOptions({ routeMode: Microsoft.Maps.Directions.RouteMode.driving });
		var waypoint1 = new Microsoft.Maps.Directions.Waypoint({ address: '新竹'});
		var waypoint2 = new Microsoft.Maps.Directions.Waypoint({ address: '台中'});
		var waypoint3 = new Microsoft.Maps.Directions.Waypoint({ address: '台南'});
		directionsManager.addWaypoint(waypoint1);
		directionsManager.addWaypoint(waypoint2);
		directionsManager.addWaypoint(waypoint3);
		// Set the element in which the itinerary will be rendered
		//directionsManager.setRenderOptions({ itineraryContainer: document.getElementById('printoutPanel') });
		directionsManager.calculateDirections();
	});
}

function clearRoute(){
	Microsoft.Maps.loadModule('Microsoft.Maps.Directions', function () {
		var directionsManager = new Microsoft.Maps.Directions.DirectionsManager(map);
		directionsManager.clearAll();
		directionsManager.calculateDirections();
	});
}*/

function pushPinCenter(){
	var pushpin = new Microsoft.Maps.Pushpin(map.getCenter(), { color: 'red' });
	map.entities.push(pushpin);
}

function pushPin(latitude, longitude){
	var pushpin = new Microsoft.Maps.Pushpin( new Microsoft.Maps.Location(latitude, longitude), { color: 'red' });
	map.entities.push(pushpin);
}

function clearAllPin(){
	map.entities.clear();
}

function findPinIndex(latitude, longitude){
	for  (var i = map.entities.getLength() - 1; i >= 0; i--){
		var pushpinLoc = map.entities.get(i).getLocation();
		if(pushpinLoc.latitude == latitude && pushpinLoc.longitude == longitude){
			return i;
		}
	}
	return -1;
}

function pushPin(latitude, longitude){
	var pushpin = new Microsoft.Maps.Pushpin( new Microsoft.Maps.Location(latitude, longitude), null);
	map.entities.push(pushpin);
}

function showTraffic(){
	Microsoft.Maps.loadModule('Microsoft.Maps.Traffic', function () {
		manager = new Microsoft.Maps.Traffic.TrafficManager(map);
		manager.show();
		manager.hideIncidents();
	});
}

function hideTraffic(){
	Microsoft.Maps.loadModule('Microsoft.Maps.Traffic', function () {
		var manager = new Microsoft.Maps.Traffic.TrafficManager(map);
		manager.show();
		manager.hide();
	});
}

function setMapAerial(){
	map.setMapType(Microsoft.Maps.MapTypeId.aerial);
}

function setMapRoad(){
	map.setMapType(Microsoft.Maps.MapTypeId.road);
}