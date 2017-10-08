$(document).ready(function(){
	var editorContent = CKEDITOR.replace('ckhtml',{
		skin: 'kama',//kama moono
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
		font_names:  '宋体/宋体;黑体/黑体;仿宋/仿宋_GB2312;楷体/楷体_GB2312;隶书/隶书;>    幼圆/幼圆;微软雅黑/微软雅黑;',
		find_highlight: {
			element : 'span',
			styles : { 'background-color' : '#ff0', 'color' : '#00f' }
		},
	});
});


