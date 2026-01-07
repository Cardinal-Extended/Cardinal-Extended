
import sys
import os


from cardinal import Cardinal


from configs import logger_config_path

from Utils import PLUGIN_DIR, LOGS_DIR
import Utils.cardinal_tools


import tomllib
import logging.config
import colorama
import time


with open('logo.txt') as fp: logo = fp.read()


VERSION = '0.1.0.0'
CARDINAL_VERSION = '0.1.16.9'


Utils.cardinal_tools.set_console_title(f'Cardinal Extended v{VERSION}')


if getattr(sys, 'frozen', False): os.chdir(os.path.dirname(sys.executable))

else: os.chdir(os.path.dirname(__file__))


folders = [PLUGIN_DIR, LOGS_DIR]
for folder in folders:
    if not folder.exists(): os.makedirs(folder)


colorama.init()

with open(logger_config_path, 'rb') as fp: logger_config = tomllib.load(fp)
logging.config.dictConfig(logger_config)
logging.raiseExceptions = False
log = logging.getLogger('main')


log.debug('------------------------------------------------------------------')


print(f'{colorama.Style.RESET_ALL}{logo}')
print(f'{colorama.Fore.RED}{colorama.Style.BRIGHT}v{CARDINAL_VERSION}{colorama.Style.RESET_ALL}\n')
print(f'{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT}By {colorama.Fore.BLUE}{colorama.Style.BRIGHT}@shiro_okamoto{colorama.Style.RESET_ALL}')
print(f'{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT}Credits to {colorama.Fore.BLUE}{colorama.Style.BRIGHT}@sidor0912 (github.com/sidor0912/FunPayCardinal){colorama.Style.RESET_ALL}\n')
print(f'{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT} * GitHub: {colorama.Fore.BLUE}{colorama.Style.BRIGHT}https://github.com/Shiro-Okamoto/CardinalExtended{colorama.Style.RESET_ALL}')
print(f'{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT} * Telegram: {colorama.Fore.BLUE}{colorama.Style.BRIGHT}t.me/shiro_okamoto')


if sys.platform == 'linux' and os.getenv('FPC_IS_RUNNIG_AS_SERVICE', '0') == '1':
    import getpass

    pid = str(os.getpid())
    pidFile = open(f'/run/CardinalExtended/{getpass.getuser()}/CardinalExtended.pid', 'w')
    pidFile.write(pid)
    pidFile.close()

    log.info(f'''$GREENPID file is created, process's PID: {pid}''')


try: Cardinal('Cardinal', CARDINAL_VERSION).init().start()

except KeyboardInterrupt:
    log.info('Exiting program...')

    sys.exit()

except:
    log.critical('An unhandled error occurred when Cardinal was running.')
    log.warning('TRACEBACK', exc_info=True)


    log.critical('Exiting program...')

    time.sleep(5)
    sys.exit()
