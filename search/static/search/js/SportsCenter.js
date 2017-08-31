var SportsCenter =
{
    center: null,

    // Performs animation to show the sports center selected
    animateSelected: function()
    {
        this.scrollTo();
        this.highlight();
        this.showForm();
    },

    // Checks if there is a center selected
    centerIsNull: function()
    {
        if (this.center == null || this.center.length == 0) {
            return true;
        }

        return false;
    },

    // Tries to find a sports center in the page
    // If it isn't there, calls for it and prints it in the results
    find: function(sportsCenterId)
    {
        var self = this;

        // Find center
        this.center = $('#center-' + sportsCenterId);
        if (this.center.length == 0) {
            $.ajax({
                method: 'GET',
                url   : 'get_sports_center/' + sportsCenterId
            })
            .done(function(response) {
                if (response['result'] == 'ok') {
                    $('#sports_centers_cards').prepend(response.html_sport_center);
                    self.center = $('#center-' + sportsCenterId);
                    self.animateSelected();
                } else {
                    alert('Ha ocurrido un error al obtener el centro deportivo');
                }
            });
        } else {
            this.animateSelected();
        }
    },

    // Hides booking forms
    hideBookingForms: function()
    {
        $('.close-reveal').click();
    },

    // Highlights the sports center
    highlight: function()
    {
        var self = this;
        if (!self.centerIsNull()) {
            $(self.center).addClass('highlighted');
            setTimeout(function () {
                $(self.center).removeClass('highlighted');
            }, 1000);
        }
    },

    // Scrolls to the sports center
    scrollTo: function()
    {
        var self = this;
        if (!self.centerIsNull()) {
            $('html, body').animate({
                scrollTop: ($(self.center).offset().top - 200)
            }, 400);
        }
    },

    // Shows booking form of the center
    showForm: function()
    {
        if (!this.centerIsNull()) {
            $(this.center).find('.activator').click();
        }
    },

    init: function()
    {
        // Hover events
        $('#sports_centers_cards').on('mouseover', '.card', function() {
            Map.highlightMarker($(this).data('id'));
        });
        $('#sports_centers_cards').on('mouseleave', '.card', function() {
            Map.unhighlightActiveMarker();
        });
    }
};





























