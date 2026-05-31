import re
from pathlib import Path

text = Path('static/js/i18n/translations.js').read_text(encoding='utf-8')

def extract_keys(lang):
    m = re.search(rf'{lang}:\s*\{{', text)
    if not m:
        return set()
    start = m.end()
    depth = 1
    i = start
    while i < len(text) and depth:
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
        i += 1
    chunk = text[start : i - 1]
    return set(re.findall(r'"((?:[^"\\]|\\.)*)"', chunk)[0::2] if False else re.findall(r'"([^"]+)":', chunk))

en = extract_keys('en')
kn = extract_keys('kn')
hi = extract_keys('hi')
print('en', len(en), 'kn', len(kn), 'hi', len(hi))
print('missing kn', len(en - kn))
print('missing hi', len(en - hi))
if en - kn:
    print('kn sample:', list(sorted(en - kn))[:20])
if en - hi:
    print('hi sample:', list(sorted(en - hi))[:20])
