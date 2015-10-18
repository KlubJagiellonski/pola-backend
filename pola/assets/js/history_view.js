(function ($) {
    "use strict";
    $('.js-revision-open').click(function (){
        var $this = $(this);
        console.log($this);
        var revision_id = $this.data('id'); 
        console.log(revision_id);
        var url = document.location.pathname + '/' + revision_id;
        $.ajax(url)
            .done(function(data){
                var $modal = $('#modal_revision');
                var $body = $modal.find('.modal-body');
                console.log($body);
                $body.html(data);
                $modal.modal('show'); 
            })
    });
}(jQuery))
