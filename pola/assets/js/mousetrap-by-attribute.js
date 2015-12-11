(function () {
    console.log("mousetra-by-attribute.js");
    $('[data-key]').each(function(){
        var $this = $(this);
        console.log($this);
        var key = $this.attr('data-key-shortcut');
        console.log('key:' + key);
        Mousetrap.bind(key, function(){
            console.log(key);
            console.log('clicked');
            $this[0].click();
            return true;
        });
    });
}(jQuery))
