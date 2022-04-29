# -*- coding=UTF-8 -*-
# pyright: strict

from __future__ import annotations

from . import action, templates
import time

def learn_first_n(n: int) -> None:
    rp = action.resize_proxy()
    action.wait_tap_image(templates.SKILL)
    action.wait_image(templates.RETURN_BUTTON)
    time.sleep (2)
    item_count = 0
    for _, pos in action.match_image_until_disappear(
        templates.PLUS, sort=lambda x: sorted(x, key=lambda i: i[1][1])
    ):
        action.tap_image(templates.PLUS)
        item_count += 1
        if n > 0 and item_count >= n:
            break
        action.swipe(
            rp.vector2((17, 540), 540),
            dy=rp.vector(-120, 540),
            duration=0.2
        )
        time.sleep(0.2)
        action.swipe(
            rp.vector2((17, 540), 540),
            dy=rp.vector(-40, 540),
            duration=0.2
        )
        action.tap(pos)
        time.sleep(0.3)


    action.wait_tap_image(templates.LEGEND_RACE_CONFIRM_BUTTON)
    action.wait_tap_image(templates.GET_SKILL)
    action.wait_tap_image(templates.CLOSE_BUTTON)
    action.wait_tap_image(templates.RETURN_BUTTON)
    time.sleep(0.5)
    action.wait_tap_image(templates.SINGLE_MODE_FINISH_BUTTON)
    action.wait_tap_image(templates.FINISH)
    action.wait_image_stable(templates.GREEN_NEXT_BUTTON)
    action.wait_tap_image_as_fucked_monster(templates.GREEN_NEXT_BUTTON)
    pass