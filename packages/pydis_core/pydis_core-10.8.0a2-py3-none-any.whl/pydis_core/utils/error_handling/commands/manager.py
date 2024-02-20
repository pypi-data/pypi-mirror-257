from collections.abc import Callable
from typing import NoReturn

from discord import Interaction
from discord.ext.commands import Context

from pydis_core.utils.error_handling.commands import AbstractCommandErrorHandler
from pydis_core.utils.logging import get_logger

log = get_logger(__name__)


class CommandErrorManager:
    """A class that registers error handlers and handles all command related errors."""

    def __init__(self, default: AbstractCommandErrorHandler, handlers: list[AbstractCommandErrorHandler] | None = None):
        self.handlers = handlers or []
        self.registered_handlers = set(type(handler).__name__ for handler in self.handlers)
        self.default = default

    async def handle_error(
        self,
        error: Exception,
        context_or_interaction: Context | Interaction
    ) -> None:
        """
        Handle a discord exception.

        This works simply by iterating over the available handlers, and chooses the one capable of handling the error.

        Instead of having some priority system to distinguish the execution order of handlers, we will
        let the `should_handle_error` do the job.

        The default needs to always be last, since the container can either be initialized with the handlers, or
        we can add handlers using the `register_handler` function that we don't know when it will be invoked, if ever.
        """
        for handler in self.handlers + [self.default]:
            if await handler.should_handle_error(error):
                callback = self._determine_callback(handler, context_or_interaction)
                await callback(context_or_interaction, error)
                break

    def register_handler(self, handler: AbstractCommandErrorHandler) -> None:
        """Register a command error handler."""
        handler_name = type(handler).__name__
        if handler_name in self.registered_handlers:
            log.info(f"Skipping registration of command error handler '{handler_name}' as it's already registered.")
            return

        self.handlers.append(handler)
        self.registered_handlers.add(type(handler).__name__)

    @staticmethod
    def _determine_callback(
        handler: AbstractCommandErrorHandler,
        context_or_interaction: Context | Interaction
    ) -> Callable[[Context, Exception], NoReturn] | Callable[[Interaction, Exception], NoReturn] | None:
        """Determines the handling callback that will be used."""
        if isinstance(context_or_interaction, Context):
            return handler.handle_text_command_error
        return handler.handle_app_command_error
