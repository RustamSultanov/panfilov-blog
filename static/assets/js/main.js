// Auto update layout
if (window.layoutHelpers) {
  window.layoutHelpers.setAutoUpdate(true);
}

$(function() {
  // Initialize sidenav
  $('#layout-sidenav').each(function() {
    new SideNav(this, {
      orientation: $(this).hasClass('sidenav-horizontal') ? 'horizontal' : 'vertical'
    });
  });

  // Initialize sidenav togglers
  $('body').on('click', '.layout-sidenav-toggle', function(e) {
    e.preventDefault();
    window.layoutHelpers.toggleCollapsed();
  });

  // Swap dropdown menus in RTL mode
  if ($('html').attr('dir') === 'rtl') {
    $('#layout-navbar .dropdown-menu').toggleClass('dropdown-menu-right');
  }
});
$( document ).ready(function() {

	$('#project-stage input[type = checkbox]').on('click', function(){
		var btn = $(this).closest(".row").find(".btn");
		if($(this).is(':checked')){
			$(btn).removeClass('disabled');
    } else{
			$(btn).addClass('disabled');
    }
	});

	$('#project-stage .btn').on('click', function () {
		$(this).closest(".row").find("input[type = checkbox]").attr('disabled', true);
		$(this).addClass('disabled');
	});

	$('.project-guarantee__show-block').on('click', function () {
		if($('.project-guarantee__block').hasClass('hidden-block')){
			$('.project-guarantee__block').removeClass('hidden-block');
		}
	});


		$(".main_input_file").change(function() {

			var f_name = [];

			for (var i = 0; i < $(this).get(0).files.length; ++i) {

				f_name.push(" " + $(this).get(0).files[i].name);

			}

			$("#f_name").val(f_name.join(", "));
		});

});