

/*
(function(){
  var $responseTarget = $("#responseTarget");
  var $linkActions = $(".actionItem");

  // $linkActions.click(function(){
     var myHref = $(this).attr('href');

     $.ajax({
       url:myHref,
       cache: false,
       success:function(data) {
         $responseTarget.html(data)
       }
     });
     return false;
  // });
})();
*/
console.log('online');

// (function(){
  console.log('inside');
  let song_library_header = document.querySelector('#song_library_header');
  let filter_header = document.querySelector('#filter_header');
  filter_header.addEventListener('click', function(event){
    if (event.target.attributes["data-type"]) {

      let attr_tag = event.target.attributes["data-type"];
      console.log('you clicked the header', attr_tag);
      // remove active class from all tabs
      let all_filter_sections = document.querySelectorAll('.filter_section');
      all_filter_sections.forEach(element => {
        element.classList.remove('active');
      });
      // apply active class to target
      document.getElementById(event.target.id).classList.add('active');
      
      // hide all filter bodies
      let all_filter_bodies = document.querySelectorAll('.filter_body');
      all_filter_bodies.forEach(element => {
        element.classList.add('hide');
      });
  
      // toggle body content
      //  #song_library_wrapper
      //  #upload_wrapper
      event.target.id === 'upload_header' ? 
        document.querySelector('#song_library_wrapper').classList.add('hide')  :
        document.querySelector('#song_library_wrapper').classList.remove('hide');
      
  
      // show filter body with matching attribute class
      document.querySelector(`.filter_body[data-type="${attr_tag.value}"]`).classList.remove('hide');
    }
  });
// });

function replaceQueryString( queryString, keys, newValues ) {
  var parts = queryString.split('&');

  // We're going to make an array of querystring key=value strings
  var new_parts = [];

  for( i in parts ) {
      var keyValue = parts[i].split('=');

      // Use jQuery to see if this key is in our desired set
      var replacePos = $.inArray(keyValue[0],keys);

      // If it is, it will give a non-negative integer, if not it'll give -1
      if( replacePos >= 0 )
          // We want to replace this key so make a new string for the key/value pair
          new_parts.push( keyValue[0] + '=' + newValues[replacePos] );
      else {
          // This isn't the key we want to replace, so leave it alone
          new_parts.push( parts[i] );
      }
  }
  // glue all the parts together and return them
  return new_parts.join('&');
}


// Form Upload
$("form#uploadMaSong").submit(function(e) {

  var postDataUrl = $("form#uploadMaSong").attr('action');
  var formData = new FormData($(this)[0]);

  $.ajax({
      type: "POST",
      url: postDataUrl,
      data: formData,
      enctype: 'multipart/form-data',
      processData: false,
      contentType: false,
      cache: false,
      timeout: 600000,
      success: function(data, textStatus, jqXHR) {
         alert('nice')
      },
      error: function(data, textStatus, jqXHR) {
         alert('naw')
      }

  });

  return false;

 });

  $('#inputGroupFile01').on('change',function(){

      //get the file name
      var fileName = $(this).val();
      console.log(fileName)
      //replace the "Choose a file" label
      $('#fileNameTarget').html(fileName);
  });