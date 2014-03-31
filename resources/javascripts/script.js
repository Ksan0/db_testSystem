$(function(){
	var form = $('.contact-form');
	var auto_agree=true;
	$("#send_sql").click(function() {
		if(!auto_agree){
			$(".confirm").show();
		}
	}	
//Timer
	if ($(".session_timer > a:nth-child(1)").length) {
		var Interval = setInterval(function(){
			var timer = parseInt($(".session_timer > a:nth-child(1)")[0].text.match(/\d+/));
			if (timer-1 > 0)	{
				$(".session_timer > a:nth-child(1)").html("Осталось "+(timer-1)+" min");
			} else {
				$(".session_timer > a:nth-child(1)").html("Время вышло");
				clearInterval(Interval);
			}
		}, 6000);
		$(".session_timer > a:nth-child(1)").html("Осталось "+parseInt($(".session_timer > a:nth-child(1)")[0].text.match(/\d+/))+" min");
	}

//выпадающее меню на профайл
	$("a.dropdown-toggle").click(function(e) {
		if($(".dropdown-menu").css('display') != 'block'){
      		$(".dropdown-menu").show();
			var click = true;
			$(document).bind('click.myEvent', function (e) {
          		if (!click && $(e.target).closest('.dropdown-menu').length == 0) {
            	$(".dropdown-menu").hide();
            	$(document).unbind('click.myEvent');
          	}
			click = false;
        });
		}
	});
	$("a.dropdown-menu").mouseleave(function(e){
       	$(".dropdown-menu").css("display", "none");
   	});

//Проверка ответа на сервере и разбор в таблицу
	$("#ajax-check-sql").click(function() {
        var form = $('.contact-form');
		var get = parseGetParams();
        $.post(
            "/test_answer/?testid="+get.testid+"&queid="+get.queid, //url
            form.serialize(),
            function(data) {      //success method
				data = jQuery.parseJSON($.parseHTML(data)[0].data.replace(/ u\'/g, " \'").replace(/: (?=[0-9])/g,": '").replace(/L,/g,"',").replace(/'/g,"\"").replace(/None/g,"\"None\""));
				var result;
				for(var k in data[0]){
					if (k == 'sql_query_error') { result="error"; break;}
				}
				if( result == "error"){
					result = "sql_query_error:" + data[0]['sql_query_error'];
				} else {
					result = "<table class=\"table\">\n<thead>\n<tr>\n";
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
				}
				$(".messages").append(result);
            }
        );
	});

//Восстановление пароля
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
