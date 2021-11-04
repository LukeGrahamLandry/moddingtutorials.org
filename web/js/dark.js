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
    let dark = document.getElementById("dark") == undefined ? getCookie("darkmode") : document.getElementById("dark").checked;
    let sheet;
    if (dark){
        sheet = "/styles/dark.css";
    } else {
        sheet = "";
    }
    document.getElementById("theme").href = sheet;
    setCookie("darkmode", sheet, 365);
}

// set darkmode from cookie
if (getCookie("darkmode")) {
    if (document.getElementById("dark") != undefined){
        document.getElementById("dark").checked = true;
    }
    
    updateDarkmode();
}