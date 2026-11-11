#!/usr/bin/env python3
"""Run after every edit to index.html: refreshes the script hash inside the Content-Security-Policy meta tag."""
import re, hashlib, base64, pathlib
p = pathlib.Path(__file__).with_name('index.html'); s = p.read_text()
body = re.search(r'<script>(.*?)</script>', s, re.S).group(1)
h = base64.b64encode(hashlib.sha256(body.encode()).digest()).decode()
csp = ("default-src 'self'; script-src 'sha256-%s'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
       "font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src https://formsubmit.co; "
       "form-action 'self'; base-uri 'self'; object-src 'none'; upgrade-insecure-requests" % h)
tag = '<meta http-equiv="Content-Security-Policy" content="%s" />' % csp
if 'http-equiv="Content-Security-Policy"' in s: s = re.sub(r'<meta http-equiv="Content-Security-Policy"[^>]*/>', tag, s)
else: s = s.replace('<meta charset="utf-8" />', '<meta charset="utf-8" />\n' + tag + '\n<meta name="referrer" content="strict-origin-when-cross-origin" />', 1)
p.write_text(s); print('CSP updated', h)
