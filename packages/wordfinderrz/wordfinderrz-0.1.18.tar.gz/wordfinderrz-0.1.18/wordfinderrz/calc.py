"""A four function calculator."""

from __future__ import annotations

import operator
import time
import tkinter as tk
from collections.abc import Callable
from typing import Any

from wordfinderrz.cache import LruQueue

_KEY_CHARS = "ACcC±%/÷*×+-−=.0123456789"
_OPERATORS_BY_SYMBOL = {
    "+": operator.add,
    "-": operator.sub,
    "−": operator.sub,
    "*": operator.mul,
    "×": operator.mul,
    "/": operator.truediv,
    "÷": operator.truediv,
}
_BG_COLOR = "#252526"
_DARK_BUTTON_COLOR = "#3a3a3b"
_LIGHT_BUTTON_COLOR = "#5b5b5c"
_BUTTON_FONT_SIZE = 22


class Calculator(tk.Tk):
    """Four function calculator tk interface."""

    def __init__(self) -> None:
        super().__init__()
        self.geometry("235x290")
        self.minsize(235, 290)
        self.maxsize(500, 290)
        self.resizable(False, False)
        self.title("Calculator")
        self.last_number: float | None = None
        self.last_operator: Callable[[Any, Any], Any] | None = None
        self.repeat_op: float | None = None
        self.start_new_num_on_press = True
        self._font_size = 40
        self._history: LruQueue[tuple[str, float | None]] = LruQueue(2)
        frm_display = tk.Frame(height=60, bg=_BG_COLOR)
        self.display = CalculatorDisplay(frame=frm_display, app=self, mount=True)
        frm_display.pack_propagate(False)
        frm_display.pack(side=tk.TOP, fill=tk.X)
        self.buttons = ButtonGrid(self, mount=True)
        self.bind("<BackSpace>", self.display.handle_backspace)
        self.bind("<Key>", self.display.handle_key_press)
        self.bind("<Return>", self.display.handle_return)

    def start(self) -> None:
        self.mainloop()


class CalculatorDisplay(tk.Label):
    def __init__(
        self, frame: tk.Frame, app: Calculator, *, mount: bool = False
    ) -> None:
        self.app: Calculator = app
        self._font_size = 40
        super().__init__(
            frame,
            height=1,
            text="0",
            font=f"sans-serif {self.font_size}",
            pady=5,
            padx=10,
            anchor=tk.NE,
            bg=_BG_COLOR,
            fg="white",
        )
        if mount:
            self.mount()

    @property
    def font_size(self) -> int:
        return self._font_size

    @font_size.setter
    def font_size(self, value: int) -> None:
        self._font_size = value
        self["font"] = f"sans-serif {value}"

    def mount(self) -> None:
        self.pack(fill=tk.X, expand=True, anchor=tk.SE)

    @property
    def value(self) -> float:
        return float(self["text"])

    @value.setter
    def value(self, value: float) -> None:
        self["text"] = CalculatorDisplay.fmt_val(value)
        self.autoset_font_size()

    @staticmethod
    def fmt_val(value: float) -> str:
        return str(value).removesuffix(".0")

    def autoset_font_size(self) -> None:
        digit_len = len([dgt for dgt in self["text"] if dgt.isnumeric()])
        if digit_len < 9:
            self.font_size = 40
        elif digit_len < 11:
            self.font_size = 32
        elif digit_len < 13:
            self.font_size = 28
        elif digit_len < 14:
            self.font_size = 25
        elif digit_len < 18:
            self.font_size = 20
        elif digit_len < 20:
            self.font_size = 18
        elif digit_len < 22:
            self.font_size = 16
        else:
            self.font_size = 14

    def add_char(self, char: str) -> None:
        if self.app.start_new_num_on_press or self["text"] == "0":
            self["text"] = char if char != "." else "0."
        else:
            self["text"] += char
        self.autoset_font_size()

    def handle_key_press(self, event: tk.Event) -> None:
        char = event.char
        if char in _KEY_CHARS:
            self.app.buttons.handle_button_press(char)

    def handle_backspace(self, event: tk.Event) -> None:
        if self["text"][:-1] == ",":
            self["text"] = self["text"][:-1]
        self["text"] = self["text"][:-1] if len(self["text"]) > 1 else "0"
        self.autoset_font_size()

    def handle_return(self, event: tk.Event) -> None:
        self.app.buttons.handle_button_press("=")


