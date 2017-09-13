(function($){
    // Init page elements
    $(function(){
        SearchResultsSportsCenter.init();
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









































