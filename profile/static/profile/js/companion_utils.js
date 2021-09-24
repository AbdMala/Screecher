function loadProfileInfo() {
    // TODO: implement
    const xmlhttp = new XMLHttpRequest();
    xmlhttp.open('GET', 'https://team13.screecher.de/profile/json/', false);
    xmlhttp.send();
    return JSON.parse(xmlhttp.responseText);

}

window.onload = function () {
    let data = loadProfileInfo();
    for (let key in data) {
        if (data.hasOwnProperty(key)) {
            let value = data[key];
            let el = document.getElementById(key);
            if (el) el.innerText = value;
        }
    }
}
