$(function(){
    var navMain = $("#navbar");
    navMain.on("click", "a", null, function () {
        navMain.collapse('hide');
    });

    var api = "http://teemupa.dy.fi:5000/api/";


    $.getJSON( api, function() {
        console.log( "success" );
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