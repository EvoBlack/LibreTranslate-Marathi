import sys
import traceback
from importlib import import_module

def run_subcommand(cmd_name):
    try:
        mod = import_module(f'onmt.bin.{cmd_name}')
        if hasattr(mod, 'main'):
            mod.main()
        else:
            print(f'{cmd_name} module has no main()')
    except Exception:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python onmt_run_wrapper.py <subcommand> [args...]')
        sys.exit(1)
    # The onmt modules parse sys.argv directly, so leave argv as-is.
    cmd = sys.argv[1]
    # Shift argv so the imported module sees the same args it would from CLI
    sys.argv = sys.argv[1:]
    run_subcommand(cmd)
