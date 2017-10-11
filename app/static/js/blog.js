/*文档就绪事件*/
$(document).ready(function(){
	//console.log('11111111111111');
	//console.log('**********'+$('.post-body').outerHeight()+'*************');
	/*$('li.listBox').each(function(index,domEle){
		//console.log('############'+$(domEle).outerHeight()+'################');
		//设置超出隐藏的高度，如果小于454内容全部显示，否则隐藏超出内容
		if($(domEle).outerHeight()<454){
			console.log('22222222222222');
			console.log($(domEle).children('div.listBoxCenter').html());
			//$(domEle).children('div.listBoxCenter').css('height',);
		}else {
			$(domEle).children('div.listBoxCenter').css("height","250px");
		}
	});*/
		
	//当鼠标移动到id=searchSubmit元素上
	$('#searchSubmit').mouseenter(function(){
		$(this).css('color','#1256cc');
		$(this).css('font-size','15px');
	});

	//当鼠标移开id=searchSubmit元素时
	$("#searchSubmit").mouseleave(function(){
		$(this).css('color','#000');	
		$(this).css('font-size','14px');
	});	

	$("#searchSubmit").click(function(){
		$(this).css('color','rgb(201, 4, 213)');
		$('#searchForm').submit();
		console.log('提交搜索表单');
	});
});


