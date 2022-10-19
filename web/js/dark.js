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
        document.getElementById("dark").checked = getCookie("darkmode") === "true";
    }
    
    updateDarkmode();
}

window.plausible = window.plausible || function() { (window.plausible.q = window.plausible.q || []).push(arguments) }

function addGoalLinkEvents(){
    let goals = ["discord", "patreon", "github", "commissions"]
    let urls = goals.map((goal) => document.location.origin + "/" + goal)
    let links = document.getElementsByTagName("a");
    for (let i=0;i<links.length;i++){
        for (let g=0;g<goals.length;g++){
            if (links[i].href == urls[g]){
                links[i].onclick = () => plausible('Redirect', {props: {target: goals[g]}});
            }
        }
    }
}

window.addEventListener('load', addGoalLinkEvents);

function showYoutubeVideo(container, video_id){
    container.innerHTML = `<iframe class="ytplayer" type="text/html" width="${container.clientWidth}" height="${container.clientWidth * 0.5625}" src="https://www.youtube.com/embed/${video_id}?rel=0" frameborder="0"></iframe>`;
    container.style.borderColor = "black";
    container.style.backgroundColor = "white";
    plausible('Youtube Embed');
}
