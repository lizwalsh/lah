
$(function() {
	// get enter
	var konami_keys = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65, 13];
	var konami_index = 0;
	
	var barrel_keys = [68, 79, 32, 65, 32, 66, 65, 82, 82, 69, 76, 32, 82, 79, 76, 76];
	var barrel_index = 0;
	$(document).keydown(function(e){
		if(e.keyCode === konami_keys[konami_index++]){
			if(konami_index === konami_keys.length){
				if ( $("#hide").text() == "wolf" ) {
					$("#img_container").css({
						"background-image" : 'url("/static/comics/images/nick_bg.png")',
						"background-repeat" : "no-repeat",
						"background-position" : "0px 120px"
						
					});
					$("#hide").text("nick");
					
				} else {
					$("#img_container").css({
						"background-image" : 'url("/static/comics/images/nick_bg_wolf.png")',
						"background-repeat" : "no-repeat",
						"background-position" : "0px 120px"
					});
					$("#hide").text("wolf");
				}
			
				konami_index = 0;
			}
		}else{
			konami_index = 0;
		}
		
		if(e.keyCode === barrel_keys[barrel_index++]){
			if (barrel_index === barrel_keys.length) {
				$('body').addClass('barrel_roll');
				setTimeout(function() { $('body').removeClass('barrel_roll'); }, 4000);
				barrel_index = 0;
			}
		} else {
			barrel_index = 0
		}
		
	});
	
	$("a[href=#menuExpand]").click(function(e) {
        $(".menu").toggleClass("menuOpen");
        e.preventDefault();
    });

    
    $(window).load(function ( ) {
	    $('#navbuts').css('margin-top', $('#comic_holder').height() )
    });
    
    $(window).resize(function () {
    	$('#navbuts').css('margin-top', $('#comic_holder').height() );
    });

});

function checkBGImages() {
	if ( $(window).width() <= 1192 )  {
		$("body").css({
			"background-image" : 'url("/static/comics/images/bg_image_stuff.png")',
			"background-repeat" : "repeat-x",
			"background-position" : "fixed"
		});
	} else {
		if ( $("#hide").text() == "wolf" ) {
			$("#img_container").css({
				"background-image" : 'url("/static/comics/images/nick_bg_wolf.png")',
				"background-repeat" : "no-repeat",
				"background-position" : "0px 120px"
			});
			
		} else {
			$("#img_container").css({
				"background-image" : 'url("/static/comics/images/nick_bg.png")',
				"background-repeat" : "no-repeat",
				"background-position" : "0px 120px"
			});
			
		}
		
	}
}



