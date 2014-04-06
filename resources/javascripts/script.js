$(function(){
	var form = $('.contact-form');
	var auto_agree=true;
	$("#send_sql").click(function() {
		if(!auto_agree){
			$(".confirm").show();
		}
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
				dataToTable(data,".messages",1);
			}
        );
	});

//Проверка у админа 
    $(".ajax-check-sql-admin").click(function() {
		$.post(
            "/custom-admin/test_question/", //url
            {
				message: $("#id_answer")[0].value,
				csrfmiddlewaretoken: $("#question_form")[0][0].value
			}, function(data) {
				dataToTable(data,".sql-check-table-admin",1);
			}	
        );
	});
//Для пересчета показателя вопроса
	$(".ajax-recalc-que-admin").click(function() {
		$.post(
			"/custom-admin/question_action/?type=recalc",
			{
				url: $(this).baseURL,
				csrfmiddlewaretoken: $("#question_form")[0][0].value
			}, function(data) {
				$(".ajax-recalc-que-admin-success").empty();
				if (data) $(".ajax-recalc-que-admin-success").append("Показатели пересчитаны");
				else $(".ajax-recalc-que-admin-success").append(data);
			}
		);
	});
// Зачесть вопрос как правильный
    $(".ajax-make-que-right-admin").click(function() {
		$.post(
			"/custom-admin/OOO",
			{
				url: $(this).baseURL,
				// csrfmiddlewaretoken: $("#question_form")[0][0].value
			}, function(data) {
				$(".ajax-recalc-que-admin-success").empty();
				if (data) $(".ajax-recalc-que-admin-success").append("Показатели пересчитаны");
				else $(".ajax-recalc-que-admin-success").append(data);
			}
		);
	});
//Статистика у админа
	$(".users").ready(function() {
		$(".answer").each(function() {
			dataToTable(this.textContent,this,1);
		});
	});
	
//Навигация у админа в статистиске юзера
	$(".rk-headers > li:first").addClass("active");
	$(".rk-view:first").addClass("active");
    
	$(".rk-headers > li").click(function() {
		$(".active").removeClass("active");
 		$(this).addClass("active");
		$($(this).attr("name")).addClass("active");
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
