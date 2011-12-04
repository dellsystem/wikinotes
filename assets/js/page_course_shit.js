$(document).ready(function() {
	$('input, textarea').placeholder();
	// for a decent fallback if JS is disabled ...
	$('#create-page-popup').hide();
	$('#create-page-button').click(function() {
		$('#create-page-popup').addClass('modal');
		$('#create-page-popup').after('<div class="modal-backdrop"></div>');
		$('#create-page-popup .modal-footer').append('<button class="btn danger" id="close-modal">Close this box</button>');
		$('#create-page-popup').show();
		$('#create-page-popup button').click(function() {
			$('.modal-backdrop').remove();
			$('#create-page-popup').hide();
			$('#create-page-popup button').remove();
		});
	});
	$('#add-section').click(function(event) {
		// Find the last visible section
		// This code needs to be optimised (later)
		var thisIDNumber;
		var thisID;
		$('fieldset[id^=section-]').not(':hidden').each(function() {
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
			$('#' + nextID).show();
		} else {
			// Duplicate the last section element, change its ID and contents, then append it
			console.log("ADD A NEW ONE");
			console.log(thisID);
			// MONKEY don't forget to change all the other stuff too (id, name, text between span, etc)
			$('#' + thisID).after($('#' + thisID).clone().attr('id', nextID));
		}
		// Increase the number of sections in the input field
		$('#num_sections').val('' + (parseInt($('#num_sections').val(), 10) + 1));
		event.preventDefault;
		return false;
	});

	// Now make the Number of sections dropdown control the number of sections
	var hideExtraSections = function(numSections) {
		$('fieldset[id^=section-]').each(function() {
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
	hideExtraSections(1);

	var inFullscreen = false;
	$('#fullscreen').click(function(event) {
		if (inFullscreen) {
			exitFullscreen();
		} else {
			enterFullscreen();
		}
		inFullscreen = !inFullscreen;
		return false;
	});

	var textareaHeight;
	var enterFullscreen = function() {
		console.log("entering fullscreen");
		$('body').css('overflow-y', 'hidden');
		$('#content-box').addClass('fullscreen');
		var newWidth = $('#main').width() - 35; // not sure
		textareaHeight = $('#content-box textarea').height();
		var newHeight = $('body').height() - 100;
		$('#content-box textarea').width(newWidth).height(newHeight);
		$('#fullscreen').text('Exit fullscreen');
	};

	var exitFullscreen = function(sectionNumber) {
		console.log("exiting fullscreen");
		$('body').css('overflow-y', 'visible');
		$('#content-box').removeClass('fullscreen');
		$('#content-box textarea').width(930).height(400);
		$('#fullscreen').text('Go fullscreen');
	};

	// Multiple choice quizzes, clicking on the "view answer" thing etc
	$('p[id^="answer-q"]').hide();
	$('a[id^="view-answer-q"]').click(function(event) {
		event.preventDefault();
		var thisID = $(this).attr('id');
		var answerID = thisID.substring(5);
		// Soooo hacky, needs to be improved
		$('#' + answerID).show();
		var questionID = thisID.substring(13);

		// now bold the relevant li
		var rightAnswerID = '#q' + questionID + ''; // fuck it
		return false;
	});

	// Tables are by default sortable, add the nosort class to prevent that
	// http://tablesorter.com/docs/example-meta-sort-list.html for initial sorting order
	$('table').not('.nosort').tablesorter();

	// Dynamically set tabindex, I'm sorry but it really is difficult to do this otherwise
	var tabindex = 1;
    $('input, select, textarea').each(function() {
        if (this.type !== "hidden") {
            $(this).attr("tabindex", tabindex);
            tabindex++;
        }
    });
	$('.radio-button input').hide();
	$('.radio-button').click(function() {
		$(this).siblings().removeClass('success');
		$(this).addClass('success');
	});
});
