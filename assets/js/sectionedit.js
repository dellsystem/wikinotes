$(document).ready(function () {
    var baseURL = window.location.pathname;
    var headers = $('.header');
    var i, header, numHeaders, anchor, editLink;
    for (i = 0, numHeaders = headers.length; i < numHeaders; i++) {
        header = headers[i];
        // Get the name of the anchor for this header
        anchor = header.children[1].name;
        // Append an element
        editLink = '<a href="' + baseURL + '/edit?section=' + anchor + '" class="editlink">edit</a>';
        $(header).append(editLink);
    }
});
