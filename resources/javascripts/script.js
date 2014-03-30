$(function(){
    $("a.dropdown-toggle").click(function(e) {
      $(".dropdown-menu").css("display", "block");
    });

    $("#ajax-check-sql").click(function() {
        var form = $('.contact-form');
        $.post(
            "ajax/answer?type=answer&testid=ID&queid=ID", //url
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
