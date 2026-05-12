"""
  serial_send_controls.py encapsulates the serial command input controls and command history handling.
"""

import tkinter as tk
from tkinter import ttk


class SerialSendControls:
    """Serial command controls with send action and command history navigation."""

    def __init__(self, frame, send_command_callback):
        self.__frame = ttk.Frame(frame)
        ttk.Label(self.__frame, text="Serial Command:").grid(column=0, row=0, sticky="W", padx=(0, 3))

        self.__entry = ttk.Entry(self.__frame)
        self.__entry.grid(column=1, row=0, sticky="EW", padx=3)

        ttk.Button(self.__frame, text="Send", command=self.__send_serial_command).grid(
            column=2,
            row=0,
            sticky="EW",
            padx=(3, 0),
        )

        self.__frame.columnconfigure(1, weight=1)

        self.__history = []
        self.__history_index = None
        self.__unsent_text = ""
        self.__send_command_callback = send_command_callback
        self.__show_controls = True

        self.__entry.bind("<Return>", self.__send_serial_command)
        self.__entry.bind("<Up>", self.__show_previous_serial_command)
        self.__entry.bind("<Down>", self.__show_next_serial_command)

    def set_visible(self, show_controls):
        """Set whether controls should be shown when positioned."""
        self.__show_controls = show_controls

    def set_position(self, row_pos_frame):
        """Position controls on the given row when enabled."""
        if not self.__show_controls:
            return

        self.__frame.grid(column=0, row=row_pos_frame, columnspan=2, sticky="EW", padx=5, pady=(0, 5))

    def __send_serial_command(self, event=None):
        """Send command from entry field to serial interface."""
        del event
        command = self.__entry.get().strip()
        if self.__send_command_callback(command):
            if command:
                self.__history.append(command)
            self.__history_index = None
            self.__unsent_text = ""
            self.__entry.delete(0, tk.END)

    def __show_previous_serial_command(self, event=None):
        """Show previous command from history in entry field."""
        del event
        if not self.__history:
            return "break"

        if self.__history_index is None:
            self.__unsent_text = self.__entry.get()
            self.__history_index = len(self.__history) - 1
        elif self.__history_index > 0:
            self.__history_index -= 1

        self.__set_serial_command_entry(self.__history[self.__history_index])
        return "break"

    def __show_next_serial_command(self, event=None):
        """Show next command from history in entry field."""
        del event
        if self.__history_index is None:
            return "break"

        if self.__history_index < len(self.__history) - 1:
            self.__history_index += 1
            self.__set_serial_command_entry(self.__history[self.__history_index])
        else:
            self.__history_index = None
            self.__set_serial_command_entry(self.__unsent_text)
        return "break"

    def __set_serial_command_entry(self, text):
        """Replace full serial command entry content."""
        self.__entry.delete(0, tk.END)
        self.__entry.insert(0, text)
