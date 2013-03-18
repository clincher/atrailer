function getCookie(c_name) {
    var i,x,y,ARRcookies=document.cookie.split(";");
    for (i=0;i<ARRcookies.length;i++)
    {
        x=ARRcookies[i].substr(0,ARRcookies[i].indexOf("="));
        y=ARRcookies[i].substr(ARRcookies[i].indexOf("=")+1);
        x=x.replace(/^\s+|\s+$/g,"");
        if (x==c_name)
        {
            return unescape(y);
        }
    }
}

$(function() {
    $('#callback-form').ajaxForm(function(res) {
        var response = $.parseJSON(res);

        if (response['errors']) {
            var errors = response['errors'];
            var msg = 'Заполните необходимые поля: ';

            if (errors['username']) msg += '\n- ваше имя ';
            if (errors['comment']) msg += '\n- вопрос ';
            if (errors['email_or_phone']) msg += '\n- email или номер телефона ';

            alert(msg);
        } else {
            alert("Мы с вами свяжемся!");
            window.location = '/';
        }
    });

    $('.add').click(function(e) {
        e.preventDefault();
        var el = $(this);
        var xhr = $.ajax({
            url: '{% url cart %}',
            type: 'post',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                add_item_id: el.attr('data-item-id'),
                add_item_quantity: el.attr('data-item-quantity')
            }
        });

        xhr.done(function(response) {
            console.log(response);
            window.location.reload();
        });
    });
});
