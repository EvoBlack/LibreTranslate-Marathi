import inspect
import argostranslate.package as pkg

print('module:', pkg)
print('has install_from_path:', hasattr(pkg, 'install_from_path'))
if hasattr(pkg, 'install_from_path'):
    print('source:')
    print(inspect.getsource(pkg.install_from_path))
else:
    print('no install_from_path')
