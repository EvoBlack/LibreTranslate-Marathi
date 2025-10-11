from libretranslate.hf_adapter import get_translator
print('Loading translator...')
tr = get_translator('en','mr')
print('Translator:', tr)
if tr:
    hyps = tr.hypotheses('Hello world', 1)
    print('Hypotheses:', hyps)
    if hyps:
        print('Translated:', hyps[0].value)
else:
    print('No translator available')
