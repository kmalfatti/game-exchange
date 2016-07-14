$('form').on('submit', function(e){
    e.preventDefault();
    $('.games').empty()
    $.ajax({
        url: "https://igdbcom-internet-game-database-v1.p.mashape.com/games/?fields=*&search=" + $('#search').val(),
        headers: { 
            "X-Mashape-Key":"E7I0tSnUnzmshhTg3A2XEie00uIHp1BB05EjsnWj0EVpHQoP7h",
            "Accept":"application/json"
        },
        success: function(data){
            console.log(data)
        },
        error: function(err){
            console.log('error: ', err)
            $('.games').append(
                '<h3>Error</h3>',
                '<p>Sorry, something went wrong while processing your request.</p>',
                '<p>Please try again later.</p>'
                )
        }
    }).done(function(data){
        if (data.length === 0){
            $('.games').append('<p>There are no games by that name.</p>')
        }
        data.forEach(function(data){
            var id = data.id
            var title = data.name
            var image = data.cover.cloudinary_id
            var release_date = data.created_at
            $('.games').append(
                '<div class="game">',
                '<p class="gameId" style="display:none">' + id + '</p>',
                '<p>' + title + '</p>',
                '<img src=https://res.cloudinary.com/igdb/image/upload/t_cover_big/' + image + '.jpg>',
                '</div>',
                '<div class="gameDesc">',

                '</div>'
                )
        })
    })
    $('#search').val('');
})
  
