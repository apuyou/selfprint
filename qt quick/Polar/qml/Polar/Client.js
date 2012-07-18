.pragma library

const RACINE = "/polar-web/";
const HOST = "localhost";

const types = {"p": "Partiel 1", "q": "Partiel 2", "m": "Médian", "f": "Final", "t": "Test 1", "u": "Test 2", "v": "Test 3"};
const semestres = {"A":"Automne", "P":"Printemps"};

var cacheDetails = {};
var cacheLogins = [];

function getUVS(callback) {
    return getJSONStuff("liste-annales", callback);
}

function getDetails(UV, callback) {
    if (!cacheDetails[UV]) {
        cacheDetails[UV] = getJSONStuff("details-annale="+UV, callback);
    }
    return cacheDetails[UV];
}

function getJSONStuff(request, callback) {
    var doc = new XMLHttpRequest();
    doc.onreadystatechange = function() {
                if (doc.readyState == XMLHttpRequest.DONE) {
                    var a = doc.responseText;
                    var jsonResult = JSON.parse(a);
                    callback(jsonResult);
                }
            };

    doc.open("GET", "http://" + HOST + RACINE+"annales/borne?" + request);
    doc.send();
}

function loadLogins() {
    getJSONStuff("get-logins", function(result) { cacheLogins = result; });
}

function validerLogin(login) {
    //return getJSONStuff("verif-login="+login, callback);
    for(var i=0; i<cacheLogins.length; i++) {
        if (cacheLogins[i] === login)
            return true;
    }
    return false;
}

function envoyerCommande(login, panier, callback) {
    var sender = new XMLHttpRequest();
    sender.onreadystatechange = function() {
                if (sender.readyState == XMLHttpRequest.DONE) {
                    callback(sender.responseText);
                }
            };

    var params = "login=" + login + "&uv0="+panier[0];
    for (var i=1; i<panier.length; i++) {
        params += "&uv"+i.toString()+"="+panier[i];
    }

    sender.open("POST", "http://" + HOST + RACINE + "annales/borne");
    //Send the proper header information along with the request
    sender.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    sender.setRequestHeader("Content-length", params.length);
    sender.setRequestHeader("Connection", "close");

    sender.send(params);
}

function priceStr(pages) {
    var prix = pages*0.06;
    var string = Math.floor(prix).toString() + ",";
    var reste = Math.floor((prix*100)%100);
    if (reste >= 10) {
        string += reste.toString();
    } else {
        string += "0" + reste.toString();
    }
    string += "€";
    return string;
}
