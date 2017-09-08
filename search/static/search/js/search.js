(function($){
    // Init page elements
    $(function(){
        SportsCenter.init();
        Paginator.init();
        BookingModal.init();
        SearchResults.init();
    });
})(jQuery);

// Callback for google captcha
function GCaptchaCallback()
{
    BookingModal.sendBookingRequest();
}











































