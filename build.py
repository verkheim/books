from pathlib import Path
import json
from render import render, ROOT
out=ROOT/'dist'
out.mkdir(exist_ok=True)
(out/'books.html').write_text(render(json.loads((ROOT/'books.json').read_text())))
(out/'_headers').write_bytes((ROOT/'books-headers.txt').read_bytes())
print('Built Books only')
