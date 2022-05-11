
function getParameter(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}
function alerterMsg(){
    msg = getParameter('msg')
    if(msg.length != 0){
        alert(msg);
        window.location.href='/login'
    }
}
alerterMsg()