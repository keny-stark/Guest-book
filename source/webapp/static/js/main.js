$('.js-button-campaign').click(function() {
	$('.js-overlay-campaign').fadeIn();
	$('.js-overlay-campaign').addClass('disabled');
});
$('.js-close-campaign').click(function() {
	$('.js-overlay-campaign').fadeOut();
});

$(function(){
     $('.litle').click(function(){
          var id =  $(this).data('id');
    })
})
$(document).mouseup(function (e) {
	var popup = $('.js-popup-campaign');
	if (e.target!=popup[0]&&popup.has(e.target).length === 0){
		$('.js-overlay-campaign').fadeOut();
	}
});
