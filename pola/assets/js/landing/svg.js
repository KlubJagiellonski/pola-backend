(function (doc) {
    var container = document.getElementById('svg-container');
    var xhr = new XMLHttpRequest();
    xhr.onload = function () {
        container.innerHTML = this.responseText;
    }
    xhr.open('get', path_config.symbols, true);
    xhr.send();
})(document)
