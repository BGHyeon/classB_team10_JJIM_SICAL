// 회원가입 페이지 이동
function to_join() {
    window.location.href = "/join"
}
// 로그인 이벤트 + jwt 토큰 저장
function sign_in() {
    let username = $("#input-username").val()
    let password = $("#input-password").val()

    $.ajax({
        type: "POST",
        url: "/sign_in",
        data: {
            username_give: username,
            password_give: password
        },
        success: function (response) {
            if (response['result'] == 'success') {
                $.cookie('mytoken', response['token'], {path: '/'});
                window.location.replace("/")
            } else {
                alert(response['msg'])
            }
        }
    });
}
// parameter 받는 메소드( 로그인 실패시 해당 msg를 추출하기 위해 사용)
function getParameter(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

//  위 메소드에서 추출한 정보를 alert
function alerterMsg() {
    msg = getParameter('msg')
    if (msg.length != 0) {
        alert(msg);
        window.location.href = '/login'
    }
}

alerterMsg()