class ButtonGrid(tk.Frame):
    """Calculator button grid."""

    def __init__(self, app: Calculator, *, mount: bool = False) -> None:
        self.app: Calculator = app
        super().__init__(app, bg=_BG_COLOR)
        self.pack_propagate(False)
        for row in range(5):
            self.rowconfigure(row, weight=1)
        for col in range(4):
            self.columnconfigure(col, weight=1)
        # First row buttons
        self.btn_clear = tk.Label(
            self,
            text="AC",
            font=f"sans-serif 18",
            bg=_DARK_BUTTON_COLOR,
            fg="white",
            width=1,
        )
        self.btn_clear.grid(row=0, column=0, sticky="news", padx=1, pady=1)
        self.btn_clear.bind("<Button-1>", self.handle_button_press)
        self.btn_plus_minus = tk.Label(
            self,
            text="±",
            font=f"sans-serif {_BUTTON_FONT_SIZE}",
            bg=_DARK_BUTTON_COLOR,
            fg="white",
        )
        self.btn_plus_minus.grid(row=0, column=1, sticky="news", padx=1, pady=1)
        self.btn_plus_minus.bind("<Button-1>", self.handle_button_press)
        self.btn_pct = tk.Label(
            self,
            text="%",
            font=f"sans-serif {_BUTTON_FONT_SIZE}",
            bg=_DARK_BUTTON_COLOR,
            fg="white",
        )
        self.btn_pct.grid(row=0, column=2, sticky="news", padx=1, pady=1)
        self.btn_pct.bind("<Button-1>", self.handle_button_press)
        self.btn_divide = tk.Label(
            self,
            text="÷",
            font=f"sans-serif {_BUTTON_FONT_SIZE}",
            bg="#fa8b1b",
            fg="white",
        )
        self.btn_divide.grid(row=0, column=3, sticky="news", padx=1, pady=1)
        self.btn_divide.bind("<Button-1>", self.handle_button_press)
        # Second row buttons
        self.btn_7 = tk.Label(
            self,
            text="7",
            font=f"sans-serif {_BUTTON_FONT_SIZE}",
            bg=_LIGHT_BUTTON_COLOR,
            fg="white",
        )
        self.btn_7.grid(row=1, column=0, sticky="news", padx=1, pady=1)
        self.btn_7.bind("<Button-1>", self.handle_button_press)
        self.btn_8 = tk.Label(
            self,
            text="8",
            font=f"sans-serif {_BUTTON_FONT_SIZE}",
            bg=_LIGHT_BUTTON_COLOR,
            fg="white",
        )
        self.btn_8.grid(row=1, column=1, sticky="news", padx=1, pady=1)
        self.btn_8.bind("<Button-1>", self.handle_button_press)
        self.btn_9 = tk.Label(
            self,
            text="9",
            font=f"sans-serif {_BUTTON_FONT_SIZE}",
            bg=_LIGHT_BUTTON_COLOR,
            fg="white",
        )
        self.btn_9.grid(row=1, column=2, sticky="news", padx=1, pady=1)
        self.btn_9.bind("<Button-1>", self.handle_button_press)
        self.btn_mult = tk.Label(
            self,
            text="×",
            font=f"sans-serif {_BUTTON_FONT_SIZE}",
            bg="#fa8b1b",
            fg="white",
        )
        self.btn_mult.grid(row=1, column=3, sticky="news", padx=1, pady=1)
        self.btn_mult.bind("<Button-1>", self.handle_button_press)
        # Third row buttons
        self.btn_4 = tk.Label(
            self,
            text="4",
            font=f"sans-serif {_BUTTON_FONT_SIZE}",
            bg=_LIGHT_BUTTON_COLOR,
            fg="white",
        )
        self.btn_4.grid(row=2, column=0, sticky="news", padx=1, pady=1)
        self.btn_4.bind("<Button-1>", self.handle_button_press)
        self.btn_5 = tk.Label(
            self,
            text="5",
            font=f"sans-serif {_BUTTON_FONT_SIZE}",
            bg=_LIGHT_BUTTON_COLOR,
            fg="white",
        )
        self.btn_5.grid(row=2, column=1, sticky="news", padx=1, pady=1)
        self.btn_5.bind("<Button-1>", self.handle_button_press)
        self.btn_6 = tk.Label(
            self,
            text="6",
            font=f"sans-serif {_BUTTON_FONT_SIZE}",
            bg=_LIGHT_BUTTON_COLOR,
            fg="white",
        )
        self.btn_6.grid(row=2, column=2, sticky="news", padx=1, pady=1)
        self.btn_6.bind("<Button-1>", self.handle_button_press)
        self.btn_sub = tk.Label(
            self,
            text="−",
            font=f"sans-serif {_BUTTON_FONT_SIZE}",
            bg="#fa8b1b",
            fg="white",
        )
        self.btn_sub.grid(row=2, column=3, sticky="news", padx=1, pady=1)
        self.btn_sub.bind("<Button-1>", self.handle_button_press)
        # Fourth row buttons
        self.btn_1 = tk.Label(
            self,
            text="1",
            font=f"sans-serif {_BUTTON_FONT_SIZE}",
            bg=_LIGHT_BUTTON_COLOR,
            fg="white",
        )
        self.btn_1.grid(row=3, column=0, sticky="news", padx=1, pady=1)
        self.btn_1.bind("<Button-1>", self.handle_button_press)
        self.btn_2 = tk.Label(
            self,
            text="2",
            font=f"sans-serif {_BUTTON_FONT_SIZE}",
            bg=_LIGHT_BUTTON_COLOR,
            fg="white",
        )
        self.btn_2.grid(row=3, column=1, sticky="news", padx=1, pady=1)
        self.btn_2.bind("<Button-1>", self.handle_button_press)
        self.btn_3 = tk.Label(
            self,
            text="3",
            font=f"sans-serif {_BUTTON_FONT_SIZE}",
            bg=_LIGHT_BUTTON_COLOR,
            fg="white",
        )
        self.btn_3.grid(row=3, column=2, sticky="news", padx=1, pady=1)
        self.btn_3.bind("<Button-1>", self.handle_button_press)
        self.btn_add = tk.Label(
            self,
            text="+",
            font=f"sans-serif {_BUTTON_FONT_SIZE}",
            bg="#fa8b1b",
            fg="white",
        )
        self.btn_add.grid(row=3, column=3, sticky="news", padx=1, pady=1)
        self.btn_add.bind("<Button-1>", self.handle_button_press)
        # Fifth row buttons
        self.btn_0 = tk.Label(
            self,
            text="0",
            font=f"sans-serif {_BUTTON_FONT_SIZE}",
            bg=_LIGHT_BUTTON_COLOR,
            fg="white",
        )
        self.btn_0.grid(row=4, column=0, columnspan=2, sticky="news", padx=1, pady=1)
        self.btn_0.bind("<Button-1>", self.handle_button_press)
        self.btn_point = tk.Label(
            self,
            text=".",
            font=f"sans-serif {_BUTTON_FONT_SIZE}",
            bg=_LIGHT_BUTTON_COLOR,
            fg="white",
        )
        self.btn_point.grid(row=4, column=2, sticky="news", padx=1, pady=1)
        self.btn_point.bind("<Button-1>", self.handle_button_press)
        self.btn_eq = tk.Label(
            self,
            text="=",
            font=f"sans-serif {_BUTTON_FONT_SIZE}",
            bg="#fa8b1b",
            fg="white",
        )
        self.btn_eq.grid(row=4, column=3, sticky="news", padx=1, pady=1)
        self.btn_eq.bind("<Button-1>", self.handle_button_press)
        self.char_map: dict[str, tk.Label] = {
            "c": self.btn_clear,
            "C": self.btn_clear,
            "AC": self.btn_clear,
            "±": self.btn_plus_minus,
            "%": self.btn_pct,
            "÷": self.btn_divide,
            "/": self.btn_divide,
            "×": self.btn_mult,
            "*": self.btn_mult,
            "+": self.btn_add,
            "-": self.btn_sub,
            "=": self.btn_eq,
            ".": self.btn_point,
            "0": self.btn_0,
            "1": self.btn_1,
            "2": self.btn_2,
            "3": self.btn_3,
            "4": self.btn_4,
            "5": self.btn_5,
            "6": self.btn_6,
            "7": self.btn_7,
            "8": self.btn_8,
            "9": self.btn_9,
        }
        if mount:
            self.mount()

    def handle_button_press(self, event: tk.Event | str) -> None:
        # handle_button_press can be called by a str representing a key
        # or a tk.Event representing a button press.
        if isinstance(event, tk.Event):
            widget = event.widget
        elif (wgt := self.char_map.get(event)) is not None:
            widget = wgt
        else:
            return None

        char: str = widget["text"]
        bg: str = widget["bg"]

        # Animate button press.
        widget["bg"] = "gray"
        widget.update()
        time.sleep(0.05)
        widget["bg"] = bg

        # Update history.
        if not char.isnumeric():
            self.app._history.append((
                char,
                self.app.display.value if char not in "ACc" else None,
            ))

        # Check if an operator is being used as an implicit '='.
        try:
            implicit_eq = all(
                op in "/÷*×+-−"
                for op in (self.app._history[0][0], self.app._history[1][0])
            )
        except IndexError:
            implicit_eq = False

        if char != "=":
            self.app.repeat_op = None
        if char in "ACc±%/÷*×+-−=":
            self.app.start_new_num_on_press = True
        elif (
            char == "."
            and not self.app.start_new_num_on_press
            and "." in self.app.display["text"]
        ):
            pass
        else:
            self.btn_clear["text"] = "C"
            self.app.display.add_char(char)
            self.app.start_new_num_on_press = False
            return None
        if char in "/÷*×+-−":  # two arg operators
            if not implicit_eq:
                self.app.last_number = self.app.display.value
                self.app.last_operator = _OPERATORS_BY_SYMBOL[char]
        elif char in "cCAC":
            # TODO: Add AC features.
            if char == "AC":
                self.app.last_number = None
                self.app.last_operator = None
            self.app.display.value = 0
            self.btn_clear["text"] = "AC"
            return None
        elif char == "±" and self.app.display.value != 0:
            self.app.display.value *= -1
            return None
        elif char == "%":
            self.app.display.value /= 100
            return None
        if (
            (char == "=" or implicit_eq)
            and self.app.last_number is not None
            and self.app.last_operator is not None
        ):
            current_display_val = self.app.display.value
            if self.app.repeat_op is not None:
                self.app.display.value = self.app.last_operator(
                    self.app.last_number, self.app.repeat_op
                )
            else:
                self.app.display.value = self.app.last_operator(
                    self.app.last_number, self.app.display.value
                )
            self.app.last_number = self.app.display.value
            if self.app.repeat_op is None:
                self.app.repeat_op = current_display_val
            if implicit_eq:
                self.app.last_number = self.app.display.value
                self.app.last_operator = _OPERATORS_BY_SYMBOL[char]

    def mount(self) -> None:
        self.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = Calculator()
    app.start()
