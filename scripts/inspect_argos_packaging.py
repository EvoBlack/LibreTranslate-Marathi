import inspect
from argostranslate.package import packaging
print([name for name in dir(packaging) if not name.startswith('_')])
if hasattr(packaging, 'create_package'):
    print('\ncreate_package source:\n')
    print(inspect.getsource(packaging.create_package))
else:
    print('\nno create_package')
