# pyright: reportMissingImports=false
"""Implement a Kivy widget that renders everything to SPI display while being headless.

* IMPORTANT: You need to run `setup_headless` function before instantiating
`HeadlessWidget`.

A Kivy widget that renders itself on a display connected to the SPI controller of RPi.
It doesn't create any window in any display manager (a.k.a "headless").

When no animation is running, you can drop fps to `min_fps` by calling
`activate_low_fps_mode`.

To increase fps to `max_fps` call `activate_high_fps_mode`.
"""
from __future__ import annotations

import atexit
import time
from pathlib import Path
from queue import Empty, Queue
from threading import Thread
from typing import TYPE_CHECKING

import kivy
import numpy as np
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.graphics.context_instructions import Color
from kivy.graphics.fbo import Fbo
from kivy.graphics.gl_instructions import ClearBuffers, ClearColor
from kivy.graphics.instructions import Canvas
from kivy.graphics.vertex_instructions import Rectangle
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from typing_extensions import Any

from headless_kivy_pi.constants import (
    BAUDRATE,
    BITS_PER_BYTE,
    BYTES_PER_PIXEL,
    CLEAR_AT_EXIT,
    IS_RPI,
    IS_TEST_ENVIRONMENT,
)
from headless_kivy_pi.display import transfer_to_display
from headless_kivy_pi.logger import logger
from headless_kivy_pi.setup import SetupHeadlessConfig, setup_kivy

if TYPE_CHECKING:
    from adafruit_rgb_display.rgb import DisplaySPI
    from kivy.graphics.texture import Texture

import board
import digitalio
from adafruit_rgb_display.st7789 import ST7789

kivy.require('2.2.1')


