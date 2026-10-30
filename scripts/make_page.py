h=open('page_head.html').read(); b=open('page_body.html').read(); js=open('step_js.js').read()+'\n'+open('page_js.js').read()
meta=open('web_meta.json').read(); blob=open('web_blob.b64').read()
out=h+b+'<script type="application/json" id="meta">'+meta+'</script>\n<script type="application/octet-stream" id="blob">'+blob+'</script>\n<script>\n'+js+'\n</script>\n'
open('pe_coluna_FD.html','w').write(out); print(len(out))
