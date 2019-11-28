

(function(){
   var $responseTarget = $("#responseTarget");
   var $linkActions = $(".actionItem");

   $linkActions.click(function(){
      var myHref = $(this).attr('href');

      $.ajax({
        url:myHref,
        cache: false,
        success:function(data) {
          $responseTarget.html(data)
        }
      });

      return false;

   });




})();
