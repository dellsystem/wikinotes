$(document).ready(function () {
    "use strict";

    $('.markdown h2').click(function(){
      $(this).nextUntil('h2').toggle();
    });
    $('.markdown h3').click(function(){
      var tillh2 = $(this).nextUntil('h2');
      var tillh3 = $(this).nextUntil('h3');
      if (tillh2.size() < tillh3.size()) {
        tillh2.toggle();
      } else {
        tillh3.toggle();
      }
    });

    // not bothering with h4, too deep, who cares about that??
});
