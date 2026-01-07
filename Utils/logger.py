'''В данном модуле написаны форматтеры для логгера.'''
import os


from logging import Formatter, LogRecord, PercentStyle
from pathlib import Path
from colorama import Fore, Back, Style
import re


CLEAR_RE = re.compile(r'(\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~]))|(\n)|(\r)')


logs_path = Path(__file__).parent.parent / 'logs'
if not logs_path.exists():
    os.makedirs(logs_path)


class ColoredFormatter(Formatter):
    def __init__(self):
        super(ColoredFormatter, self).__init__(datefmt='%Y-%m-%d %H:%M:%S')
        self.log_level_colors = {'DEBUG': '\033[94m', 'INFO': '\033[92m', 'WARNING': '\033[93m', 'ERROR': '\033[91m', 'CRITICAL': '\033[95m'}
        self.colors = {
            "$YELLOW": Fore.YELLOW,
            "$CYAN": Fore.CYAN,
            "$MAGENTA": Fore.MAGENTA,
            "$BLUE": Fore.BLUE,
            "$GREEN": Fore.GREEN,
            "$BLACK": Fore.BLACK,
            "$WHITE": Fore.WHITE,
            "$B_YELLOW": Back.YELLOW,
            "$B_CYAN": Back.CYAN,
            "$B_MAGENTA": Back.MAGENTA,
            "$B_BLUE": Back.BLUE,
            "$B_GREEN": Back.GREEN,
            "$B_BLACK": Back.BLACK,
            "$B_WHITE": Back.WHITE
        }


    def format(self, record):
        msg = record.getMessage()

        for c in self.colors:
            if c in msg: msg = msg.replace(c, self.colors[c])
        msg = msg.replace('$RESET', self.log_level_colors[record.levelname])

        record.msg = msg


        fmt = f'{self.log_level_colors.get(record.levelname, '')}%(name)s: [%(levelname)s: %(asctime)s] %(message)s'

        self._style = PercentStyle(fmt)
        self._style.validate()

        return super().format(record)


class FileFormatter(Formatter):
    def __init__(self):
        super().__init__(
            fmt='%(name)s: [%(levelname)s: %(asctime)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )


    def format(self, record: LogRecord):
        msg = record.getMessage()

        msg = CLEAR_RE.sub('', msg)

        record.msg = msg

        return super().format(record)