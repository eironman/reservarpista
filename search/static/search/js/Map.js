var Map =
{
    map: null,
    markersList: [],
    markerHighlighted: null,
    sportsCenterslocations: [],
    // blueMarkerIcon: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
    blueMarkerIcon: '/static/search/img/blu-circle.png',
    redMarkerIcon: '/static/search/img/red-circle.png',

    // Shows in the results the sports center selected
    displayCenter: function(sportsCenterId)
    {
        SportsCenter.find(sportsCenterId);
    },

    // Hides the map (for mobile)
    hideMap: function()
    {
        $("#map-column").css("visibility", "hidden");
    },

    // Highlights the marker of a sports center
    highlightMarker: function(id)
    {
        if (this.markerHighlighted == null ||
           (this.markerHighlighted !== null && this.markerHighlighted.sportsCenterId != id))
        {
            for (var i=0; i<this.markersList.length; i++) {
                if (this.markersList[i].sportsCenterId == id) {
                    this.markersList[i].setIcon(this.redMarkerIcon);
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
                '<a href="#" onclick="Map.displayCenter(' + self.sportsCenterslocations[i]['id'] + '); return false;">' +
                'Ver Ficha' +
                '</a>' +
                '</p>';

            // Put marker on map
            var marker = new google.maps.Marker({
                position: markerPosition,
                map: self.map,
                icon: self.blueMarkerIcon,
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

    // Shows the map (for mobile)
    showMap: function()
    {
        $("#map-column").css("visibility", "visible");
    },

    // Stops highlighting the active marker at that moment
    unhighlightActiveMarker: function()
    {
        if (this.markerHighlighted !== null) {
            this.markerHighlighted.setIcon(this.blueMarkerIcon);
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
          mapTypeControlOptions: {
              position: google.maps.ControlPosition.TOP_CENTER
          },
        });

        this.placeMarkers();
    }
};