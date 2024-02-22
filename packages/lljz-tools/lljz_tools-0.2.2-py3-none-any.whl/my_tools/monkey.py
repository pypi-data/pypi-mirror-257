# coding=utf-8
import logging
import re
import sys

from my_tools.log_manager import LogManager

_print_logger = LogManager(
    'print',
    level=logging.DEBUG,
    console_colors={"INFO": "cyan"},
    formatter='%(asctime)s.%(msecs)03d - %(name)s - %(message)s',
    log_file='/pythonlog/print.log', error_log_file=''
).get_logger()

print_raw = print


def my_print(*args, sep=' ', end='\n', file=None, flush=False):
    fra = sys._getframe(1)
    line = fra.f_lineno
    file_name = fra.f_code.co_filename
    args = (f'"{file_name}:{line}" - {fra.f_code.co_name} :', *args)
    if file in [sys.stdout, None]:
        _print_logger.info(sep.join(map(str, args)))
    else:
        _print_logger.error(sep.join(map(str, args)))


def patch_print():

    try:
        __builtins__.print = my_print
        from traceback import TracebackException

        def t_print(self, *, file=None, chain=True):
            """Print the result of self.format(chain=chain) to 'file'."""
            if file is None:
                file = sys.stderr
            for line in self.format(chain=chain):
                print_raw(line, file=file, end="")

        TracebackException.print = t_print
    except AttributeError:
        __builtins__['print'] = my_print


def restore_print():
    try:
        __builtins__.print = print_raw
    except AttributeError:
        __builtins__['print'] = print_raw


if __name__ == '__main__':
    from my_tools.decorators import catch_exception, auto_retry

    patch_print()


    @catch_exception(3)
    def func():
        print('hello world')
        raise ValueError("123")


    def to():
        func()


    to()
    print('END')
