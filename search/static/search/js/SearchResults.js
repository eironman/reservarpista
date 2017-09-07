var SearchResults =
{
    //
    showSportsCentersMap: function()
    {
        Map.showMap();
        SportsCenter.hideList();
        $("#show-result-map").addClass("hide");
        $("#show-result-centers").removeClass("hide");
    },

    showSportsCentersList: function()
    {
        Map.hideMap();
        SportsCenter.showList();
        $("#show-result-map").removeClass("hide");
        $("#show-result-centers").addClass("hide");
    },

    init: function()
    {
        var self = this;
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