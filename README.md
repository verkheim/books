# Books

Edit one document at https://app.pagescms.org/verkheim/books/main/file/books.
Save publishes automatically to https://dsnyder.cloud/books through Cloudflare.

`books.md` is the only content source. Write ordinary paragraphs, headings and
links; there are no per-book fields. The editor offers rich text and Markdown
source views. Dropbox is a separate copy, not an automatic sync.

Build: `npm ci` then `python3 build.py` (Python 3 and Node.js).
`build.mjs` renders Markdown to `dist/books.html`. `wrangler.jsonc` deploys it to
the isolated `dsnyder-books` Worker. Other website pages stay in the private
main Worker. Older JSON and renderer files are obsolete and not read by this build.
