
    function getMusicalInfo(id) {
        $.ajax({
            type: 'GET',
            url: '/info/' + id,
            success: function (response) {
                console.log(response)
                alert(response['name'] + '\n' + response['location'] + '\n' + response['date'] + '\n' + response['poster'])
                $('#modal_title').text(response['name']);
                $('#modal_period').text(response['date']);
                $('#modal_loca').text(response['location']);
                $('#modal_poster').attr('src', response['poster']);
                $('#favorite-btn').attr('title',response['id']);
                $('#modal').attr('title',response['id']);
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
                for(var i = 0 ; i < performs.length;i++){
                    element = performs[i]
                    performid = element.getAttribute('id');
                    if (favoritelist.includes(performid)) {
                        element.style.display = '';
                    } else {
                        if(button.text()=='찜 목록만 보기')
                            element.style.display = 'none';
                        else
                            element.style.display='';
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
            type:'PATCH',
            url:'/add/favorite/'+id,
            success:function (response){
                alert(response['msg'])
                 button = $('#favorite_btn');
                if (button.text() == '전체 보기') {
                    refreshFavoirteList();
                }
            }
        })

    }