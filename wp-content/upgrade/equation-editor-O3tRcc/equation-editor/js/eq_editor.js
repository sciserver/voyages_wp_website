var popupEqnEditorwin = null; 
(function() {
	var eq_protocol = window.location.protocol;
	tinymce.create('tinymce.plugins.equation', {
		init: function(ed, url) {
			ed.addCommand('eqCmd', function(a, latex)	{
																					
				if (popupEqnEditorwin==null || popupEqnEditorwin.closed || !popupEqnEditorwin.location) 
				{
					var url = eq_protocol+'//latex.codecogs.com/editor_json3.php?type=url&editor=TinyMCE';
			
					if(latex!==undefined) 
					{	
						latex=unescape(latex);
						latex=latex.replace(/\+/g,'&plus;');
						url+='&latex='+escape(latex);
					}
					
					popupEqnEditorwin=window.open('','LaTexEditor','width=700,height=450,status=1,scrollbars=yes,resizable=1');
					if (!popupEqnEditorwin.opener) popupEqnEditorwin.opener = self;
					popupEqnEditorwin.document.open();
					popupEqnEditorwin.document.write('<!DOCTYPE html><head><script src="'+url+'" type="text/javascript"></script></head><body></body></html>');
					popupEqnEditorwin.document.close();
				}
				else if (window.focus) 
				{ 
					popupEqnEditorwin.focus()
					if(latex!==undefined)
					{
						latex=unescape(latex);
						latex = latex.replace(/\\/g,'\\\\');
						latex = latex.replace(/\'/g,'\\\'');
						latex = latex.replace(/\"/g,'\\"');
						latex = latex.replace(/\0/g,'\\0');

						eval("var old = popupEqnEditorwin.document.getElementById('JSONload')");
						if (old != null) {
							old.parentNode.removeChild(old);
							delete old;
						}
						
						var head = popupEqnEditorwin.document.getElementsByTagName("head")[0];
						var script = document.createElement("script"); 
						script.type = "text/javascript";  
						script.id = 'JSONload';
						script.innerHTML = 'EqEditor.load(\''+(latex)+'\');';
						head.appendChild(script);
					
          }
				}
																																									

			});
					
		  ed.addButton('equation', {
				title: 'Equation Editor',
				image: url + '/images/fx.png',
				cmd: 'eqCmd' });
			
			ed.onDblClick.add(function(ed, e) {
				var eq_protocol = window.location.protocol;
				if (e.target.nodeName.toLowerCase() == "img") {
					if (eq_protocol == 'https:') {
						 alert('https:');
					var sName = e.target.src.match( /https:\/\/(latex.codecogs.com)\/(gif|svg)\.latex\?(.*)/ );
					} else {
						alert('http:')
					var sName = e.target.src.match( /http:\/\/(latex.codecogs.com)\/(gif|svg)\.latex\?(.*)/ );	
					}
				
	      	if(sName[1]=='latex.codecogs.com')
		        tinymce.execCommand('eqCmd', false, sName[3]);
				}
			});
			
	  }, 
	
	  createControl : function(n, cm) { return null; } 
  });

  tinymce.PluginManager.add('equation', tinymce.plugins.equation);
})();

TinyMCE_Add = function( name )
{
	var eq_protocol = window.location.protocol;
	if (eq_protocol == 'https:') {
	  name = name.replace(/^http:\/\//i, 'https://');
	}
	var sName = name.match( /(gif|svg)\.latex\?(.*)/ );
	var latex= unescape(sName[2]);
	latex = latex.replace(/@plus;/g,'+');
	latex = latex.replace(/&plus;/g,'+');
	latex = latex.replace(/&space;/g,' ');
	
	tinyMCE.activeEditor.execCommand('mceInsertContent', false, '<img src="'+name+'" alt="'+latex+'" align="absmiddle" />');
	tinyMCE.execCommand('mceFocus', false, tinymce.activeEditor.editorId);
}