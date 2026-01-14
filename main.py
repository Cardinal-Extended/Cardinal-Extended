
import sys
import os


from cardinal_manager import CardinalManager


from configs import VERSION_PATH, PLUGINS_DIR, LOGS_DIR, STORAGE_DIR, CACHE_DIR, UPDATE_DIR, Config

from Utils import set_console_title


import logging.config
import colorama
import time


VERSION = VERSION_PATH.read_text('utf-8')


set_console_title(f'Cardinal Extended {VERSION}')


if getattr(sys, 'frozen', False): os.chdir(os.path.dirname(sys.executable))

else: os.chdir(os.path.dirname(__file__))


folders = [PLUGINS_DIR, LOGS_DIR, STORAGE_DIR, CACHE_DIR, UPDATE_DIR]

for folder in folders:
    if not folder.exists(): folder.mkdir(parents=True, exist_ok=True)


colorama.init()


logger_config: dict = Config().LOGGER.to_dict()

logging.config.dictConfig(logger_config)

logging.raiseExceptions = False


log = logging.getLogger('main')


log.debug('------------------------------------------------------------------')


with open('logo.txt') as fp: logo = fp.read()


greetings = (
    f'{colorama.Style.RESET_ALL}{logo}\n'

    f'{colorama.Fore.RED}{colorama.Style.BRIGHT}{VERSION}{colorama.Style.RESET_ALL}\n\n'


    f'{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT}By {colorama.Style.RESET_ALL}'
    f'{colorama.Fore.BLUE}{colorama.Style.BRIGHT}@shiro_okamoto{colorama.Style.RESET_ALL}\n'

    f'{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT}Credits to {colorama.Style.RESET_ALL}'
    f'{colorama.Fore.BLUE}{colorama.Style.BRIGHT}@sidor0912 (github.com/sidor0912/FunPayCardinal){colorama.Style.RESET_ALL}\n\n'


    f'{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT} * GitHub: {colorama.Style.RESET_ALL}'
    f'{colorama.Fore.BLUE}{colorama.Style.BRIGHT}https://github.com/Shiro-Okamoto/CardinalExtended{colorama.Style.RESET_ALL}\n'

    f'{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT} * Telegram: {colorama.Style.RESET_ALL}'
    f'{colorama.Fore.BLUE}{colorama.Style.BRIGHT}t.me/shiro_okamoto{colorama.Style.RESET_ALL}'
)

print(greetings)


if sys.platform == 'linux' and os.getenv('FPC_IS_RUNNIG_AS_SERVICE', '0') == '1':
    import getpass

    pid = str(os.getpid())
    pidFile = open(f'/run/CardinalExtended/{getpass.getuser()}/CardinalExtended.pid', 'w')
    pidFile.write(pid)
    pidFile.close()

    log.info(f'''$GREENPID file is created, process's PID: {pid}''')


try:
    log.info('Starting program...')

    manager = CardinalManager()

    manager.start_cardinal('CARDINAL', VERSION)

    manager.loop()

except KeyboardInterrupt:
    log.info('Exiting program...')

    sys.exit()

except:
    log.critical('An unhandled error occurred when Cardinal was running.')
    log.warning('TRACEBACK', exc_info=True)


    log.critical('Exiting program...')

    time.sleep(5)
    sys.exit()
