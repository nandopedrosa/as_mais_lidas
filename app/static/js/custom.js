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
$('#lang').click(function() {
   var lang = $(this);

    if(lang.text().toLowerCase() == 'english') {
        //We're changing to English
        $('#aml-title').text('The Most Read');
        $('#aml-subtitle').text('news you want to read');
        $('#aml-description').text("Here you find the most read news from popular" +
            " News Websites from all around the world. " +
            "If you are in Brazil, we'll try to show you some regional news from your location*!");
        $('#btn-national').text('National');
        $('#btn-international').text('International');
        $('#lang').text('PORTUGUÊS');
        $('#contact').text('CONTACT');
        $('#about').text('ABOUT');
    } else {
        //We're changing back to Portuguese
        window.location.reload(baseURL);
    }
});