$(function(){
    $("a.dropdown-toggle").click(function(e) {
      $(this).parent().toggleClass('open');
      e.preventDefault();
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
        return false;
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
})
