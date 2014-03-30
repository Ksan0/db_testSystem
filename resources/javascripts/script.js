$(function(){
	var form = $('.contact-form');
		
    $("a.dropdown-toggle").click(function(e) {
      	$(".dropdown-menu").css("display", "block");
    e.PreventDefault();
	});

    $("#ajax-check-sql").click(function() {
        var form = $('.contact-form');
		var get = parseGetParams();
        $.post(
            "/test_answer/?testid="+get.testid+"&queid="+get.queid, //url
            form.serialize(),
            function(data) {      //success method
                $('#messages').html(data);
            }
        );
	});

    $(".restore_link").click(function() {
		$(".login_form").css("display","none");
		$(".restore_form").css("display","block");
	});
	
	$(".login_link").click(function() {
    	$(".login_form").css("display","block");
    	$(".restore_form").css("display","none");
    });

});

function parseGetParams() { 
   var $_GET = {}; 
   var __GET = window.location.search.substring(1).split("&"); 
   for(var i=0; i<__GET.length; i++) { 
      var getVar = __GET[i].split("="); 
      $_GET[getVar[0]] = typeof(getVar[1])=="undefined" ? "" : getVar[1]; 
   } 
   return $_GET; 
} 
//  $('#ajax-check-sql').click(function(e) {
//      e.preventDefault();
//      $.ajax({
//          type: "POST",
//          url: "/test/ajax/attempt-sql/",
//          dataType: "json",
//          data: {
//              'csrfmiddlewaretoken':$( "#csrfmiddlewaretoken" ).val(),
//              'sql': $(this).serialize()
//          }
//          ,
//          success: function(data) {
//              $('p').html('ok');
//              alert(1);
//          },
//          error: function(data) {
//
//          }
//      });
//  })
