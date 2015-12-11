(function () {
    $('[data-key]').each(function(){
        var $this = $(this);
        var key = $this.attr('data-key-shortcut');
        Mousetrap.bind(key, function(){
            $this[0].click();
            return true;
        });
    });
}(jQuery))
