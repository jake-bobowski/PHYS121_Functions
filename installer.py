def Check():
    import importlib.util
    import sys
    import subprocess
    cnt = 0
    # For illustrative purposes.
    package_names = ['ipysheet', 'uncertainties', 'httpimport']
    for name in package_names:
        spec = importlib.util.find_spec(name)
        if spec is None:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user', name])
            cnt += 1
                
    if cnt == 0:
        print('\033[1m All packages already installed. Please proceed. \033[0m')
    else:
        print('\n \033[1m Some packages were installed.  Please completely log out and then login again before proceeding. \033[0m')