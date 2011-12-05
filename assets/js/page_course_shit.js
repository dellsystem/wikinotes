$(document).ready(function() {
	var showAllSemesters = function() {
		$('.page-row').show();
		$('.page-table').show(); // show the tables and the headings
		$('.page-table').each(function() {
			$($(this).prev()[0]).show();
		});
	};
	// The filter by semester enhancement on the course overview page
	$('.semester-filter').click(function() {
		var semester = $(this).attr('data-semester');

		// Hide everything at the end, using a fadeOut()
		var thingsToHide = [];

		$('.page-table').each(function() {
			var numPages = parseInt($(this).attr('data-num-pages'), 10);
			var categoryThingsToHide = []; // don't judge
			$(this).find('.page-row').each(function() {
				var thisPageSemester = $(this).attr('data-semester');
				if (thisPageSemester !== semester) {
					categoryThingsToHide.push($(this));
				}
			});

			// If we need to hide all the rows in the table, just hide the whole table
			if (categoryThingsToHide.length == numPages) {
				thingsToHide.push($(this));
				// Hide the relevant h4 as well
				thingsToHide.push($($(this).prev()[0]));
			}
		});
		showAllSemesters();
		$(thingsToHide).each(function() {
			$(this).hide();
		});
		return false;
	});
	$('#semester-show').click(function() {
		showAllSemesters();
		return false;
	});

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
		$('body').css('overflow-y', 'hidden');
		$('#content-box').addClass('fullscreen');
		var newWidth = $('#main').width() - 35; // not sure
		textareaHeight = $('#content-box textarea').height();
		var newHeight = $('body').height() - 100;
		$('#content-box textarea').width(newWidth).height(newHeight);
		$('#fullscreen').text('Exit fullscreen');
	};

	var exitFullscreen = function(sectionNumber) {
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

	var setEditButtonMessage = function(text, pClass) {
		$($('#edit-buttons p')[0]).attr('class', pClass).text(text);
	};

	var clearEditButtonMessage = function() {
		setEditButtonMessage('', '');
	};

	var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
	$('#preview-pill').click(function() {
		$('#edit-pill').removeClass('active');
		$('#preview-pill').addClass('active');
		$('#content-textarea').hide();
		$('#content-preview').fadeIn(200);
		$.ajax({
			data: {
				'csrfmiddlewaretoken': csrfToken,
				'content': $('#content-textarea').val(),
			},
			dataType: 'html',
			type: 'POST',
			url: '/markdown',
			success: function(data) {
				$('#content-preview').html(data);
				MathJax.Hub.Queue(['Typeset', MathJax.Hub, 'content-preview']);
			},
		});
		$('#edit-buttons').hide();
		return false;
	});

	$('#edit-pill').click(function() {
		$('#preview-pill').removeClass('active');
		$('#edit-pill').addClass('active');
		$('#content-preview').hide();
		$('#content-textarea').show();
		$('#edit-buttons').show();
		return false;
	});

	// The BBCode-like editor not sure what to call it
	var textarea = $($('#content-box textarea')[0]);
	$('.surround-button').click(function() {
		var selection = textarea.getSelection();
		var surroundingShit = $(this).attr('data-surround-with');
		if (selection.length > 0) {
			textarea.replaceSelection(surroundingShit + selection.text + surroundingShit);
			clearEditButtonMessage();
		} else {
			setEditButtonMessage('Please select something first', 'error');
		}
		return false;
	});
	$('.insert-button').click(function() {
		var selection = textarea.getSelection();
		// Insert whatever it is after the start
		var shitToInsert = $(this).attr('data-insert');
		// Assume that the cursor is somewhere because there's no way of checking (0 vs 0)
		textarea.replaceSelection(shitToInsert + selection.text);
		clearEditButtonMessage();
		return false;
	});
	$('.insert-button, .surround-button').mouseover(function() {
		var usage = $(this).attr('data-usage');
		setEditButtonMessage(usage, '');
	});
});
