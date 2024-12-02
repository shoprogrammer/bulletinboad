$(document).ready(function(){
    $(".alert").delay(3000).fadeOut("slow");

});

// お気に入りボタンの非同期通信
$(document).on('click','favorite-form',function(e){
    e.preventDefault();

    let $form = $(this);
    let url = $form.attrs('action');
    let data = $form.serialize();

    $ajax({
        url: url,
        type: 'POST',
        dataType: 'json',



    }).done(function(response){
        if (response.status === 'success'){
            $form.closest('td').html(response.html);

        }else{
            alert('エラーが発生しました.:' + response.message);
        }


    }).fail(function(response){
        alert('エラーが発生しました:' + response.message);
    });


});