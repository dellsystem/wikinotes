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
	
	// When you select a term, change the months available
	// Obviously we have to do server-side validation as well
	$('#id_term').change(function() {
		hideExtraMonths($('#id_term').val());
	});
	
	var hideExtraMonths = function(term) {
		// Winter = first four months, summer = second four, etc
		var i = 1;
		var lowerBounds = {'winter': 1, 'summer': 5, 'fall': 9};
		var upperBounds = {'winter': 4, 'summer': 8, 'fall': 12};
		$('#id_month option').each(function() {
			if (i < lowerBounds[term] || i > upperBounds[term]) {
				console.log("i is " + i);
				$(this).hide();
			} else {
				$(this).show();
			}
			i++;
		});
	};
	// Do this automatically too
	hideExtraMonths($('#id_term').val());
	
	$('#add-button').click(function(event) {
		$('#choose-page-box').modal();
		return false;
	});
	
	$('#add-section').click(function(event) {
		// Find the last visible section
		var thisIDNumber;
		var thisID;
		$('div[id^=section-]').not(':hidden').each(function() {
			thisID = $(this).attr('id');
			thisIDNumber = parseInt(thisID.substring(thisID.indexOf('-')+1));
			console.log(thisID + ' is NOT HIDDEN LOL');
		});
		// Now check if the new section is already present in the document
		var nextIDNumber = thisIDNumber + 1;
		var nextID = 'section-' + nextIDNumber;
		console.log(nextID);
		if ($('#' + nextID).length > 0) {
			// Show it
			$('#' + nextID).show()
		} else {
			// Duplicate the last section element, change its ID and contents, then append it
			console.log("ADD A NEW ONE");
			console.log(thisID);
			$('#' + thisID).after($('#' + thisID).clone().attr('id', nextID));
		}
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
			}
		});
	};
	hideExtraSections($('#id_num_sections').val());
	
	$('#id_num_sections').change(function() {
		hideExtraSections($('#id_num_sections').val());
	});
});
