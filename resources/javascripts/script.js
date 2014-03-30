$(function(){
	var form = $('.contact-form');
		
	var Interval = setInterval(function(){
		var timer = parseInt($(".nav > li:nth-child(2) > a:nth-child(1)")[0].text.match(/\d+/));
		if (timer-1 > 0)	{
			$(".nav > li:nth-child(2) > a:nth-child(1)").html("Осталось "+(timer-1)+" min");
		} else {
			$(".nav > li:nth-child(2) > a:nth-child(1)").html("Время вышло");
			clearInterval(Interval);
		}
	}, 60000);
	$(".nav > li:nth-child(2) > a:nth-child(1)").html("Осталось "+parseInt($(".nav > li:nth-child(2) > a:nth-child(1)")[0].text.match(/\d+/))+" min");

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
				data = jQuery.parseJSON($.parseHTML(data)[0].data.replace(/ u\'/g, " \'").replace(/: (?=[0-9])/g,": '").replace(/L,/g,"',").replace(/'/g,"\"").replace(/None/g,"\"None\""));
				var result = "<table class=\"table\">\n<thead>\n<tr>\n";
				var keys = [];
				for(var k in data[0]){
					result+="<th>"+k+"</th>\n";
				}
				result+="</tr></thead>\n<tbody>\n";
				for(var k in data){
					result+="<tr>";
					for(var j in data[k]){
						result+="<th>"+data[k][j]+"</th>";
					}
					result+="</tr>\n";
				}	
				result +="</tbody>\n</table>";
				$(".messages").append(result);
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
