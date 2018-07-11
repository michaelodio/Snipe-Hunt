$(document).ready(function() {
    var progression = 0,
    progress = setInterval(function() 
    {
    $('#progressbox .progress-text').text(progression + '%');
	$('#progressbox .progress-bar').css({'aria-valuenow':progression});
	$('#progressbox .progress-bar').css({'width': progression + '%'});
        if(progression == 100) {
            clearInterval(progress);
        } else
            progression += 1;

    }, 2000);
});