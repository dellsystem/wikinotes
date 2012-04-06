$(document).ready(function() {
	// Fill the course search box thing first
	$.ajax({
		dataType: 'html',
		url: '/courses/get_all',
		success: function(data) {
			$('#course-search-box').html(data).chosen().change(function() {
				window.location.pathname = $(this).val();
			});
		},
	});

	// If there's an ol on the page ... (MUST be an ol to be considered a q)
	var orderedLists = $('.markdown ol');
	var	answerPrefix = 'ANSWER: '
	var containsQuestion = false;
	if (orderedLists.length > 0) {
		var questionNumber = 1; // for numbering the questions (classes etc)
		// For each ordered list ...
		$.each(orderedLists, function(i, orderedList) {
			// For each li in the ordered list (a potential question)
			var potentialQs = $(orderedList).children();
			$.each(potentialQs, function(j, potentialQ) {
				var answers = $(potentialQ).children().filter('ul').children();

				// Make all the answers bold when you click them
				$(answers).addClass('js-answer');

				// Check if there are at least two "answers" (incl. the explanation)
				if (answers.length < 3) {
					return;
				} else {
					// Still potential - check that the last "answer" starts with ANSWER:
					var lastOne = answers[answers.length - 1];
					var explanation = lastOne.innerText;
					if (explanation.lastIndexOf(answerPrefix, 0) === 0) {
						// Figure out the actual answer
						// Text between the first space and the next space/period/;/,
						var actualAnswer = explanation.substring(answerPrefix.length, answerPrefix.length + 3);
						// Store the actual answer in the question element
						$(potentialQ).attr('data-answer', actualAnswer).addClass('is-question');
						$(lastOne).removeClass('js-answer').html('<a href="#" class="js-show-answer">Show answer &raquo;</a> <span class="js-explanation">' + explanation.substring(answerPrefix.length) + '</span>');
						containsQuestion = true;
					}
				}

				// Make each answer into a radio button
				$.each(answers, function(index, answer) {
					if ($(answer).hasClass('js-answer')) {
						answer.innerHTML = '<label><input type="radio" name="question-' + questionNumber + '" /> <span>' + answer.innerHTML + '</span></label>';
					}
				});
				questionNumber++;
			});
		});

		// Now, only if there are questions on the page ...
		if (containsQuestion) {
			// Now handle clicking of js-show-answer etc
			$('.js-show-answer').click(function() {
				$(this).next().show();
				return false;
			});

			$('.js-answer').click(function() {
				// Remove bold from all the other answers here
				$(this).parent().children().removeClass('answer-clicked');
				$(this).addClass('answer-clicked');
			});

			// Click handler for the reset quiz thing
			$('#js-reset-quiz').click(function() {
				// First, hide the answer statistics thing
				$('#grade-answers span').hide();
				// Remove the correct/incorrect classes from the js-explanations
				$('.js-explanation').removeClass('correct').removeClass('incorrect').hide();
				// Remove the answer-clicked class
				$('.answer-clicked').removeClass('answer-clicked');
				// Clear all the radio buttons
				$('.js-answer input').prop('checked', false);
				return false;
			});

			var setClass = function(object, thisClass, otherClass) {
				if ($(object).hasClass(thisClass)) {
					/// Done, return
					return;
				} else {
					if ($(object).hasClass(otherClass)) {
						$(object).removeClass(otherClass);
					}
					// Just add the class
					$(object).addClass(thisClass);
				}
			};
		
			var setCorrect = function(object) {
				setClass(object, 'correct', 'incorrect');
			};
		
			var setIncorrect = function(object) {
				setClass(object, 'incorrect', 'correct');
			};

			// Click handler for the grade answers thing
			$('#grade-answers').show();
			$('#js-grade-answers').click(function() {
				var questions = $('.markdown ol').find('.is-question');
				var correct = 0;
				var total = 0;
				// For each question, check if the right answer is selected
				$.each(questions, function(i, question) {
					// First store the actual answer
					var actual = $(this).attr('data-answer');
					// Find the selected one
					var selected = $(this).find('.answer-clicked span');

					if (selected.length == 1 && selected[0].innerText.lastIndexOf(actual, 0) === 0) {
						// This one is correct - increment counter, and change class of the showAnswer thing
						correct++;
						setCorrect($(this).find('.js-explanation'));
					} else {
						setIncorrect($(this).find('.js-explanation'));
					}
					total++;
				});
				var percentage = Math.round(correct / total * 100);
				var span = $(this).next();
				// Show the span, then change the values
				$(span).show();
				var values = $(span).find('i');
				$(values[0]).text(correct);
				$(values[1]).text(total);
				$(values[2]).text(percentage);

				// Make it green if total == correct
				if (total == correct) {
					setCorrect(span);
				} else {
					setIncorrect(span);
				}

				// Show all the explanations
				$('.js-explanation').show();
				return false;
			});
		}
	}

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
		var newHeight = $('body').height() - 130;
		$('#content-box textarea').width(newWidth).height(newHeight);
		$('#fullscreen').text('Exit fullscreen');
	};

	var exitFullscreen = function(sectionNumber) {
		$('body').css('overflow-y', 'visible');
		$('#content-box').removeClass('fullscreen');
		$('#content-box textarea').width(930).height(400);
		$('#fullscreen').text('Go fullscreen');
	};

	// Make the tab key enter a tab character instead of going to the next thing
	$('#content-textarea').keydown(function(e) {
		var TABKEY = 9;
		var text = $(this).val();
		// Figure out where the cursor is
		var selection = $(this).getSelection()
		if (e.keyCode == TABKEY) {
			// If shift, de-indent 4 spaces (if possible)
			if (e.shiftKey) {
				// Find the text right before the cursor
				if (selection.length == 0) {
					// Work on selected case later
					var previousNewline = 0;
					var tempText = text;
					while (tempText.indexOf('\n') <= selection.start && tempText.indexOf('\n') >= 0) {
						previousNewline += tempText.indexOf('\n') + 1;
						tempText = tempText.substring(tempText.indexOf('\n') + 1);
					}
					// Strip the first four (or fewer) consecutive space chars after the newline
					var unindentedLine = text.substring(previousNewline, previousNewline + 4).replace(/^ {1,4}/, '');
					var newText = text.substring(0, previousNewline) + unindentedLine + text.substring(previousNewline + 4);
					$(this).val(newText);
				} else {
					$(this).replaceSelection(selection.text.replace(/^ {1,4}/mg, ''));
				}
			} else {
				if (selection.length == 0) {
					$(this).replaceSelection('    ');
				} else {
					$(this).replaceSelection('    ' + selection.text.replace(/\n/g, '\n    '));
				}
			}

			// Prevent the default behaviour
			return false;
		}
	});

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
	$('table').filter('.sort').tablesorter();

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
		$($('#edit-buttons p')[0]).attr('class', pClass).html(text);
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
		// Turn \n into an actual newline (use the g modifier to replace all)
		var shitToInsert = $(this).attr('data-insert').replace(/\\n/g, '\n');
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