class HeadlessWidget(Widget):
    """Headless Kivy widget class rendering on SPI connected display."""

    _is_setup_headless_called: bool = False
    should_ignore_hash: bool = False
    texture = ObjectProperty(None, allownone=True)
    _display: DisplaySPI

    min_fps: int
    max_fps: int
    is_paused: bool
    width: int
    height: int
    debug_mode: bool
    double_buffering: bool
    synchronous_clock: bool
    automatic_fps_control: bool

    last_second: int
    rendered_frames: int
    skipped_frames: int
    pending_render_threads: Queue[Thread]
    last_hash: int
    fps: int

    fbo: Fbo
    fbo_rect: Rectangle

    def __init__(self: HeadlessWidget, **kwargs: dict[str, object]) -> None:
        """Initialize a `HeadlessWidget`."""
        if not HeadlessWidget._is_setup_headless_called:
            msg = (
                'You need to run `setup_headless` before instantiating `HeadlessWidget`'
            )
            raise RuntimeError(msg)

        __import__('kivy.core.window')

        if self.debug_mode:
            self.last_second = int(time.time())
            self.rendered_frames = 0
            self.skipped_frames = 0

        self.pending_render_threads = Queue(2 if HeadlessWidget.double_buffering else 1)
        self.last_hash = 0
        self.last_change = time.time()
        self.fps = self.max_fps

        self.canvas = Canvas()
        with self.canvas:
            self.fbo = Fbo(size=self.size, with_stencilbuffer=True)
            self.fbo_color = Color(1, 1, 1, 1)
            self.fbo_rect = Rectangle()

        with self.fbo:
            ClearColor(0, 0, 0, 0)
            ClearBuffers()

        self.texture = self.fbo.texture

        super().__init__(**kwargs)

        self.render_trigger = Clock.create_trigger(
            lambda _: self.render_on_display(),
            1 / self.fps,
            interval=True,
        )
        self.render_trigger()
        app = App.get_running_app()

        def clear(*_: object) -> None:
            self.render_trigger.cancel()

        if app:
            app.bind(on_stop=clear)

    def add_widget(
        self: HeadlessWidget,
        *args: Any,  # noqa: ANN401
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        """Extend `Widget.add_widget` and handle `canvas`."""
        canvas = self.canvas
        self.canvas = self.fbo
        super().add_widget(*args, **kwargs)
        self.canvas = canvas

    def remove_widget(
        self: HeadlessWidget,
        *args: Any,  # noqa: ANN401
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        """Extend `Widget.remove_widget` and handle `canvas`."""
        canvas = self.canvas
        self.canvas = self.fbo
        super().remove_widget(*args, **kwargs)
        self.canvas = canvas

    def on_size(
        self: HeadlessWidget,
        _: HeadlessWidget,
        value: tuple[int, int],
    ) -> None:
        """Update size of `fbo` and size of `fbo_rect` when widget's size changes."""
        self.fbo.size = value
        self.texture = self.fbo.texture
        self.fbo_rect.size = value

    def on_pos(
        self: HeadlessWidget,
        _: HeadlessWidget,
        value: tuple[int, int],
    ) -> None:
        """Update position of `fbo_rect` when widget's position changes."""
        self.fbo_rect.pos = value

    def on_texture(self: HeadlessWidget, _: HeadlessWidget, value: Texture) -> None:
        """Update texture of `fbo_rect` when widget's texture changes."""
        self.fbo_rect.texture = value

    def on_alpha(self: HeadlessWidget, _: HeadlessWidget, value: float) -> None:
        """Update alpha value of `fbo_rect` when widget's alpha value changes."""
        self.fbo_color.rgba = (1, 1, 1, value)

    def pause(self: HeadlessWidget) -> None:
        """Pause writing to the display."""
        HeadlessWidget.is_paused = True

    def resume(self: HeadlessWidget) -> None:
        """Resume writing to the display."""
        self.is_paused = False
        self.should_ignore_hash = True

    def render(self: HeadlessWidget) -> None:
        """Schedule a force render."""
        if not self:
            return
        Clock.schedule_once(self.render_on_display, 0)

    def _activate_high_fps_mode(self: HeadlessWidget) -> None:
        """Increase fps to `max_fps`."""
        if not self.instance:
            return
        logger.info('Activating high fps mode, setting FPS to `max_fps`')
        self.instance.fps = self.max_fps
        self.instance.render_trigger.timeout = 1.0 / self.instance.fps
        self.instance.last_hash = 0

    def activate_high_fps_mode(self: HeadlessWidget) -> None:
        """Schedule increasing fps to `max_fps`."""
        self.render()
        Clock.schedule_once(lambda _: self._activate_high_fps_mode(), 0)

    def _activate_low_fps_mode(self: HeadlessWidget) -> None:
        """Drop fps to `min_fps`."""
        logger.info('Activating low fps mode, dropping FPS to `min_fps`')
        self.fps = self.min_fps
        self.render_trigger.timeout = 1.0 / self.fps

    def activate_low_fps_mode(self: HeadlessWidget) -> None:
        """Schedule dropping fps to `min_fps`."""
        self.render()
        Clock.schedule_once(lambda _: self._activate_low_fps_mode(), 0)

    def render_on_display(self: HeadlessWidget, *_: object) -> None:
        """Render the widget on display connected to the SPI controller."""
        if HeadlessWidget.is_paused:
            return

        # Log the number of skipped and rendered frames in the last second
        if self.debug_mode:
            # Increment rendered_frames/skipped_frames count every frame and reset their
            # values to zero every second.
            current_second = int(time.time())

            if current_second != self.last_second:
                logger.debug(
                    f"""Frames in {self.last_second}: \
[Skipped: {self.skipped_frames}] [Rendered: {self.rendered_frames}]""",
                )
                self.last_second = current_second
                self.rendered_frames = 0
                self.skipped_frames = 0

        # If `synchronous_clock` is False, skip frames if there are more than one
        # pending render in case `double_buffering` is enabled, or if there are ANY
        # pending render in case `double_buffering` is disabled.
        if (
            not HeadlessWidget.synchronous_clock
            and self.pending_render_threads.qsize()
            > (1 if HeadlessWidget.double_buffering else 0)
        ):
            self.skipped_frames += 1
            return

        data = np.frombuffer(self.texture.pixels, dtype=np.uint8)
        data_hash = hash(data.data.tobytes())
        if data_hash == self.last_hash and not HeadlessWidget.should_ignore_hash:
            # Only drop FPS when the screen has not changed for at least one second
            if (
                self.automatic_fps_control
                and time.time() - self.last_change > 1
                and self.fps != self.min_fps
            ):
                logger.debug('Frame content has not changed for 1 second')
                self.activate_low_fps_mode()

            # Considering the content has not changed, this frame can safely be ignored
            return

        if self.debug_mode:
            self.rendered_frames += 1
            with Path('headless_kivy_pi_buffer.raw').open('wb') as snapshot_file:
                snapshot_file.write(
                    bytes(
                        data.reshape(
                            HeadlessWidget.width,
                            HeadlessWidget.height,
                            -1,
                        )[::-1, :, :3]
                        .flatten()
                        .tolist(),
                    ),
                )

        HeadlessWidget.should_ignore_hash = False

        self.last_change = time.time()
        self.last_hash = data_hash
        if self.automatic_fps_control and self.fps != self.max_fps:
            logger.debug('Frame content has changed')
            self.activate_high_fps_mode()

        # Render the current frame on the display asynchronously
        try:
            last_thread = self.pending_render_threads.get(False)
        except Empty:
            last_thread = None
        thread = Thread(
            target=transfer_to_display,
            args=(
                data,
                data_hash,
                last_thread,
            ),
            daemon=True,
        )
        self.pending_render_threads.put(thread)
        thread.start()

    def setup_headless(
        self: HeadlessWidget,
        config: SetupHeadlessConfig | None = None,
    ) -> None:
        """Set up `HeadlessWidget`."""
        if config is None:
            config = {}

        setup_kivy(config)
        baudrate = config.get('baudrate', BAUDRATE)
        display_class: DisplaySPI = config.get('st7789', ST7789)
        clear_at_exit = config.get('clear_at_exit', CLEAR_AT_EXIT)

        if HeadlessWidget.min_fps > HeadlessWidget.max_fps:
            msg = f"""Invalid value "{HeadlessWidget.min_fps}" for "min_fps", it can't \
be higher than 'max_fps' which is set to '{HeadlessWidget.max_fps}'."""
            raise ValueError(msg)

        fps_cap = baudrate / (
            HeadlessWidget.width
            * HeadlessWidget.height
            * BYTES_PER_PIXEL
            * BITS_PER_BYTE
        )

        if HeadlessWidget.max_fps > fps_cap:
            msg = f"""Invalid value "{HeadlessWidget.max_fps}" for "max_fps", it can't \
be higher than "{fps_cap:.1f}" (baudrate={baudrate} ÷ (width={HeadlessWidget.width} x \
height={HeadlessWidget.height} x bytes per pixel={BYTES_PER_PIXEL} x bits per byte=\
{BITS_PER_BYTE}))"""
            raise ValueError(msg)

        if IS_TEST_ENVIRONMENT:
            Config.set('graphics', 'window_state', 'hidden')
            from kivy.core.window import Window
        elif IS_RPI:
            Config.set('graphics', 'window_state', 'hidden')
            spi = board.SPI()
            # Configuration for CS and DC pins (these are PiTFT defaults):
            cs_pin = digitalio.DigitalInOut(board.CE0)
            dc_pin = digitalio.DigitalInOut(board.D25)
            reset_pin = digitalio.DigitalInOut(board.D24)
            display = display_class(
                spi,
                height=HeadlessWidget.height,
                width=HeadlessWidget.width,
                y_offset=80,
                x_offset=0,
                cs=cs_pin,
                dc=dc_pin,
                rst=reset_pin,
                baudrate=baudrate,
            )
            HeadlessWidget._display = display
            if clear_at_exit:
                atexit.register(
                    lambda: display._block(  # noqa: SLF001
                        0,
                        0,
                        HeadlessWidget.width - 1,
                        HeadlessWidget.height - 1,
                        bytes(HeadlessWidget.width * HeadlessWidget.height * 2),
                    ),
                )
        else:
            from kivy.core.window import Window
            from screeninfo import get_monitors

            monitor = get_monitors()[0]

            Window._win.set_always_on_top(True)  # noqa: SLF001
            Window._set_top(200)  # noqa: SLF001
            Window._set_left(monitor.width - Window._size[0])  # noqa: SLF001
        HeadlessWidget._is_setup_headless_called = True

    @classmethod
    def get_instance(
        cls: type[HeadlessWidget],
        widget: Widget,
    ) -> HeadlessWidget | None:
        """Get the nearest instance of `HeadlessWidget`."""
        if isinstance(widget, HeadlessWidget):
            return widget
        if widget.parent:
            return cls.get_instance(widget.parent)
        return None
