"use strict";
(function ($) {
	function check() {
        $('#id_company').prop('disabled', $('#id_company_empty').is(':checked'));
	}
    $('#id_company_empty').change(check);
}(jQuery));
