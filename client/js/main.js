$(function(){
    var navMain = $("#navbar");
    navMain.on("click", "a", null, function () {
        navMain.collapse('hide');
    });

    var api = "http://teemupa.dy.fi:5000/api/";


    $.getJSON( api, function(data) {
	
		var cur_time = data["collection"]["items"][0]["data"][0]["value"];
		var cur_temp = data["collection"]["items"][0]["data"][1]["value"];
		var cur_hum  = data["collection"]["items"][0]["data"][2]["value"];
		
		cur_temp 	= Math.round(cur_temp * 100) / 100;
		cur_hum 	= Math.round(cur_hum * 100) / 100;
		
		$("#current-temperature").text(cur_temp);
		$("#current-humidity").text(cur_hum);
		$("#timestamp").text(cur_time);
		
    })
        .done(function() {
            console.log( "second success" );
        })
        .fail(function() {
            console.log( "error" );
        })
        .always(function() {
            console.log( "complete" );
        });
	

    $.getJSON( api+"history/", function(data) {
	

		var historyArray = data["collection"]["items"];
		var historyLenght = historyArray.length;
	
		for (var i = 0; i < historyLenght; i++) {
			console.log(historyArray[i]["timestamp"] + " Temp: " + historyArray[i]["temp_in"] + " Hum: " + historyArray[i]["hum"]);
		}	
    })
        .done(function() {
            console.log( "second success" );
        })
        .fail(function() {
            console.log( "error" );
        })
        .always(function() {
            console.log( "complete" );
        });

	
	
	
		
});