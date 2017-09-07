(function($){
    // Init page elements
    $(function(){
        Paginator.init();
        SportsCenter.init();
        BookingModal.init();
        SearchResults.init();
    });
})(jQuery);

// Callback for google captcha
function GCaptchaCallback()
{
    BookingModal.sendBookingRequest();
}











































