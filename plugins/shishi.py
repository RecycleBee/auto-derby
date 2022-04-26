from __future__ import annotations

import time

import auto_derby
from auto_derby import single_mode
from auto_derby import action
from auto_derby import templates
from auto_derby.constants import RuningStyle
from auto_derby.single_mode.context import Context

def default_ignore_training_commands(ctx: Context) -> bool:
    if any(i for i in single_mode.race.find(ctx) if i.score(ctx) > 50):
        return True
    if ctx.vitality < 0.2:
        return True
    return False

class Plugin(auto_derby.Plugin):
    def install(self) -> None:
        auto_derby.config.single_mode_ignore_training_commands = default_ignore_training_commands

auto_derby.plugin.register(__name__, Plugin())