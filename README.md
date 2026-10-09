# Books

Public content and renderer for the Books page at https://dsnyder.cloud/books.
Edit Books in https://app.pagescms.org/verkheim/books/main.

Build: `python3 build.py`. Cloudflare Workers Builds deploys main to the
isolated dsnyder-books Worker. The private main website forwards only its
Books URLs to this Worker. No other website source or credentials belong here.

render-baseline.json preserves the exact existing page markup for lossless
rendering; books.json is the editable content. Section counts are generated.
Summary statistics and last-updated text are editable fields.
