from calendar import leapdays
import auto_derby
from auto_derby import single_mode
from auto_derby import scenes
from __future__ import annotations

import time


class PaddockScene (scenes.PaddockScene):
    def choose_runing_style(self, style: LEAD):
        time.sleep(0.5)


auto_derby.plugin.register(__name__, Plugin())
