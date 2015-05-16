# -*- coding: utf-8 -*-
import logbook
from logbook import Logger
from logbook import RotatingFileHandler
from logbook import TimedRotatingFileHandler


class MyLog:

    def __init__(self, filename=r'log\error.log'):
        # 设置本地时间
        logbook.set_datetime_format("local")
        self.filename = filename
        self.format_string = '[{record.time:%Y-%m-%d %H:%M:%S}] {record.level_name}: {record.channel}: {record.message}'

    def rotating(self):
        log_handler = RotatingFileHandler(
            filename=self.filename, mode='a', encoding='utf-8', level=0,
            format_string=self.format_string, max_size=10 * 1024 * 1024,
            backup_count=5, filter=None, bubble=False, delay=False)
        log_handler.push_application()

    def timed_rotating(self):
        log_handler = TimedRotatingFileHandler(
            filename=self.filename, mode='a', encoding='utf-8', level=0,
            format_string=self.format_string, date_format='%Y-%m-%d',
            backup_count=30, filter=None, bubble=False)
        log_handler.push_application()


if __name__ == "__main__":
    my_log = MyLog('log\package.log')

    my_log.rotating()
    log = Logger('My Logger')
    log.error('This is a warning')
