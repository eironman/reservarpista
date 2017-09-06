var BookingModal =
{
    sport: null,
    location: null,
    date: null,
    time: null,
    duration: null,
    sportsCenterId: null,

    fillSportsCenterName: function(name)
    {
        $('#booking-modal #modal-sports-center-name').html(name);
    },

    // Fills the user request data
    fillUserRequestData: function()
    {
        $("#booking-modal-sport").html(this.sport);
        $("#booking-modal-location").html(this.location);
        $("#booking-modal-date").html(this.date);
        $("#booking-modal-time").html(this.time);
        $("#booking-modal-duration").html(this.duration);
    },

    // Hides all error messages
    hideErrors: function()
    {
        $('#booking-modal .errorlist .mandatory-name-field').addClass('hide');
        $('#booking-modal .errorlist .mandatory-contact-field').addClass('hide');
        $('#booking-modal .errorlist .request-error').addClass('hide');
    },

    // Checks if the form is ok, then executes the captcha
    isFormCompleted: function()
    {
        if ($("#user-name").val() == "") {
            this.showMandatoryNameError();
        } else if ($("#contact-phone").val() == "" && $("#contact-email").val() == "") {
            this.showMandatoryContactError();
        } else {
            // grecaptcha.execute(); // The callback is GCaptchaCallback (search.js), which executes BookingModal.sendBookingRequest()
            this.sendBookingRequest();
        }
    },

    // Sends the request to the sports center
    sendBookingRequest: function()
    {
        var self = this;
        this.showLoading();
        this.hideErrors();

        // Set the security token
        var csrftoken = Helper.getCookie('csrftoken')
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

        // Do the request
        $.ajax({
            method: 'POST',
            url   : 'send_booking_request/',
            data  : {
                sportsCenterId: self.sportsCenterId,
                location: self.location,
                sport: self.sport,
                date: self.date,
                time: self.time,
                duration: self.duration,
                userName: $("#user-name").val(),
                phone: $("#contact-phone").val(),
                email: $("#contact-email").val()
            }
        })
        .done(function(response) {
            if (response['result'] == 'ok') {
                self.showSuccess();
            } else {
                self.showForm();
                self.showRequestError();
            }
        })
        .fail(function() {
            self.showForm();
            self.showRequestError();
        });
    },

    // Shows the form to send the request
    showForm: function()
    {
        grecaptcha.reset();
        $('#booking-modal .btn').removeClass('disabled');
        $('#booking-modal .booking-form-content').removeClass('hide');
        $('#booking-modal .success-content').addClass('hide');
        $('#booking-modal .loading-content').addClass('hide');
    },

    // Shows the loader
    showLoading: function()
    {
        $('#booking-modal .btn').addClass('disabled');
        $('#booking-modal .booking-form-content').addClass('hide');
        $('#booking-modal .success-content').addClass('hide');
        $('#booking-modal .loading-content').removeClass('hide');
    },

    // Message error when the user didn't fill the name
    showMandatoryNameError: function()
    {
        $('#booking-modal .errorlist .request-error').addClass('hide');
        $('#booking-modal .errorlist .mandatory-contact-field').addClass('hide');
        $('#booking-modal .errorlist .mandatory-name-field').removeClass('hide');
    },

    // Message error when the user didn't fill the contact data
    showMandatoryContactError: function()
    {
        $('#booking-modal .errorlist .request-error').addClass('hide');
        $('#booking-modal .errorlist .mandatory-name-field').addClass('hide');
        $('#booking-modal .errorlist .mandatory-contact-field').removeClass('hide');
    },

    // Message error when the request went wrong
    showRequestError: function()
    {
        $('#booking-modal .errorlist .mandatory-field').addClass('hide');
        $('#booking-modal .errorlist .request-error').removeClass('hide');
    },

    // Success message
    showSuccess: function()
    {
        $('#booking-modal .btn.modal-close').removeClass('disabled');
        $('#booking-modal .booking-form-content').addClass('hide');
        $('#booking-modal .success-content').removeClass('hide');
        $('#booking-modal .loading-content').addClass('hide');
    },

    init: function()
    {
        var self = this;
        $('#booking-modal').modal({
            dismissible: false, // Modal can be dismissed by clicking outside of the modal
            ready: function(modal, trigger) { // Modal is opened
                self.sportsCenterId = $(trigger).data('id');
                self.fillSportsCenterName($(trigger).data('sports-center-name'));
                self.showForm();
            },
            complete: function() { // Modal is closed
                self.showLoading();
                self.hideErrors();
            }
        });

        this.sport = SearchForm.getSportText()
        this.location = SearchForm.getLocationText()
        this.date = SearchForm.getDate('dddd d !de mmmm')
        if (this.date == '') {
            this.date = SearchForm.getDatePlaceholder();
        }
        this.time = SearchForm.getTimeText();
        this.duration = SearchForm.getDurationText();
        this.fillUserRequestData();
        // $('#booking-modal').modal('open');
        // this.showForm();
    }
}




























