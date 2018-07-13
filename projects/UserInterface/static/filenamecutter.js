
document.getElementById('file').onchange = function () {
    var str = this.value.substr(12);
    if(str.length > 20) {
        str = str.substr(0, 20);
        str = str + "...";
    }
    document.getElementById("fname").innerHTML = str;
};
