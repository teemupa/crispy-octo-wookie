$(function(){


    function alertIfNeeded( temp ) {

        if (temp < 20)
        {
            $('#myModal').modal();
            $('#myModal').modal('show');
        }


    }


    var navMain = $("#navbar");
    navMain.on("click", "a", null, function () {
        navMain.collapse('hide');
    });


    // Generate bar graph
    var ctx1 = document.getElementById("humidity-canvas").getContext("2d");
    var barChartData = {
        labels : [],
        datasets : [
            {
                label: "Humidity data",
                fillColor : "rgba(151,187,205,0.5)",
                strokeColor : "rgba(151,187,205,0.8)",
                highlightFill : "rgba(151,187,205,0.75)",
                highlightStroke : "rgba(151,187,205,1)",
                data : []
            }
        ]
    }

    var barChart = new Chart(ctx1).Bar(barChartData, {
        responsive : true
    });

    // Generate bar graph
    var ctx2 = document.getElementById("temperature-canvas").getContext("2d");
    var lineChartData = {
        labels : [],
        datasets : [
            {
                label: "Temperature data",
                fillColor : "rgba(151,187,205,0.5)",
                strokeColor : "rgba(151,187,205,0.8)",
                highlightFill : "rgba(151,187,205,0.75)",
                highlightStroke : "rgba(151,187,205,1)",
                data : []
            }
        ]
    }

    var lineChart = new Chart(ctx2).Line(lineChartData, {
        responsive : true
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
        alertIfNeeded( cur_temp );
		
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
		var historyLength = historyArray.length;

        var humidityVal, temperatureVal;
		for (var i = 0; i < historyLength; i++) {
            humidityVal = Math.round(historyArray[i]["hum"] * 100) / 100;
            temperatureVal = Math.round(historyArray[i]["temp_in"] * 100) / 100
            console.log(historyArray[i]["timestamp"] + " Temp: " + historyArray[i]["temp_in"] + " Hum: " + historyArray[i]["hum"]);
            barChart.addData([humidityVal], i-historyLength);
            lineChart.addData([temperatureVal], i-historyLength);
            $(".loader").hide();
            $("canvas").show();
            barChart.update();
            $(window).resize();
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