# -*- coding=UTF-8 -*-
# pyright: strict
"""tools for image processing.  """

import hashlib
import threading
from pathlib import Path
from typing import Any, Callable, Dict, Literal, Optional, Text, Tuple, Union

import cast_unknown as cast
import cv2
import cv2.img_hash
import numpy as np
from PIL.Image import Image, fromarray


def md5(b_img: np.ndarray, *, save_path: Optional[Text] = None) -> Text:
    _id = hashlib.md5(b_img.tobytes()).hexdigest()

    if save_path:
        dst = Path(save_path) / _id[0] / _id[1:3] / (_id[3:] + ".png")
        if not dst.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            fromarray(b_img).convert("1").save(dst)

    return _id


_HASH_ALGORITHM = cv2.img_hash.BlockMeanHash_create()


def image_hash(img: Image, *, save_path: Optional[Text] = None) -> Text:
    cv_img = np.asarray(img.convert("L"))
    h = _HASH_ALGORITHM.compute(cv_img).tobytes().hex()

    if save_path:
        md5_hash = hashlib.md5(img.tobytes()).hexdigest()
        dst = Path(save_path) / h[0] / h[1:3] / h[3:] / (md5_hash + ".png")
        if not dst.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            img.convert("RGB").save(dst)

    return h


def compare_hash(a: Text, b: Text) -> float:
    if a == b:
        return 1.0
    cv_a = np.array(list(bytes.fromhex(a)), np.uint8)
    cv_b = np.array(list(bytes.fromhex(b)), np.uint8)
    res = _HASH_ALGORITHM.compare(cv_a, cv_b)
    return 1 - (res / (len(a) * 2))


def _cast_float(v: Any) -> float:
    return float(v)


def cv_image(img: Image) -> np.ndarray:
    if img.mode == "RGB":
        return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    if img.mode == "L":
        return np.array(img)
    raise ValueError("cv_image: unsupported mode: %s" % img.mode)


def pil_image(img: np.ndarray) -> Image:
    if img.shape[2:] == (3,):
        return fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    return fromarray(img)


def compare_color(
    a: Union[Tuple[int, ...], int], b: Union[Tuple[int, ...], int], *, bit_size: int = 8
) -> float:
    max_value = (1 << bit_size) - 1
    t_a = tuple(cast.list_(a, (int,)))
    t_b = tuple(cast.list_(b, (int,)))
    if len(t_a) != len(t_b):
        return 0

    return max(
        1
        - _cast_float(
            np.sqrt(_cast_float(np.sum((np.array(t_a) - np.array(t_b)) ** 2, axis=0)))
        )
        / max_value,
        0,
    )


def level(
    img: np.ndarray, black: np.ndarray, white: np.ndarray, *, bit_size: int = 8
) -> np.ndarray:
    max_value = (1 << bit_size) - 1
    return np.clip((img - black) / (white - black) * max_value, 0, max_value).astype(
        img.dtype
    )


def color_key(
    img: np.ndarray, color: np.ndarray, threshold: float = 0.8, bit_size: int = 8
) -> np.ndarray:
    max_value = (1 << bit_size) - 1
    assert img.shape == color.shape, (img.shape, color.shape)

    if len(img.shape) == 2:
        img = img[..., np.newaxis]
        color = color[..., np.newaxis]

    # do this is somehow faster than
    # `numpy.linalg.norm(img.astype(int) - color.astype(int), axis=2,).clip(0, 255).astype(np.uint8)`
    diff_img = (
        np.asarray(
            np.sqrt(
                np.asarray(np.sum((img.astype(int) - color.astype(int)) ** 2, axis=2))
            )
        )
        .clip(0, 255)
        .astype(img.dtype)
    )

    ret = max_value - diff_img
    if threshold > 0:
        mask_img = (ret > (max_value * threshold)).astype(img.dtype)
        ret *= mask_img
    ret = ret.clip(0, 255)
    ret = ret.astype(img.dtype)
    return ret


def constant_color_key(
    img: np.ndarray, *colors: Tuple[int, ...], threshold: float = 0.8, bit_size: int = 8
) -> np.ndarray:
    ret = np.zeros(img.shape[:2])

    for color in colors:
        match_img = color_key(
            img, np.full_like(img, color), threshold=threshold, bit_size=bit_size
        )
        ret = np.array(np.maximum(ret, match_img))

    return ret


def sharpen(img: np.ndarray, size: int = 1, *, bit_size: int = 8) -> np.ndarray:
    return cv2.filter2D(
        img, bit_size, np.array(((-1, -1, -1), (-1, 9, -1), (-1, -1, -1))) * size
    )


def mix(a: np.ndarray, b: np.ndarray, a_mix: float) -> np.ndarray:
    total_ratio = 10000
    a_ratio = int(a_mix * total_ratio)
    b_ratio = total_ratio - a_ratio
    return ((a.astype(int) * a_ratio + b.astype(int) * b_ratio) / total_ratio).astype(
        a.dtype
    )


def bg_mask_by_outline(outline_img: np.ndarray) -> np.ndarray:
    h, w = outline_img.shape[:2]

    border_points = (
        *((0, i) for i in range(h)),
        *((i, 0) for i in range(w)),
        *((w - 1, i) for i in range(h)),
        *((i, h - 1) for i in range(w)),
    )

    fill_mask_img = cv2.copyMakeBorder(outline_img, 1, 1, 1, 1, cv2.BORDER_CONSTANT)
    bg_mask_img = np.zeros_like(outline_img)
    for i in border_points:
        x, y = i
        if outline_img[y, x] != 0:
            continue
        cv2.floodFill(bg_mask_img, fill_mask_img, (x, y), (255,), 0, 0)

    return bg_mask_img


def resize_by_heihgt(img: Image, height: int) -> Image:
    w, h = img.width, img.height
    w = round(height / h * w)
    h = height
    return img.resize((w, h))


def fill_area(img: np.ndarray, color: Tuple[int, ...], *, size_lt: int):
    contours, _ = cv2.findContours(
        (img * 255).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )
    for i in contours:
        size = cv2.contourArea(i)
        if size < size_lt:
            cv2.drawContours(img, [i], -1, color, cv2.FILLED)


_WINDOW_ID: Dict[Literal["value"], int] = {"value": 0}


def show(img: Image, title: Text = "") -> Callable[[], None]:

    stop_event = threading.Event()
    stop_event.is_set()
    _WINDOW_ID["value"] += 1
    title = f"{title} - {_WINDOW_ID['value']}"

    def _run():
        cv_img = np.asarray(img)
        try:
            cv2.imshow(title, cv_img)
            while not stop_event.is_set() and cv2.getWindowProperty(title, 0) >= 0:
                if cv2.pollKey() == "q":
                    break
        finally:
            cv2.destroyWindow(title)

    t = threading.Thread(target=_run, daemon=True)
    t.start()

    def _close():
        stop_event.set()
        t.join()

    return _close
