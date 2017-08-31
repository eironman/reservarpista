var SearchForm =
{
    picker: null,
    form: null,

    getLocationText: function()
    {
        var location = this.form.find('select[name="location"] option:selected').text();
        return location;
    },

    getLocationValue: function()
    {
        var location = this.form.find('select[name="location"]').val();
        return location;
    },

    getDatePlaceholder: function()
    {
        var date = $('.datepicker').attr('placeholder');
        return date;
    },

    getDate: function(format)
    {
        format = format || 'yyyy/mm/dd';
        var date = this.picker.get('select', format);
        return date;
    },

    getDurationText: function()
    {
        var duration = this.form.find('select[name="duration"] option:selected').text();
        return duration;
    },

    getDurationValue: function()
    {
        var duration = this.form.find('select[name="duration"]').val();
        return duration;
    },

    getSportText: function()
    {
        var sport = this.form.find('select[name="sport"] option:selected').text();
        return sport;
    },

    getSportValue: function()
    {
        var sport = this.form.find('select[name="sport"]').val();
        return sport;
    },

    getTimeText: function()
    {
        var time = this.form.find('select[name="time"] option:selected').text();
        return time;
    },

    getTimeValue: function()
    {
        var time = this.form.find('select[name="time"]').val();
        return time;
    },

    initPickADate: function(page)
    {
        // Translations
        jQuery.extend( jQuery.fn.pickadate.defaults, {
            labelMonthNext: 'Mes siguiente',
            labelMonthPrev: 'Mes anterior',
            labelMonthSelect: 'Selecciona mes',
            labelYearSelect: 'Selecciona año',
            monthsFull: [ 'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre' ],
            monthsShort: [ 'ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic' ],
            weekdaysFull: [ 'domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado' ],
            weekdaysShort: [ 'dom', 'lun', 'mar', 'mié', 'jue', 'vie', 'sáb' ],
            weekdaysLetter: [ 'D', 'L', 'M', 'X', 'J', 'V', 'S' ],
            today: 'hoy',
            clear: 'borrar',
            close: 'cerrar',
            firstDay: 1,
            format: 'dddd d !de mmmm',
            formatSubmit: 'yyyy/mm/dd',
            hiddenName: true,
        });

        // Init pickadate
        var $input = $('.datepicker').pickadate({
            min: true
        });

        // Picker to use the API
        this.picker = $input.pickadate('picker');

        // Close when clicking on a date
        $('.datepicker').on('change', function(){
            $(this).next().find('.picker__close').click();
        })
    },

    // When user performs a search
    onUserSearch: function(event)
    {
        var to_url = "/" +
            this.getSportValue() + "/" +
            this.getLocationValue() + "?time=" +
            this.getTimeValue() + "&duration=" +
            this.getDurationValue();

        if (this.getDate() !== "") {
            to_url += "&date=" + this.getDate();
        }

        window.location = to_url;
    },

    init: function()
    {
        var self = this;

        $('select').material_select();
        self.initPickADate();
        self.form = $("#search-form");
        self.form.submit(function(event) {
            event.preventDefault();
            self.onUserSearch();
        });
    }
};