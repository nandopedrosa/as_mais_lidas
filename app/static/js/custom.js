// We need the host root URL to execute the AJAX calls
baseURL = window.location.protocol + "//" + window.location.host;

// News list template
var template = '<li class="list-group-item"><a href="#LINK#" target="_blank">#TITLE#</a></li>';

// Busy Processing Indicator
$.ajaxSetup({
    beforeSend: function () {
        $("#loading").show();
    },
    complete: function () {
        $("#loading").hide();
    }
});


//AJAX Call to refresh the Main Panel after user clicks on a menu item
function refreshNewsSource(obj) {

    var params;
    var id = obj.attr('id');

    params = {
        ns: id
    };

    // For local News Sources we have to fecth JQuery.data to know the location (eg.: DF, SP, etc.)
    if (id == 'local') {
        params.local = obj.data('state');
    }

    // AJAX call to refresh the news source
    $.get(
        baseURL + '/most_read_ns',
        params,
        function (responseContent) {
            //Set the title of the news
            $('#aml-source').text(responseContent.header);

            //Remove old news
            $('.list-group-item', '#aml-list').remove();

            //Now set the list of news
            var newsList = $('#aml-list');
            for (var i = 0; i < responseContent.news.length; i++) {
                var n = template.replace('#LINK#', responseContent.news[i].link).replace('#TITLE#', responseContent.news[i].title);
                newsList.append(n);
            }
        },
        'json'
    );
}

/*
 Activates selected menu item (and deactivates previous selected menu item)
 */
function toggleMenuItem(menuItem) {
    //Remove previous selected item
    $('#aml-menu > a.list-group-item').removeClass('active');
    //Activate current menu item
    menuItem.addClass('active');
    $(this).addClass('active');
}

/*
 Changes between National and International news source
 Activates selected menu (based on the first news source of the national or international list)
 */

$('.aml-btn').click(function () {

    var id = $(this).attr('id');
    var firstItem;

    if (id == 'btn-national') {
        $('.national').css('display', 'block');
        $('.international').css('display', 'none');
        firstItem = $('.national').first();

    } else {
        $('.national').css('display', 'none');
        $('.international').css('display', 'block');
        firstItem = $('.international').first();
    }
    toggleMenuItem(firstItem);
    refreshNewsSource(firstItem);
});

/*
 Select and refresh news source
 */
$('#aml-menu > a.list-group-item').click(function () {
    toggleMenuItem($(this));
    refreshNewsSource($(this));
});

/*
 Change page language
 */
$('#lang').click(function () {
    var lang = $(this);
    var code = 'pt';

    if (lang.text().toLowerCase() == 'english') {
        lang.text('PORTUGUÊS');
        code = 'en';
    } else {
        lang.text('ENGLISH');
    }

    console.log(code);
    $.post(
        baseURL + '/lang/' + code,
        function() {
            window.location.reload();
        }
    );

});

/*
 Change user location
 */
$('#select-location').change(function () {
    var location = $(this).val();

    if (location == '')
        return;

    $.get(
        baseURL + '/change_location',
        {
            location: location
        },
        function (responseContent) {
            $('#local').text(responseContent.ns_name + '*');
            $('#local').data('state', location.replace('local', '')); // e.g (localAC -> AC)
        },
        'json'
    );
});

/*
 Resets modal fields and error messages
 :param modalId: the id of the modal to be reset
 */
function resetModal(modalId) {
    $(modalId).find('form').trigger('reset'); //Resets all input fields
    $(modalId).find('div').removeClass('has-error'); //Removes error class
    $(modalId).find('p.text-danger').text(''); //Removes field error messages
    $(modalId).find('div.alert').remove(); //Removes alert messages
}

/*
 Resets modal fields and error messages when modal is opened
 */
$('*[data-toggle="modal"]').click(function () {
    var modalId = $(this).attr('data-target');
    resetModal(modalId);
});

/*
 Hides a specific modal (and removes backdrop overlay)
 param: id: the ID of the modal to be hidden
 */
/*function hideModal(id) {
 $(id).modal('hide');
 $('body').removeClass('modal-open');
 $('.modal-backdrop').remove();
 }*/

/*
 Shows an error message for a specific form element
 :param id: the form element id
 :param message: the error message to be shown
 */
function fieldError(id, message) {
    $(id).next('p').text(message);
    $(id).parent('div.form-group').addClass('has-error');
}

/*
 Shows a sucess message alert
 param: formId: the id of the form related to the message
 para: message: the message content to be shown
 */
function showSuccessMessage(formId, message) {
    var successMessage = '<div class="alert alert-success" role="alert">#MESSAGE#</div>'.replace('#MESSAGE#', message);
    $(successMessage).insertBefore(formId);
}

/*
 Submit contact message
 */
$('#btn-submit-contact').click(function () {
    $.post(
        baseURL + '/send_message',
        $('#contact-form').serialize(),
        function (data) {
            if (data.error) {
                if (data.name != undefined) fieldError('#contact-name', data.name[0]);
                if (data.email != undefined) fieldError('#contact-email', data.email[0]);
                if (data.message != undefined) fieldError('#contact-message', data.message[0]);
            } else {
                resetModal('#contact-modal');
                showSuccessMessage('#contact-form', 'Mensagem enviada com sucesso');
            }
        },
        'json'
    );
});

