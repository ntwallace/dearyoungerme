block = 2

$(window).scroll(function() {
	if($(window).scrollTop() + $(window).height() === $(document).height()) {  // got to bottom of screen
	  // unhide next divs
	  $("." + block + "").show();
	  block++
	}
});