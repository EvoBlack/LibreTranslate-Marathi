import inspect
import argostranslate
import argostranslate.package

print('argostranslate version:', getattr(argostranslate, '__version__', 'unknown'))
print('package module functions:')
print([name for name in dir(argostranslate.package) if not name.startswith('_')])

if hasattr(argostranslate.package, 'create_package'):
    print('\nSource of argostranslate.package.create_package:')
    print(inspect.getsource(argostranslate.package.create_package))
else:
    print('\ncreate_package not found')
