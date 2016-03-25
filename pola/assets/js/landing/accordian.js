(function ($){
  $('.accordian-header').click(function(){
    var accordian = $(this).closest('.accordian');
    accordian.toggleClass('is-open');
    var accprdian_content = accordian.find('.accordian-content');
    var aria_hidden = accprdian_content.attr('aria-hidden');
    if(accordian.hasClass('is-open')){
      accprdian_content.attr('aria-hidden', 'false');
    }else{
      accprdian_content.attr('aria-hidden', 'true');
    }
  });
}) (jQuery);
