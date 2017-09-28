$(document).ready(function(){
	// 用CKEditor替换<textarea id="editor">
	// 修改默认配置
	var editorContent = CKEDITOR.replace('ckdemo',{
		//font_names: '宋体/SimSun;新宋体/NSimSun;仿宋/FangSong;Arial/Arial, Helvetica, sans-serif;',
		skin: 'kama',//kama moono
		//toolbar: 'Full',//Basic Full 自定义
		//uiColor: '#fff',
		//uiColor: '#9AB8F3',
		toolbarLocation: 'top',//top bottom 
		toolbarCanCollapse: true,
		language: 'zh-cn',
		allowedContent: true,
		removePlugins:  'elementspath',//移除元素路径
		resize_enabled: true, //是否可拖拽

		enterMode: CKEDITOR.ENTER_BR,// 配置Enter是换行
		shiftEnterMode: CKEDITOR.ENTER_P, // 配置Shift + Enter是换段落

		filebrowserUploadUrl: '/ckupload/', //文件上传路径

		extraPlugins: 'preview,colorbutton,font,find,save',//预览
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
});



