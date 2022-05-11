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
        }
    })

}