from typing import final

from .abc import TelegramType
from .chat import Chat


@final
class Story(TelegramType):
    """This object represents a story.

    See: https://core.telegram.org/bots/api#story
    """

    chat: Chat
    """Chat that posted the story."""

    id: int
    """Unique identifier for the story in the chat."""
