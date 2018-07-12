$(document).ready(
    function() {
        alert("hi");
        $('.list-group-item').on('click', function() {
            $('.glyphicon', this).toggleClass('glyphicon-chevron-right').toggleClass('glyphicon-chevron-down');
            alert("there");
        });

    }
);