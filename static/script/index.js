// 검색 기능
// category에 따라서 다른 조건으로 탐색 진행
function searchMusical() {
    var search = $('#search-input').val().toUpperCase();
    let performs = document.getElementById('item-box').children;
    let button = $('#favorite-btn');
    let categoryBox = document.getElementById('category-selection')
    let categoryId = categoryBox.options[categoryBox.selectedIndex].value
    if (button.text() == '전체 보기') {
        button.text('찜 목록만 보기')
    }
    if (categoryId == 0) {
        for (var i = 0; i < performs.length; i++) {
            let element = performs[i];
            if (element.getElementsByClassName('pf-tit')[0].innerText.toUpperCase().includes(search)) {
                element.style.display = '';
            } else {
                element.style.display = 'none';
            }
        }
    } else if (categoryId == 1) {
        let selectDate = new Date(search)
        for (var i = 0; i < performs.length; i++) {
            let element = performs[i];
            let date = element.getElementsByClassName('pf-date')[0].innerText.toUpperCase().replace('.', '-');
            let preDate = new Date(date.split('~')[0]);
            let lastDate = new Date(date.split('~')[1]);
            if (selectDate >= preDate && selectDate <= lastDate) {
                element.style.display = '';
            } else {
                element.style.display = 'none';
            }
        }
    } else {
        for (var i = 0; i < performs.length; i++) {
            let element = performs[i];
            if (element.getElementsByClassName('pf-location')[0].innerText.toUpperCase().includes(search)) {
                element.style.display = '';
            } else {
                element.style.display = 'none';
            }
        }
    }
}
// 검색 category 변경 이벤트
function onChangeCategory() {
    let categoryBox = document.getElementById('category-selection')
    let categoryId = categoryBox.options[categoryBox.selectedIndex].value
    let searchInput = $('#search-input')

    switch (categoryId) {
        case '2':
        case '0':
            searchInput.attr('type', 'text');
            break;
        case '1':
            searchInput.attr('type', 'date');
            break;
    }
    searchInput.val('');
}
// modal창을 띄우기 위한 공연 정보 검색 이벤트
function getMusicalInfo(id) {
    $.ajax({
        type: 'GET',
        url: '/info/' + id,
        success: function (response) {
            console.log(response)

            let data = response['data']
            $('#modal_title').text(data['name']);
            $('#modal_period').text(data['date']);
            $('#modal_loca').text(data['location']);
            $('#modal_poster').attr('src', data['poster']);
            $('#favorite-btn').attr('title', data['id']);
            $('#modal').attr('title', data['id']);
            let comments = response['comment'];

            $("#dynamicTbody").empty();
            for (var i = 0; i < comments.length; i++) {
                let comment = comments[i];
                var html = '';
                html += '<tr>';
                html += '<td>' + comment['nick'] + '</td>';
                html += '<td>' + comment['comment'] + '</td>';
                html += '</tr>';
                $("#dynamicTbody").append(html);
            }
            show()
        }
    })
}
// 찜 목록만 보기에서 선택한 공연을 찜 해제했을때
// 바로 화면에 반영하기 위하여 다시한번 user 정보 조회후 화면에 반영
function refreshFavoirteList() {
    $.ajax({
        type: 'GET',
        url: '/userinfo',
        success: function (response) {
            favoritelist = response['favorite']
            console.log(response)
            let performs = document.getElementById('item-box').children
            for (var i = 0; i < performs.length; i++) {
                element = performs[i]
                performid = element.getAttribute('id');
                if (favoritelist.includes(performid)) {
                    element.style.display = '';
                } else {
                    element.style.display = 'none';
                }
            }
        }
    })
}
// 찜 목록만 보여주거나 전체 항목을 보여주는 이벤트
function toggleFavoriteList() {
    $.ajax({
        type: 'GET',
        url: '/userinfo',
        success: function (response) {
            favoritelist = response['favorite']
            button = $('#favorite_btn');

            let performs = document.getElementById('item-box').children
            for (var i = 0; i < performs.length; i++) {
                element = performs[i]
                performid = element.getAttribute('id');
                if (favoritelist.includes(performid)) {
                    element.style.display = '';
                } else {
                    if (button.text() == '찜 목록만 보기')
                        element.style.display = 'none';
                    else
                        element.style.display = '';
                }
            }
            if (button.text() == '찜 목록만 보기') {
                button.text('전체 보기')
            } else {
                button.text('찜 목록만 보기')
            }
        }
    })
}

// 찜 목록을 등록하거나 해제하는 이벤트
// 등록/해제후 변화된 ❤ 수를 바로 반영한다.
function toggleFavorite(id) {
    $.ajax({
        type: 'PATCH',
        url: '/add/favorite/' + id,
        success: function (response) {
            alert(response['msg'])
            button = $('#favorite_btn');
            if (button.text() == '전체 보기') {
                refreshFavoirteList();
            }
            let data = response['data']
            let target = document.getElementById(data['id']);
            target.getElementsByClassName('info-like')[0].innerText = '❤ ' + data['likecount'];
        }
    })
}
// comment를 등록하는 이벤트
function save_comment(id) {
    let commentval = $('#comment').val()
    $.ajax({
        type: "POST",
        url: "/add/comment/" + id,
        data: {comment_give: commentval},
        success: function (response) {
            alert(response["msg"])
            modal_clsbtn();
        }
    });
}
// 코멘트 테이블 체워넣는 이벤트(삭제)
function comment_table() {
    $.ajax({
        type: 'GET',
        url: "/comment/table",
        success: function (data) {
            var html = '';

            for (key in data) {
                html += '<tr>';
                html += '<td>' + data[key] + '</td>';
                html += '<td>' + data[key].comment + '</td>';
                html += '</tr>';
            }

            $("#dynamicTbody").empty();
            $("#dynamicTbody").append(html);
        }
    })
}

// modal 창 띄우기
function show() {
    document.querySelector(".background").className = "background show";
}
// modal 창 닫기
function modal_clsbtn() {
    document.querySelector(".background").className = "background";
}
