$(document).ready(function(){
	// 用CKEditor替换<textarea id="editor">
	// 修改默认配置
	var editorContent = CKEDITOR.replace('editor',{
		//font_names: '宋体/SimSun;新宋体/NSimSun;仿宋/FangSong;Arial/Arial, Helvetica, sans-serif;',
		skin: 'moono',//kama moono
		//uiColor: '#fff',
		uiColor: '#9AB8F3',
		toolbarLocation: 'top',//top bottom 
		toolbarCanCollapse: true,
		language: 'zh-cn',
		allowedContent: true,
		removePlugins:  'elementspath',//移除元素路径
		resize_enabled: true, //是否可拖拽

		enterMode: CKEDITOR.ENTER_BR,// 配置Enter是换行
		shiftEnterMode: CKEDITOR.ENTER_P, // 配置Shift + Enter是换段落

		filebrowserUploadUrl: '/ckupload/', //文件上传路径

		extraPlugins: 'preview,colorbutton,font,find',//预览
		font_names:  '宋体/宋体;黑体/黑体;仿宋/仿宋_GB2312;楷体/楷体_GB2312;隶书/隶书;幼圆/幼圆;微软雅黑/微软雅黑;',
		//font_defaultLabel: '微软雅黑',
		//使用搜索时的高亮色
		find_highlight: {
			element : 'span',
			styles : { 'background-color' : '#ff0', 'color' : '#00f' }
		},
	});

	// 监控ckeditor值的变化	--> 实现预览功能
	editorContent.on('change', function(event){
	var data = this.getData();
	console.log(data);
		$("#test1").html(data);
	});

	/*CKEDITOR.instances.editor.on('instanceReady', function (e) {
		CKEDITOR.instances.editor.execCommand('maximize'); // 初始最大化
	});*/
				
	$("#btn1").click(function(){
		// post  
		editorContent.setData('<b>This is for test</b>');
	});
				
	$("#btn2").click(function(){
		//$("#test1").html(editorContent.getData());
		//post 
		editorContent.execCommand('preview');  // 预览
		//CKEDITOR.instances.editor.execCommand('print');  // 打印
	});

	$("#save").click(function(){
		//为了能在后台通过textarea获得值，必须用editor.updateElement()来更新textarea元素
		editorContent.updateElement();
		$("#ckformid").submit();
	});
});



