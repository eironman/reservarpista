var SearchResultsSportsCenter =
{
    center: null,

    // Performs animation to show the sports center selected in the map
    animateSelected: function()
    {
        this.scrollTo();
        this.highlight();
        this.showInfo();
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
                    self.initializeCarousel();
                    SearchResults.showSportsCentersList();
                    self.animateSelected();
                } else {
                    alert('Ha ocurrido un error al obtener el centro deportivo');
                }
            });
        } else {
            self.initializeCarousel();
            SearchResults.showSportsCentersList();
            this.animateSelected();
        }
    },

    // Highlights the sports center selected in the map
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

    // Hides the centers list (for mobile)
    hideList: function()
    {
        $("#sports-centers-column").css("visibility", "hidden");
    },

    // Initializes the image carousel
    initializeCarousel: function()
    {
        $('.carousel.carousel-slider').carousel({
            fullWidth: true,
            indicators: true
        });
    },

    // Scrolls to the sports center selected in the map
    scrollTo: function()
    {
        var self = this;
        if (!self.centerIsNull()) {
            $('html, body').animate({
                scrollTop: ($(self.center).offset().top - 200)
            }, 400);
        }
    },

    // Shows the info card of the center selected in the map
    showInfo: function()
    {
        if (!this.centerIsNull()) {
            $(this.center).find('.activator').click();
        }
    },

    // Shows the centers list (for mobile)
    showList: function()
    {
        $("#sports-centers-column").css("visibility", "visible");
    },

    init: function()
    {
        this.initializeCarousel();

        // Hover events
        $('#sports_centers_cards').on('mouseover', '.card', function() {
            SearchResultsMap.highlightMarker($(this).data('id'));
        });
        $('#sports_centers_cards').on('mouseleave', '.card', function() {
            SearchResultsMap.unhighlightActiveMarker();
        });
    }
};





























