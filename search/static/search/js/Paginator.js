var Paginator =
{
    goToPage: function(page)
    {
        var self = this;

        $.ajax({
            method: 'GET',
            url   : 'go_to_page/' + page + '/' + window.location.search
        })
        .done(function(response) {
            if (response['result'] == 'ok') {
                $('#sports_centers_cards').html(response.html_list);
                $('#sports_centers_paginator').html(response.html_paginator);
                $('body').scrollTop(0);
            } else {
                alert('Ha ocurrido un error al obtener los centros deportivos');
            }
        });
    },

    init: function()
    {
        var self = this;

        $('#sports_centers_paginator').on('click', '#prev-page', function() {
            self.goToPage($(this).data('page'));
        });

        $('#sports_centers_paginator').on('click', '#next-page', function() {
            self.goToPage($(this).data('page'));
        });
    }
};