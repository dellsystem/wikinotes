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
	
	// Now make the Number of sections dropdown control the number of sections
	var hideExtraSections = function(numSections) {
		$('div[id^=section-]').each(function() {
			// Hide all of the divs with an ID number greater than the selected number of sections
			var thisID = $(this).attr('id');
			var thisIDNumber = parseInt(thisID.substring(thisID.indexOf('-')+1));
			if (thisIDNumber > numSections) {
				$(this).hide();
			} else {
				$(this).show();
				console.log("WTF");
			}
		});
	};
	hideExtraSections($('#id_num_sections').val());
	
	$('#id_num_sections').change(function() {
		hideExtraSections($('#id_num_sections').val());
	});
});
