$(function(){
    var navMain = $("#navbar");
    navMain.on("click", "a", null, function () {
        navMain.collapse('hide');
    });


    (function worker() {
        $.get('ajax/test.html', function(data) {
            // Now that we've completed the request schedule the next one.
            $('.result').html(data);
            setTimeout(worker, 5000);
        });
    })();

    (function worker() {
        $.ajax({
            url: 'ajax/test.html',
            success: function(data) {
                $('.result').html(data);
            },
            complete: function() {
                // Schedule the next request when the current one's complete
                setTimeout(worker, 5000);
            }
        });
    })();

});