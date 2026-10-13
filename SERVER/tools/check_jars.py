import zipfile, os, sys
mods_dir = os.path.join(os.getcwd(), 'mods')
if not os.path.isdir(mods_dir):
    print('NO_MODS_DIR')
    sys.exit(0)

found = False
for f in sorted(os.listdir(mods_dir)):
    if f.lower().endswith('.jar'):
        p = os.path.join(mods_dir, f)
        try:
            with zipfile.ZipFile(p, 'r') as z:
                bad = z.testzip()
                if bad:
                    print('BAD:', f, 'testzip failed at', bad)
                    found = True
                else:
                    print('OK:', f)
        except Exception as e:
            print('BAD:', f, '-', repr(e))
            found = True

if not found:
    print('All jars appear OK')
