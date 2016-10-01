$('.searchForm').on('submit', function(e){
    e.preventDefault();
    $('.games').empty()
    $('.games').hide()
    $('footer').css({position:'fixed',bottom: 0})
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
                ).show('slow')
            $('footer').css({position:'absolute',bottom: 0})
        }
    }).done(function(data){
        var csrftoken = $('meta[name=csrf-token]').attr('content')
        if (data.length === 0){
            $('.games').append('<p>There are no games by that name.</p>').show('slow')
        }
        data.forEach(function(data){
            try {
            var id = data.id
            var title = data.name
            var image = data.cover.cloudinary_id
            var summary = data.summary
            if (!data.summary){
                summary = "No summary available"
            }
            var rating = Number(data.rating).toFixed(2)
            if (!data.rating){
                rating = "Not Rated"
            }
            var release_date = new Date(data.release_dates[0].date)
            var platforms = []
            var platform = data.release_dates.forEach(function(item, idx){
                if (item.platform === 9 && platforms.indexOf('Playstation 3') === -1){
                    platforms.push('Playstation 3')
                } else if (item.platform === 48 && platforms.indexOf('Playstation 4') === -1){
                    platforms.push('Playstation 4')
                } else if (item.platform === 12 && platforms.indexOf('Xbox 360') === -1){
                    platforms.push('Xbox 360')
                } else if (item.platform === 49 && platforms.indexOf('Xbox One') === -1){
                    platforms.push('Xbox One')
                } else if (item.platform === 3 && platforms.indexOf('Wii') === -1){
                    platforms.push('Wii')
                } else if (item.platform === 41 && platforms.indexOf('Wii U') === -1){
                    platforms.push('Wii U')
                } else if (platforms.length===0 && data.release_dates.length-1 === idx){
                    platforms.push('Other')
                }
            })
            var platformInputs = platforms.map(function(system, index){
                return '<input type="radio" id='+system.split(' ').join('')+' name="platform" value='+system.replace(/ /,"-") + '>' + system
            })
            $('.games').append(
                '<div class="game"> <p>' + title + '</p> <div class="gameCover"> <p class="gameId" style="display:none">' + id + '</p>' +
                '<img src=https://res.cloudinary.com/igdb/image/upload/t_cover_big/' + image + '.jpg> </div>' +
                '<div class="gameDesc"> <p><b>Summary:</b> ' + summary + '</p>' + 
                '<p><b>Rating:</b> ' + rating + '</p>' + 
                '<p><b>Release Date:</b> ' + Number(release_date.getMonth()+1) +'/'+ release_date.getDate() +'/'+ release_date.getFullYear() + '</p>' + 
                '<form id="addGameForm" action="/search" method="POST"><div class="inputs">'+ platformInputs.join('') + '</div><div class="buttons"> <input type="submit" id="own" name="action" value="I own it!">' + '<input type="submit" id="want" name="action" value="I want it!"></div>' +
                '<input id="csrf_token" name="csrf_token" type="hidden" value="' + csrftoken + '">' + '<input type="hidden" name="name" value="'+ title + '">' + '<input type="hidden" name="image" value="'+ image + '">' +
                '<input type="hidden" name="game_id" value="'+ id + '">' + 
                '</form>' +'</div>' + '</div> <hr>'
                ).show('slow')
            }
            catch(err){console.log(err)}
        })

    if (data.length===0){
        $('footer').css({position:'fixed',bottom: 0})
    }
    $('#search').val('');
    if (data.length > 0){
        $('footer').hide()
        setTimeout( function(){ 
            $('footer').css({position:'static',bottom: 0}).show('slow')
        }  ,500)
    }
    })
})

$('.homeSearchForm').on('submit', function(e){
    e.preventDefault()
    var game = $('#homeSearch').val()
    window.location.href = "/search?" + game
})

$('.searchForm').ready(function() {
    if (window.location.search.substring(1)){
        var query = window.location.search.substring(1)
        var vars = query.split("%20").join(" ")
        $('#search').val(vars)
        $('#searchBtn').click()
    }
});

$('.hover').on('click',function(e){
    $(e.target).next().show()
})

