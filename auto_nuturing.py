# -*- coding=UTF-8 -*-
# pyright: strict

from __future__ import annotations

from . import action, templates
import time

def auto_pick_up(n: int) -> None:
    action.wait_tap_image(templates.NUTURING)
    action.wait_image(templates.RETURN_BUTTON)
    time.sleep(0.5)
    action.tap_image(templates.GREEN_NEXT_BUTTON)
    action.wait_tap_image(templates.RACE_CONFIRM_BUTTON)
    time.sleep(0.2)
    action.tap_image(templates.GREEN_NEXT_BUTTON)

    item_count = 0
    for _ in action.match_image_until_disappear(
        templates.GREEN_CROSS, sort=lambda x: sorted(x, key=lambda i: i[1][1])
    ):
        action.tap_image(templates.GREEN_CROSS)
        item_count += 1
        if n > 0 and item_count >= n:
            break
        action.wait_tap_image(templates.BROWNIE)
        action.wait_tap_image(templates.DECIDED)
        time.sleep(0.2)


    action.wait_tap_image(templates.GREEN_NEXT_BUTTON)
    action.wait_tap_image(templates.GREEN_CROSS)
    time.sleep(0.2)
    action.wait_tap_image(templates.FUKUKITA)
    time.sleep(0.2)
    action.wait_tap_image(templates.START_NUTURING)
    time.sleep(0.2)
    tmpl,pos = action.wait_image(
        templates.RECOVER,
        templates.START_NUTURING
        )
    name = tmpl.name
    if name == templates.RECOVER:
        action.tap(pos)
        action.wait_tap_image(templates.TP30_USAGE)
        action.wait_tap_image(templates.OK)
        action.wait_tap_image(templates.CLOSE2)
    action.wait_tap_image(templates.START_NUTURING)
    action.wait_tap_image(templates.SKIP_BUTTON)
    action.wait_tap_image(templates.DECIDED)
    action.wait_tap_image_twice(templates.SKIP_OFF)
    pass