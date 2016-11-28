$("label input").on("click",function(){
    $('label').css('background', 'transparent')
    $('label').css('color', 'black')
    $(this).parent().css('color', 'white')
    if ($(this).val()=='Playstation-3' || $(this).val()=='Playstation-4'){
      $(this).parent().css('background', 'linear-gradient(to right, rgb(1,72,153), rgb(1, 132, 212)')
    }
    else if ($(this).val()=='Xbox-One' || $(this).val()=='Xbox-360'){
      $(this).parent().css('background', 'linear-gradient(to right, green, rgb(33, 188, 70)')

    }
    else if ($(this).val()=='Wii' || $(this).val()=='Wii-U'){
      $(this).parent().css('background', 'linear-gradient(to right, gray, rgb(180, 180, 180)')

    }
    else if ($(this).val()=='Other'){
      $(this).parent().css('background', 'linear-gradient(to right, black, rgb(80, 80, 80)')
    }
});
