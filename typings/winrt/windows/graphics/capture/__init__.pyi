# -*- coding=UTF-8 -*-
# This typing file was generated by typing_from_help.py
"""
winrt.windows.graphics.capture - # WARNING: Please don't edit this file. It was generated by Python/WinRT v0.9.210202.1
"""

import typing



import _winrt

class Direct3D11CaptureFrame(_winrt._winrt_base):
    """
    base class for wrapped WinRT object instances.
    """

    content_size: ...
    """
    """

    surface: ...
    """
    """

    @staticmethod
    def __new__(*args, **kwargs):
        """
        Create and return a new object.  See help(type) for accurate signature.
        """
        ...

    def __enter__(self, *args, **kwargs):
        """
        """
        ...

    def __exit__(self, *args, **kwargs):
        """
        """
        ...

    def close(self, *args, **kwargs):
        """
        """
        ...

    ...

class Direct3D11CaptureFramePool(_winrt._winrt_base):
    """
    base class for wrapped WinRT object instances.
    """

    @staticmethod
    def __new__(*args, **kwargs):
        """
        Create and return a new object.  See help(type) for accurate signature.
        """
        ...

    @staticmethod
    def create(*args, **kwargs):
        """
        """
        ...

    @staticmethod
    def create_free_threaded(*args, **kwargs):
        """
        """
        ...

    def __enter__(self, *args, **kwargs):
        """
        """
        ...

    def __exit__(self, *args, **kwargs):
        """
        """
        ...

    def add_frame_arrived(self, *args, **kwargs):
        """
        """
        ...

    def close(self, *args, **kwargs):
        """
        """
        ...

    def create_capture_session(self, *args, **kwargs):
        """
        """
        ...

    def recreate(self, *args, **kwargs):
        """
        """
        ...

    def remove_frame_arrived(self, *args, **kwargs):
        """
        """
        ...

    def try_get_next_frame(self, *args, **kwargs):
        """
        """
        ...

    ...

class GraphicsCaptureItem(_winrt._winrt_base):
    """
    base class for wrapped WinRT object instances.
    """

    display_name: ...
    """
    """

    @staticmethod
    def __new__(*args, **kwargs):
        """
        Create and return a new object.  See help(type) for accurate signature.
        """
        ...

    @staticmethod
    def create_from_visual(*args, **kwargs):
        """
        """
        ...

    def add_closed(self, *args, **kwargs):
        """
        """
        ...

    def remove_closed(self, *args, **kwargs):
        """
        """
        ...

    ...

class GraphicsCapturePicker(_winrt._winrt_base):
    """
    base class for wrapped WinRT object instances.
    """

    @staticmethod
    def __new__():
        """
        Create and return a new object.  See help(type) for accurate signature.
        """
        ...

    def pick_single_item_async(self) -> _winrt.IAsyncOperation:
        """
        """
        ...

    ...

class GraphicsCaptureSession(_winrt._winrt_base):
    """
    base class for wrapped WinRT object instances.
    """

    @staticmethod
    def __new__(*args, **kwargs):
        """
        Create and return a new object.  See help(type) for accurate signature.
        """
        ...

    def __enter__(self, *args, **kwargs):
        """
        """
        ...

    def __exit__(self, *args, **kwargs):
        """
        """
        ...

    def close(self, *args, **kwargs):
        """
        """
        ...

    def start_capture(self, *args, **kwargs):
        """
        """
        ...

    ...

__all__: ...
"""
['Direct3D11CaptureFrame', 'Direct3D11CaptureFramePool', 'Gr...
"""
