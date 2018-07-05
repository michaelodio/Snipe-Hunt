
document.getElementById('file').onchange = function () {
    var st = this.value.substr(12, 20)
    st = st + "..."
    document.getElementById("fname").innerHTML = st
};