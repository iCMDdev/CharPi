from CharPi import HD44780_4bitDriver

display = HD44780_4bitDriver(25, 24, (23, 17, 27, 22), lines=4, columns=20) # 4 rows, 20 colums display, with specified pins (more details below)
display.writeString("Hello, World!", delay = 0.1, newlineDelay = 0.3) # write a string with the specified delays. 
display.writeString("I'm using a HD44780 display!", lineNum = 2, columnNum = 0) # write a string, starting at the specified coordinates

# Useful to know:

# 1) writeString() automatically writes on the next line when needed, unless the disableAutoNewline argument is set to True.
#       Example: display.writeString("No Automatic Newline", disableAutoNewline=True) # automatic newline is disabled.

# 2) On some displays, when automatic newline is disabled, you might notice the letters appear on another line (not necessarily the next one)
#    when writing strings beyond the current line's maximum character limit. This is normal behaivour, caused by the display's memory 
#    being assigned in that order.

# 3) Coordinates (row number and column number) start at 0.

# 4) You can change your display's pins:
#    display.HD44780_4bitDriver(RS_Pin, EN_Pin, (D4, D5, D6, D7), lines=4, columns=20)
#    Note: you must provide all your pin BCM IDs
