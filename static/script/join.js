$(document).ready(function () {

})
// id 중복 체크
function check_id() {
    if ($('#id').val() == '')
        alert('아이디를 입력해주세요.')
    else {
        $.ajax({
            type: "POST",
            url: "/idcheck",
            data: {id_give: $('#id').val()},
            success: function (response) {
                alert(response["msg"])
            }
        })
    }

}
// 취소시 login 페이지로 이동
function cancel() {
    window.location.href = '/login'
}
// 회원가입 이벤트
function join() {
    $.ajax({
        type: "POST",
        url: "/join",
        data: {
            id_give: $('#id').val(),
            pw_give: $('#pw').val(),
            nick_give: $('#nick').val(),
        },
        success: function (response) {
            if (response['result'] == 'success') {
                alert('회원가입이 완료되었습니다.')
                window.location.href = '/login'
            } else {
                alert('회원가입이 실패하였습니다.')
            }
        }
    })
}