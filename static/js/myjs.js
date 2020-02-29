$(document).ready(function(){

	$('.tabs').tabs();


	// $('.sidenav2').sidenav();

	$('[data-fancybox]').fancybox({
		speed : 330,
		loop : true,
		opacity : 'auto',
		gutter : 30,
		infobar : false,
		 buttons: [
       	 "close"
   		 ],
   		 transitionEffect: "fade",

	});




	$('.mobile_nav_dots').click(function(){
		$('.search_catalog2').slideToggle(300);
		console.log('click');
		return false;
	});





	var bazPrice = 10000;
	var dopPrice = 0;
	var tottaly;
	var lesskm = $('.lesskm');
	var morekm = $('.morekm');


	$('.promezutok').text(dopPrice);
	$('.totall').text(bazPrice);
	$('.price_tovar').text(bazPrice);





	lesskm.change(function(){

		if($(this).is(':checked')) {
			var newCifra = lesskm.val();
			$('.promezutok').text(newCifra);
			var newTotal = bazPrice + +newCifra;
			$('.totall').text(newTotal);			
		}


		else{
			var newCifra = dopPrice;
			$('.promezutok').text(newCifra);
			var newTotal = bazPrice + +newCifra;
			$('.totall').text(newTotal);
		
		}
	});


	$('.morekm').change(function(){

		if($(this).is(':checked')){
			var lastCifra = morekm.val();
			$('.promezutok').text(lastCifra);
			var lastTotal = bazPrice + +lastCifra;
			$('.totall').text(lastTotal);

		}
		else{
			var lastCifra = dopPrice;
			$('.promezutok').text(lastCifra);
			var lastTotal = bazPrice + +lastCifra;
			$('.totall').text(lastTotal);
		}
	});



});