$('.sure').on('click', function(){
    $('.sure').fadeOut()
})

$('.1star').on('click', function(){
    $('.1star').css('color', '#FFDF00').hide().fadeIn()
    $('.2star').css('color', 'rgb(200,200,200)')
    $('.3star').css('color', 'rgb(200,200,200)')
    $('.4star').css('color', 'rgb(200,200,200)')
    $('.5star').css('color', 'rgb(200,200,200)')
    $('#stars').val(1)
})
$('.2star').on('click', function(){
    $('.1star').css('color', '#FFDF00').hide().fadeIn()
    $('.2star').css('color', '#FFDF00').hide().fadeIn()
    $('.3star').css('color', 'rgb(200,200,200)')
    $('.4star').css('color', 'rgb(200,200,200)')
    $('.5star').css('color', 'rgb(200,200,200)')
    $('#stars').val(2)
})
$('.3star').on('click', function(){
    $('.1star').css('color', '#FFDF00').hide().fadeIn()
    $('.2star').css('color', '#FFDF00').hide().fadeIn()
    $('.3star').css('color', '#FFDF00').hide().fadeIn()
    $('.4star').css('color', 'rgb(200,200,200)')
    $('.5star').css('color', 'rgb(200,200,200)')
    $('#stars').val(3)
})
$('.4star').on('click', function(){
    $('.1star').css('color', '#FFDF00').hide().fadeIn()
    $('.2star').css('color', '#FFDF00').hide().fadeIn()
    $('.3star').css('color', '#FFDF00').hide().fadeIn()
    $('.4star').css('color', '#FFDF00').hide().fadeIn()
    $('.5star').css('color', 'rgb(200,200,200)')
    $('#stars').val(4)
})
$('.5star').on('click', function(){
    $('.1star').css('color', '#FFDF00').hide().fadeIn()
    $('.2star').css('color', '#FFDF00').hide().fadeIn()
    $('.3star').css('color', '#FFDF00').hide().fadeIn()
    $('.4star').css('color', '#FFDF00').hide().fadeIn()
    $('.5star').css('color', '#FFDF00').hide().fadeIn()
    $('#stars').val(5)
})

$('#bars').click(function(){
    $('#sideNav').toggle('slow')
})

$('#bio').hover(function(){
    $('.bio-edit-icon').toggle('show')
})


$('.bio-edit-icon').click(function(){
    $('#edit-box').fadeToggle('show')
    $('#bioSave').fadeToggle('show')
    $('#bioCancel').fadeToggle('show')
    $('#edit-box').focus()
})

$('#bioCancel').click(function(){
    $('#edit-box').hide()
    $('#bioSave').hide()
    $('#bioCancel').hide()
})

$(document).ready(function(){
    if('#edit-box'){
        $('#edit-box').val($('#bioText')[0].innerText)
    }
})

$('.profPic').hover(function(){
    $('.img-edit-icon').toggle('show')
})

$('.img-edit-icon').click(function(){
    $('#imgInput').fadeToggle('show')
    $('#imgSave').fadeToggle('show')
    $('#imgCancel').fadeToggle('show')
    $('#imgInput').focus()
})

$('#imgCancel').click(function(){
    $('#imgInput').hide()
    $('#imgSave').hide()
    $('#imgCancel').hide()
})

// $('#imgSave').click(function(){
//     $('#edit-box').val === $('#bioText').text()
//     $('#image-form').submit()
// })

// $('#bioSave').click(function(){
//     // $('#imgInput').val($('.profImg')[0].src)
//     //     console.log('yo')
//     // if ($('#imgInput').val()===window.location.origin+'/static/images/crash.jpg'){
//     //     $('#imgInput').val('../static/images/crash.jpg')
//     //     console.log($('#imgInput').val())
//     // }
//     $("image-form").submit(function(e){
//         stopEvent(e);
//     })
//     $('#bio-form').submit()
// })

$(document).ready(function(){
    var path=window.location.pathname
    if (path==="/contact"){
        if (window.screen.height > 999){
            $('footer').css({position:'absolute',bottom: 0})
        }
    }
})

