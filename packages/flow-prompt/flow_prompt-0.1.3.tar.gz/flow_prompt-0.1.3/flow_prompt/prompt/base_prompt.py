import logging
import typing as t
from collections import defaultdict
from dataclasses import dataclass, field

from flow_prompt.prompt.chat import ChatsEntity

logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class BasePrompt:
    priorities: t.Dict[int, t.List[ChatsEntity]] = field(
        default_factory=lambda: defaultdict(list)
    )
    chats: t.List[ChatsEntity] = field(default_factory=list)
    pipe: t.List[str] = field(default_factory=list)
    functions: t.List[dict] = None

    def add(
        self,
        content: str = "",
        role: str = "user",
        name: t.Optional[str] = None,
        tool_calls: t.Dict[str, str] = None,
        priority: int = 0,
        required: bool = False,
        is_multiple: bool = False,
        while_fits: bool = False,
        add_in_reverse_order: bool = False,
        in_one_message: bool = False,
        continue_if_doesnt_fit: bool = False,
        add_if_fitted_labels: t.List[str] = None,
        label: t.Optional[str] = None,
        presentation: t.Optional[str] = None,
        last_words: t.Optional[str] = None,
    ):
        if not isinstance(content, str):
            logger.warning(f"content is not string: {content}, assignig str of it")
            content = str(content)

        chat_value = ChatsEntity(
            role=role,
            content=(content or ""),
            name=name,
            tool_calls=tool_calls,
            priority=priority,
            required=required,
            is_multiple=is_multiple,
            while_fits=while_fits,
            add_in_reverse_order=add_in_reverse_order,
            in_one_message=in_one_message,
            continue_if_doesnt_fit=continue_if_doesnt_fit,
            add_if_fitted_labels=add_if_fitted_labels,
            label=label,
            presentation=presentation,
            last_words=last_words,
        )
        self.chats.append(chat_value)
        self.priorities[priority].append(chat_value)
        self.pipe.append(chat_value._uuid)

    def add_function(self, function: dict):
        if not self.functions:
            self.functions = []
        self.functions.append(function)
