// Some jQuery for controlling the add a page and watch this course buttons
$(document).ready(function() {
	$('#watch-button').click(function() {
		alert("send off a JSON request");
		$.post('', function(data) {
			if (data == 'lol') {
				alert("notlol");
			} else {
				alert("lol");
			}
		});
	});
	
	$('#add-button').click(function(event) {
		$('#choose-page-box').modal();
		return false;
	});
});
