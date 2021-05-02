from tg_bot.modules.disable import DisableAbleCommandHandler, DisableAbleMessageHandler
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler
from telegram.ext.filters import BaseFilter
from tg_bot import dispatcher as d, log
from typing import Optional, Union



class KigyoTelegramHandler:
    def __init__(self, d):
        self._dispatcher = d

    def command(
        self, command: str, filters: Optional[BaseFilter] = None, admin_ok: bool = False, pass_args: bool = False, run_async: bool = True, can_disable: bool = True, group: Optional[Union[int]] = None
    ):


        def _command(func):
            try:
                if can_disable:
                    self._dispatcher.add_handler(
                        DisableAbleCommandHandler(command, func, filters=filters, run_async=run_async, pass_args=pass_args, admin_ok=admin_ok), group
                    )
                else:
                    self._dispatcher.add_handler(
                        CommandHandler(command, func, filters=filters, run_async=run_async, pass_args=pass_args), group
                    )
                log.info(f"[KIGCMD] Loaded handler {command} for function {func.__name__} in group {group}")
            except TypeError:
                if can_disable:
                    self._dispatcher.add_handler(
                        DisableAbleCommandHandler(command, func, filters=filters, run_async=run_async, pass_args=pass_args, admin_ok=admin_ok)
                    )
                else:
                    self._dispatcher.add_handler(
                        CommandHandler(command, func, filters=filters, run_async=run_async, pass_args=pass_args)
                    )
                log.info(f"[KIGCMD] Loaded handler {command} for function {func.__name__}")
            
            return func

        return _command

    def message(self, pattern: Optional[str] = None, can_disable: bool = True, run_async: bool = True, group: Optional[Union[int]] = None, friendly = None):
        def _message(func):
            try:
                if can_disable:
                    self._dispatcher.add_handler(
                        DisableAbleMessageHandler(pattern, func, friendly=friendly, run_async=run_async), group
                    )
                else:
                    self._dispatcher.add_handler(
                        MessageHandler(pattern, func, run_async=run_async), group
                    )
                log.info(f"[KIGMSG] Loaded filter pattern {pattern} for function {func.__name__} in group {group}")
            except TypeError:
                if can_disable:
                    self._dispatcher.add_handler(
                        DisableAbleMessageHandler(pattern, func, friendly=friendly, run_async=run_async)
                    )
                else:
                    self._dispatcher.add_handler(
                        MessageHandler(pattern, func, run_async=run_async)
                    )
                log.info(f"[KIGMSG] Loaded filter pattern {pattern} for function {func.__name__}")
            
            return func
        return _message

    def callbackquery(self, pattern: str = None, run_async: bool = True):
        def _callbackquery(func):
            self._dispatcher.add_handler(CallbackQueryHandler(pattern=pattern, callback=func, run_async=run_async))
            log.info(f'[KIGCALLBACK] Loaded callbackquery handler with pattern {pattern} for function {func.__name__}')
            return func
        return _callbackquery

kigcmd = KigyoTelegramHandler(d).command
kigmsg = KigyoTelegramHandler(d).message
kigcallback = KigyoTelegramHandler(d).callbackquery