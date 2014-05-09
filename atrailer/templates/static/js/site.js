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

function post_to_url(path, params, method) {
    method = method || "post"; // Set method to post by default, if not specified.

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
        }
    }

    document.body.appendChild(form);
    form.submit();
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
            refresh_button = $(".js-captcha-refresh").get(0);
            $(refresh_button).siblings('img').attr('src', json['new_cptch_image']);
            $(refresh_button).siblings('[name=captcha_0]').attr('value', json['new_cptch_key']);

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
            url: '/cart/',
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

    $('.item-delete').click(function(e){
        e.preventDefault();
        post_to_url(
            $(this).attr("href"),
            {csrfmiddlewaretoken: getCookie('csrftoken')}
        );
    });
    $('.js-captcha-refresh').click(function(e){
        e.preventDefault();
        url = $(this).parents('form').attr('action');

        $.getJSON(url, {}, function(json) {
            refresh_button = $(".js-captcha-refresh").get(0);
            $(refresh_button).siblings('img').attr('src', json['new_cptch_image']);
            $(refresh_button).siblings('[name=captcha_0]').attr('value', json['new_cptch_key']);
            // This your should update captcha image src and captcha hidden input
        });
        return false;
    });
});
