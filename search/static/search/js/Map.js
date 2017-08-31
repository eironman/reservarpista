var Map =
{
    map: null,
    markersList: [],
    markerHighlighted: null,
    sportsCenterslocations: [],
    blueMarker: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
    redMarker: 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',

    // Shows in the results the sports center selected and shows the booking form
    askForBooking: function(sportsCenterId)
    {
        SportsCenter.find(sportsCenterId);
    },

    // Highlights the marker of a sports center
    highlightMarker: function(id)
    {
        if (this.markerHighlighted == null ||
           (this.markerHighlighted !== null && this.markerHighlighted.sportsCenterId != id))
        {
            for (var i=0; i<this.markersList.length; i++) {
                if (this.markersList[i].sportsCenterId == id) {
                    this.markersList[i].setIcon(this.redMarker);
                    this.markerHighlighted = this.markersList[i];
                    break;
                }
            }
        }
    },

    // Places the markers in the map and sets the map boundaries to fit all the markers
    placeMarkers: function()
    {
        var self = this;
        var infoWindow;
        var infoWindowContent;
        var markersBounds = new google.maps.LatLngBounds();

        for (var i=0; i < self.sportsCenterslocations.length; i++) {

            var markerPosition = {
                lat: self.sportsCenterslocations[i]['lat'],
                lng: self.sportsCenterslocations[i]['lng']
            }
            markersBounds.extend(markerPosition);

            self.infoWindowContent =
                '<h6>' + self.sportsCenterslocations[i]['name'] + '</h6>' +
                '<p>' + self.sportsCenterslocations[i]['phone'] + '</p>' +
                '<p>' +
                '<a href="#" onclick="Map.askForBooking(' + self.sportsCenterslocations[i]['id'] + '); return false;">' +
                'Ver Ficha' +
                '</a>' +
                '</p>';

            // Put marker on map
            var marker = new google.maps.Marker({
                position: markerPosition,
                map: self.map,
                icon: self.blueMarker,
                html: self.infoWindowContent,
                sportsCenterId: this.sportsCenterslocations[i]['id'],
            });

            // Add info window
            infoWindow = new google.maps.InfoWindow();
            marker.addListener('click', function() {
                infoWindow.setContent(this.html);
                infoWindow.open(map, this);
            })

            self.markersList.push(marker);
        }

        // Sets map boundaries to fit all markers
        self.map.fitBounds(markersBounds);
    },

    // Stops highlighting the active marker at that moment
    unhighlightActiveMarker: function()
    {
        if (this.markerHighlighted !== null) {
            this.markerHighlighted.setIcon(this.blueMarker);
            this.markerHighlighted = null;
        }
    },

    init: function()
    {
        var containerWidth = $('#map-column').width();
        var containerHeight = $(window).height();
        var headerHeight = $('header').outerHeight();
        var searchFormHeight = $('.search-form-container').outerHeight();;
        this.sportsCenterslocations = $('#map').data('locations');

        // Set map container width
        $('#map-container').width(containerWidth + 'px');

        // Set map container height
        containerHeight -= searchFormHeight
        containerHeight -= headerHeight;
        $('#map-container').height(containerHeight + 'px');

        // Set map container top
        $('#map-container').css('top', headerHeight + searchFormHeight + 'px');

        // Init map
        this.map = new google.maps.Map(document.getElementById('map'), {
          scrollwheel: false,
        });

        this.placeMarkers();
    }
};