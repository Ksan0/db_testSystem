$(function(){
	var form = $('.contact-form');
	var auto_agree=true;
	$("#send_sql").click(function() {
		if(!auto_agree){
			$(".confirm").show();
		}
	});	

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
		}, 60000);
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

//Проверка ответа на сервере и разбор в таблицу
	$("#ajax-check-sql").click(function() {
        var form = $('.contact-form');
		var get = parseGetParams();
        $.post(
            "/test_answer/?testid="+get.testid+"&queid="+get.queid, //url
            form.serialize(), function(data) {
                console.log(data);
				dataToTable(data,".messages",1);
			}
        );
	});

// by Ksan. Не работает, нужно допилить
    $(".ajax-check-sql-admin").click(function() {
        // id : $("#id_answer")[0].baseURLOD.
		$.post(
            "/ajax", //url
            {
				message: $("#id_answer")[0].value,
				url : $("#id_answer").context.URL
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

//Статистика у админа
	$(".users").ready(function() {
		$(".answer").each(function() {
			dataToTable(this.textContent,this,1);
		});
	});
	
//Навигация у админа в статистиске юзера
	$(".rk-headers > li:nth-child(1)").addClass("active");

	$(".rk-headers > li").click(function() {
		$(".rk-headers > li").each(function() {
			$(this).removeClass("active")
		});
 		$(this).addClass("active");
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

function dataToTable(data, elem, clear) {      //success method
    if (!elem) return;
	try {
		data = jQuery.parseJSON(data);
		var result;	
    	if(data.sql_query_error){
			if(clear) $(elem).empty;
            if(data.sql_query_error != "empty_query") result = "sql_query_error: \"" + data.sql_query_error+"\"";
		} else if(data[0]) {
       		result = "<table class=\"table\" back>\n<thead>\n<tr>\n";
        	for(var k in data[0]){
        		result+="<th>"+k+"</th>\n";
   			}
        	result+="</tr></thead>\n<tbody style=\"background-color:transparent\">\n";
	   	 	for(var k in data){
    			result+="<tr>";
        		for(var j in data[k]){
        			result+="<th>"+data[k][j]+"</th>";
       	 		}
        		result+="</tr>\n";
    		}
   			result +="</tbody>\n</table>";
   		}
		if(clear) $(elem).empty();
    	if(!result) $(elem).append("<h4>Empty set</h4>");
		$(elem).append(result);
    } catch(err) {
		console.log(err,data);
		if(clear) $(elem).empty();
		$(elem).append("<h4>"+data+"<h4>");

	}
}
