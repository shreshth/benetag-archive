$(document).ready(function() {
	$("a[rel=popover]")
		.popover({
			offset: 10,
			template: '<div class="popover"><div class="arrow"></div><div class="popover-inner fit-content"><h4 class="popover-title"></h4></div></div>',
		})
});