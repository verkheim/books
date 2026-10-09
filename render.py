"""Render one Books page. No network, credentials, routes or deployment operations."""
import copy,html,json,re,sys
from pathlib import Path
ROOT=Path(__file__).parent
ESC=lambda s:html.escape(str(s),quote=False)
def rich(s):
    from html.parser import HTMLParser
    from urllib.parse import urlsplit
    class Validator(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag not in {'p','br','strong','em','b','i','u','s','ul','ol','li','blockquote','h2','h3','h4','a'}:
                raise ValueError('Unsupported formatted-content tag: '+tag)
            for name,value in attrs:
                if tag!='a' or name not in {'href','title'}:
                    raise ValueError('Unsupported formatted-content attribute: '+name)
                if name=='href' and urlsplit(value or '').scheme not in {'http','https'}:
                    raise ValueError('Formatted links must use HTTP or HTTPS')
        def handle_startendtag(self,tag,attrs):self.handle_starttag(tag,attrs)
    Validator(convert_charrefs=True).feed(s)
    return s

def render(data):
    base=json.loads((ROOT/'render-baseline.json').read_text())
    old=base['data'];out=base['shell'];seen=set()
    if [s['id'] for s in data['sections']] != [s['id'] for s in old['sections']]:
        raise ValueError('Keep the six established sections in their original order')
    for sec in data['sections']:
        cards=[]
        for b in sec['books']:
            bid=b.get('id','')
            if bid:
                if bid in seen: raise ValueError('Duplicate book ID')
                seen.add(bid)
            record=base['cards'].get(bid)
            if record and b==record['data']:
                cards.append(record['html']);continue
            # Reuse original wrappers/spacing, replacing only edited fields.
            previous=record['data'] if record else {}
            card=record['html'] if record else '<article class="book">\n  <h3></h3>\n</article>'
            def replace(pattern,value,addition):
                nonlocal card
                if re.search(pattern,card,re.S):card=re.sub(pattern,lambda m:value,card,count=1,flags=re.S)
                elif value:card=card.replace('</article>',addition+'\n</article>')
            if b.get('title')!=previous.get('title'):
                card=re.sub(r'<h3>.*?</h3>',lambda m:'<h3>'+ESC(b['title'])+'</h3>',card,count=1,flags=re.S)
            if b.get('metadata','')!=previous.get('metadata',''):
                v='<div class="meta">'+rich(b.get('metadata',''))+'</div>';replace(r'<div class="meta">.*?</div>',v,v)
            if b.get('details',[])!=previous.get('details',[]):
                matches=list(re.finditer(r'<div class="(?:meta|rating|date)">.*?</div>',card,re.S))
                for m in reversed(matches[1:]):card=card[:m.start()]+card[m.end():]
                v=''.join('<div class="'+x['kind']+'">'+rich(x['content'])+'</div>' for x in b.get('details',[]) if x['kind'] in ['meta','rating','date'])
                m=re.search(r'<div class="meta">.*?</div>',card,re.S)
                if m:card=card[:m.end()]+v+card[m.end():]
            if b.get('summary','')!=previous.get('summary',''):
                v='<p class="summary">'+ESC(b['summary'])+'</p>' if b.get('summary') else '';replace(r'<p class="summary">.*?</p>',v,v)
            if b.get('notes','')!=previous.get('notes',''):
                v='<section class="my-notes">'+rich(b['notes'])+'</section>' if b.get('notes') else '';replace(r'<section class="my-notes">.*?</section>',v,v)
            if b.get('links',[])!=previous.get('links',[]):
                card=re.sub(r'<div class="link">.*?</div>','',card,flags=re.S)
                for link in b.get('links',[]):
                    if not re.match(r'^https://',link['url']):raise ValueError('Links must use HTTPS')
                    card=card.replace('</article>','<div class="link"><a href="'+html.escape(link['url'],quote=True)+'">'+ESC(link['label'])+'</a></div>\n</article>')
            cards.append(card)
        out=out.replace('{{section:'+sec['id']+'}}',''.join(cards)).replace('{{label:'+sec['id']+'}}',ESC(sec['label'])+' ('+str(len(cards))+')')
    out=out.replace('<title>'+ESC(old['title'])+'</title>','<title>'+ESC(data['title'])+'</title>').replace('<h1>'+ESC(old['title'])+'</h1>','<h1>'+ESC(data['title'])+'</h1>')
    out=out.replace('Last updated: '+old['updated'],'Last updated: '+ESC(data['updated']))
    if data['introduction']!=old['introduction']:out=out.replace(old['introduction'],rich(data['introduction']),1)
    if data['statistics']!=old['statistics']:
        a=''.join('<div class="stat"><div class="stat-value">'+ESC(x['value'])+'</div><div class="stat-label">'+ESC(x['label'])+'</div></div>' for x in data['statistics'])
        out=re.sub(r'  <div class="stats">.*?\n  </div>',lambda m:'  <div class="stats">'+a+'\n  </div>',out,count=1,flags=re.S)
    if '{{section:' in out:raise ValueError('Unrendered section')
    return out
if __name__=='__main__':
    source=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'books.json'
    target=Path(sys.argv[2]) if len(sys.argv)>2 else ROOT/'dist/books.html'
    target.parent.mkdir(parents=True,exist_ok=True);target.write_text(render(json.loads(source.read_text())))
    print('Rendered',target)
