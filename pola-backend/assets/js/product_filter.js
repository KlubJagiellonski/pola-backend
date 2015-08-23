"use strict";
(function ($) {
    function check() {
        $('#id_company').prop('disabled', $('#id_company_empty').is(':checked'));
    }
    check();
    $('#id_company_empty').change(check);
}(jQuery));
