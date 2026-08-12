"""Tests for connecting deck buttons to action execution."""

from unittest.mock import Mock

from pytestqt.qtbot import QtBot

from quickdeck.models import ActionDefinition, ActionType, DeckButton
from quickdeck.widgets import DeckButtonWidget


def test_click_executes_all_actions(qtbot: QtBot) -> None:
    actions = [
        ActionDefinition("first", ActionType.OPEN_APPLICATION, "first.exe"),
        ActionDefinition("second", ActionType.OPEN_WEBSITE, "https://example.com"),
    ]
    action_service = Mock()
    action_service.execute.return_value = None
    widget = DeckButtonWidget(
        DeckButton(id="test", name="Test", actions=actions),
        action_service,
    )
    qtbot.addWidget(widget)

    widget.click()

    assert action_service.execute.call_args_list == [
        ((actions[0],),),
        ((actions[1],),),
    ]
