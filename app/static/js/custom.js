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


//AJAX call to refresh the News Source
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

// AJAX calls after menu select
$('#aml-menu > a.list-group-item').click(function () {

    //Highlight the correct menu item
    $('#aml-menu > a.list-group-item').removeClass('active');
    $(this).addClass('active');

    refreshNewsSource($(this));
});

function setLocation(userip) {
    alert(userip);


}