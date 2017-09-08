var SearchResults =
{
    mq: null,

    showSportsCentersMap: function()
    {
        if (this.mq.matches) {
            Map.showMap();
            SportsCenter.hideList();
            $("#show-result-map").addClass("hide");
            $("#show-result-centers").removeClass("hide");
        }
    },

    showSportsCentersList: function()
    {
        if (this.mq.matches) {
            Map.hideMap();
            SportsCenter.showList();
            $("#show-result-map").removeClass("hide");
            $("#show-result-centers").addClass("hide");
        }
    },

    init: function()
    {
        var self = this;

        // Media query to control window width
        this.mq = window.matchMedia( "(max-width: 601px)" );

        // Mobile buttons
        // Show map
        $("#show-result-map").on('click', function(){
            self.showSportsCentersMap();
        });
        // Show centers list
        $("#show-result-centers").on('click', function(){
            self.showSportsCentersList();
        });
    }
}