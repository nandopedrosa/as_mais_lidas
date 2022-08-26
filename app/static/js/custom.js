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
    ).fail(function () {
        window.location.replace(baseURL + '/error');
    });
}

/*
 Activates selected menu item (and deactivates previous selected menu item)
 */
function toggleMenuItem(menuItem) {
    //Remove previous selected item
    $('#aml-menu > a.list-group-item').removeClass('active');
    //Activate current menu item
    menuItem.addClass('active');
}

/*
 Changes between National and International news source
 Activates selected menu (based on the first news source of the national or international list)
 */

$('.aml-btn').click(function () {

    var id = $(this).attr('id');
    var firstItem;

    if (id == 'btn-national') {
        $('.news.national').css('display', 'block');
        firstItem = $('.national').first();

    } else {
        $('.national').css('display', 'none');
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
 Removes a previous alert (error) message
 */
function removeErrorAlert(modalId) {
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
 Shows a sucess message alert
 param: formId: the id of the form related to the message
 para: message: the message content to be shown
 */
function showSuccessMessage(formId, message) {
    var successMessage = '<div class="alert alert-success" role="alert">#MESSAGE#</div>'.replace('#MESSAGE#', message);
    $(successMessage).insertBefore(formId);
}

/*
 Shows an error message alert
 param: formId: the id of the form related to the message
 para: message: the message content to be shown
 */
function showErrorMesssage(formId, message) {
    var errorMessage = '<div class="alert alert-danger" role="alert">#MESSAGE#</div>'.replace('#MESSAGE#', message);
    $(errorMessage).insertBefore(formId);
}

/*
 Change category
 */
$('#select-category').change(function() {
    //Make previous news source go blank, for a smoother transition
    $('#aml-source').text('');

   //First we hide previously shown items
    $('.list-group-item').css('display', 'none');

    //Now we show the correct items based on the chosen category
    var category = $(this).val();

    $('.list-group-item.national.' + category).css('display', 'block');

    // We only show the Location Select and National/International Buttons for the News Category
    if(category != 'news') {
        $('#btn-national').hide();
    } else {
        $('#btn-national').show();
    }

    var firstItem = $('.' + category).first();
    toggleMenuItem(firstItem);
    refreshNewsSource(firstItem);

});
