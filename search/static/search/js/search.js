(function($){
    // Init page elements
    $(function(){
        Paginator.init();
        SportsCenter.init();
        BookingModal.init();
    });
})(jQuery);

function GCaptchaCallback()
{
    BookingModal.sendBookingRequest();
}











































