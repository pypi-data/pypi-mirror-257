# SPDX-FileCopyrightText: 2024 Justin Myers
#
# SPDX-License-Identifier: MIT
"""
Board stub for PewPew LCD
 - port: atmel-samd
 - board_id: pewpew_lcd
 - NVM size: 256
 - Included modules: array, board, builtins, busdisplay, busio, busio.SPI, busio.UART, collections, digitalio, displayio, epaperdisplay, fontio, fourwire, i2cdisplaybus, microcontroller, os, pwmio, random, storage, struct, supervisor, sys, terminalio, time, touchio, usb_cdc
 - Frozen libraries: pew
"""

# Imports
import displayio
import microcontroller


# Board Info:
board_id: str


# Pins:
_SCK: microcontroller.Pin  # PA23
_MOSI: microcontroller.Pin  # PA22
_CS: microcontroller.Pin  # PA19
_RST: microcontroller.Pin  # PA18
_BL: microcontroller.Pin  # PA17
_UP: microcontroller.Pin  # PA03
_DOWN: microcontroller.Pin  # PA05
_LEFT: microcontroller.Pin  # PA04
_RIGHT: microcontroller.Pin  # PA02
_O: microcontroller.Pin  # PA06
_X: microcontroller.Pin  # PA07
P1: microcontroller.Pin  # PA30
P2: microcontroller.Pin  # PA31
P3: microcontroller.Pin  # PA08
P4: microcontroller.Pin  # PA09
P5: microcontroller.Pin  # PA10
P6: microcontroller.Pin  # PA11
P7: microcontroller.Pin  # PA14


# Members:
"""Returns the `displayio.Display` object for the board's built in display.
The object created is a singleton, and uses the default parameter values for `displayio.Display`.
"""
DISPLAY: displayio.Display


# Unmapped:
#   none
