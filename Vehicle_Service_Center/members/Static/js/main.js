(function ($) {
  //Add OnepageNav / Sidebar
  function onePageFixedNav() {
	  if($('body').length){
		// Add scrollspy to 
		$('body').scrollspy({target: ".theme-main-header", offset: 70});   

		// Add smooth scrolling on all links inside the one-page-menu
		$(".one-page-menu li a").on('click', function(event) {
		  // Make sure this.hash has a value before overriding default behavior
		  if (this.hash !== "") {
			// Prevent default anchor click behavior
			event.preventDefault();

			// Store hash
			var hash = this.hash;

			// Using jQuery's animate() method to add smooth page scroll
			// The optional number (800) specifies the number of milliseconds it takes to scroll to the specified area
			$('html, body').animate({
			  scrollTop: $(hash).offset().top
			}, 1000, function(){
		
			  // Add hash (#) to URL when done scrolling (default click behavior)
			  window.location.hash = hash;
			});
		  }  // End if
		});
	  }
  }


  // Sticky header
  function stickyHeader () {
	if ($('.theme-main-header').length) {
	  var sticky = $('.theme-main-header'),
		scroll = $(window).scrollTop();
	
	  if (scroll >= 100) sticky.addClass('fixed');
	  else sticky.removeClass('fixed');
	  
	};
  }

  // Tooggle Home page menu click Function 
  function subMenuExpend () {
	if($(".theme-main-header").length) {
	  $('.theme-main-header li.dropdown-holder').append(function () {
	  return '<i class="fa fa-angle-down"></i>';
	  });
	  $('.theme-main-header li.dropdown-holder .fa').on('click', function () {
	  $(this).parent('li').children('ul').slideToggle();
	  });
	}
  }

  function scrollToTop () {
	if ($('.scroll-top').length) {
	
	  //Check to see if the window is top if not then display button
	  $(window).on('scroll', function (){
	  if ($(this).scrollTop() > 200) {
		$('.scroll-top').fadeIn();
	  } else {
		$('.scroll-top').fadeOut();
	  }
	  });
	  
	  //Click event to scroll to top
	  $('.scroll-top').on('click', function() {
	  $('html, body').animate({scrollTop : 0},1500);
	  return false;
	  });
	}
  }

  $(".testimonial-carousel").owlCarousel({
	autoplay: true,
	smartSpeed: 1000,
	center: true,
	margin: 25,
	dots: true,
	loop: true,
	nav : false,
	responsive: {
	  0:{
		items:1
	  },
	  768:{
		items:2
	  },
	  992:{
		items:3
	  }
	}
  });

})(jQuery);
