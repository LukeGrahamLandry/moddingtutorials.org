// HTTP

function httpGetPlaintext(url){
    url = url + ((/\?/).test(url) ? "&" : "?") + "time=" + (new Date()).getTime()  // make sure not cached

    let xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", url, false); // synchronous
    xmlHttp.send();
    let response = xmlHttp.responseText;
    return response;
}

function httpGet(url){
    let response_str = httpGetPlaintext(url);
    let response = JSON.parse(response_str);
    return response;
}

// COOKIES 

function setCookie(cname,cvalue,exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires=" + d.toGMTString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}
function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return null;
}
function delCookie(cname){
    setCookie(cname, "", -1);
}

function updateDarkmode(){
    let dark = document.getElementById("dark") == undefined ? true : document.getElementById("dark").checked;
    if (getCookie("darkmode") != null) {
        dark = getCookie("darkmode");
    }

    let sheet;
    if (dark){
        sheet = "/styles/dark.css";
    } else {
        sheet = "";
    }
    document.getElementById("theme").href = sheet;
    setCookie("darkmode", dark, 365);
}

// set darkmode from cookie
if (getCookie("darkmode")) {
    if (document.getElementById("dark") != undefined){
        document.getElementById("dark").checked = true;
    }
    
    updateDarkmode();
}


// stream notification
function checkStream(){
    let API_KEY = "AIzaSyBqwRckp6kyEQK7yXNI4OhmRDGSEEUrgKk";
    let channelId = "UC8gYhA5SkhI1tajZ5JF2pbQ";

    let getStreamURL = "https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=" + channelId + "&eventType=live&type=video&key=" + API_KEY;
    let streamData = httpGet(getStreamURL);
    if (streamData["error"] != undefined){
        console.log("youtube api key used on invalid site. PLEASE DONT STEAL MY CODE :) - LukeGrahamLandry#6888");
    } else if (streamData["items"].length == 0) {
        console.log("no stream found");
    } else {
        let url = "https://youtube.com/watch?v=" + streamData["items"][0]["id"]["videoId"];
        let img = streamData["items"][0]["snippet"]["thumbnails"]["default"]["url"];
        let title = streamData["items"][0]["snippet"]["title"];

        console.log("found stream: " + title);
    
        let code = '<a class="video" href="' + url + '" target="_blank" id="videolink">'
        code += '<img alt="stream thumbnail" src="' + img + '" id="videoimg">'
        code += '<div style="position: absolute; bottom: 3rem; right: 25px; color: red; background-color: white; border-radius: 25px; padding: 3px; font-size: 0.75rem; font-weight: 1000;">&#x2B24; LIVE</div>'
        code += '<b class="title" id="videotitle"> ' + title + ' </b>';
        code += '</a>';
    
        let elements = document.getElementsByClassName("embedstream");
        for (let i=0;i<elements.length;i++){
            let element = elements[i];
            element.innerHTML = code;
        }
    }
}
// setTimeout(checkStream, 1);