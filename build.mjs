import fs from 'node:fs';
import MarkdownIt from 'markdown-it';
const source = fs.readFileSync(new URL('books.md', import.meta.url), 'utf8').replace(/^---\r?\n(?:[\s\S]*?\r?\n)?---\r?\n/, '');
const md = new MarkdownIt({html:false, breaks:true, linkify:false});
const body = md.render(source);
const page = `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>My Reading List</title><style>
body{max-width:850px;margin:0 auto;padding:40px 24px;font:18px/1.65 system-ui,sans-serif;color:#272522;background:#faf9f6}h1,h2,h3{line-height:1.25}h2{margin-top:2.5em;border-bottom:1px solid #d7d2c9;padding-bottom:.3em}h3{margin-top:2em}a{color:#23579a;overflow-wrap:anywhere}blockquote{border-left:3px solid #d7d2c9;margin-left:0;padding-left:1em;color:#595650}img{max-width:100%}pre{white-space:pre-wrap}hr{border:0;border-top:1px solid #d7d2c9}
</style></head><body><main>${body}</main></body></html>\n`;
fs.mkdirSync('dist',{recursive:true});
fs.writeFileSync('dist/books.html',page);
fs.copyFileSync('books-headers.txt','dist/_headers');
console.log('Built single Markdown Books document');
