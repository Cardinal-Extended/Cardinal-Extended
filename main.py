
import sys
import os
from pip._internal.cli.main import main


from cardinal import Cardinal


from configs import logger_config_path


import Utils.cardinal_tools
import Utils.config_loader as cfg_loader
import Utils.exceptions as excs


from first_setup import first_setup


from locales.localizer import Localizer


import tomllib
import logging.config
import colorama
import time


with open('logo.txt') as fp: logo = fp.read()


VERSION = "0.0.0.1"
CARDINAL_VERSION = "0.1.16.9"


Utils.cardinal_tools.set_console_title(f"Cardinal Extended v{VERSION}")


if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))
else:
    os.chdir(os.path.dirname(__file__))


folders = ["configs", "logs", "storage", "storage/cache", "storage/plugins", "storage/products", "plugins"]
for i in folders:
    if not os.path.exists(i):
        os.makedirs(i)


files = ["configs/auto_delivery.cfg", "configs/auto_response.cfg"]
for i in files:
    if not os.path.exists(i):
        with open(i, "w", encoding="utf-8") as f:
            ...


colorama.init()

with open(logger_config_path, 'rb') as fp: logger_config = tomllib.load(fp)
logging.config.dictConfig(logger_config)
logging.raiseExceptions = False
logger = logging.getLogger("main")
logger.debug("------------------------------------------------------------------")


print(f"{colorama.Style.RESET_ALL}{logo}")
print(f"{colorama.Fore.RED}{colorama.Style.BRIGHT}v{CARDINAL_VERSION}{colorama.Style.RESET_ALL}\n")  # locale
print(f"{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT}By {colorama.Fore.BLUE}{colorama.Style.BRIGHT}Woopertail, @sidor0912{colorama.Style.RESET_ALL}")
print(
    f"{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT} * GitHub: {colorama.Fore.BLUE}{colorama.Style.BRIGHT}github.com/sidor0912/FunPayCardinal{colorama.Style.RESET_ALL}")
print(f"{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT} * Telegram: {colorama.Fore.BLUE}{colorama.Style.BRIGHT}t.me/sidor0912")
print(f"{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT} * Новости о обновлениях: {colorama.Fore.BLUE}{colorama.Style.BRIGHT}t.me/fpc_updates")
print(f"{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT} * Плагины: {colorama.Fore.BLUE}{colorama.Style.BRIGHT}t.me/fpc_plugins")
print(f"{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT} * Донат: {colorama.Fore.BLUE}{colorama.Style.BRIGHT}t.me/sidor_donate")
print(f"{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT} * Telegram-чат: {colorama.Fore.BLUE}{colorama.Style.BRIGHT}t.me/funpay_cardinal")


if not os.path.exists("configs/_main.cfg"):
    first_setup()
    sys.exit()


if sys.platform == "linux" and os.getenv('FPC_IS_RUNNIG_AS_SERVICE', '0') == '1':
    import getpass

    pid = str(os.getpid())
    pidFile = open(f"/run/FunPayCardinal/{getpass.getuser()}/FunPayCardinal.pid", "w")
    pidFile.write(pid)
    pidFile.close()

    logger.info(f"$GREENPID файл создан, PID процесса: {pid}")  # locale


directory = 'plugins'
for filename in os.listdir(directory):
    if filename.endswith(".py"):  # Проверяем, что файл имеет расширение .py
        filepath = os.path.join(directory, filename)  # Получаем полный путь к файлу
        with open(filepath, 'r', encoding='utf-8') as file:
            data = file.read()  # Читаем содержимое файла
        # Заменяем подстроку
        if '"<i>Разработчик:</i> " + CREDITS' in data or " lot.stars " in data or " lot.seller " in data:
            data = data.replace('"<i>Разработчик:</i> " + CREDITS', '"sidor0912"') \
                .replace(" lot.stars ", " lot.seller.stars ") \
                .replace(" lot.seller ", " lot.seller.username ")
            # Сохраняем изменения обратно в файл
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(data)


try:
    logger.info("$MAGENTAЗагружаю конфиг _main.cfg...")  # locale
    MAIN_CFG = cfg_loader.load_main_config("configs/_main.cfg")
    localizer = Localizer(MAIN_CFG["Other"]["language"])
    _ = localizer.translate

    logger.info("$MAGENTAЗагружаю конфиг auto_response.cfg...")  # locale
    AR_CFG = cfg_loader.load_auto_response_config("configs/auto_response.cfg")
    RAW_AR_CFG = cfg_loader.load_raw_auto_response_config("configs/auto_response.cfg")

    logger.info("$MAGENTAЗагружаю конфиг auto_delivery.cfg...")  # locale
    AD_CFG = cfg_loader.load_auto_delivery_config("configs/auto_delivery.cfg")
except excs.ConfigParseError as e:
    logger.error(e)
    logger.error("Завершаю программу...")  # locale
    time.sleep(5)
    sys.exit()
except UnicodeDecodeError:
    logger.error("Произошла ошибка при расшифровке UTF-8. Убедитесь, что кодировка файла = UTF-8, "
                 "а формат конца строк = LF.")  # locale
    logger.error("Завершаю программу...")  # locale
    time.sleep(5)
    sys.exit()
except:
    logger.critical("Произошла непредвиденная ошибка.")  # locale
    logger.warning("TRACEBACK", exc_info=True)
    logger.error("Завершаю программу...")  # locale
    time.sleep(5)
    sys.exit()


try:
    Cardinal('Cardinal', MAIN_CFG, AD_CFG, AR_CFG, RAW_AR_CFG, CARDINAL_VERSION).init().run()
except KeyboardInterrupt:
    logger.info("Завершаю программу...")  # locale
    sys.exit()
except:
    logger.critical("При работе Кардинала произошла необработанная ошибка.")  # locale
    logger.warning("TRACEBACK", exc_info=True)
    logger.critical("Завершаю программу...")  # locale
    time.sleep(5)
    sys.exit()
