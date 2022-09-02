from CharPi import HD44780I2Cdriver

display = HD44780I2Cdriver(lines=4, columns=20, address=0x27) # 4 rows, 20 colums display, at I2C address 0x27
display.writeString("Hello, World!", delay = 0.1, newlineDelay = 0.3) # write a string with the specified delays. 
display.writeString("I'm using a HD44780 display!", lineNum = 2, columnNum = 0) # write a string, starting at the specified coordinates

# Useful to know:

# 1) writeString() automatically writes on the next line when needed, unless the disableAutoNewline argument is set to True.
#       Example: display.writeString("No Automatic Newline", disableAutoNewline=True) # automatic newline is disabled.

# 2) On some displays, when automatic newline is disabled, you might notice the letters appear on another line (not necessarily the next one)
#    when writing strings beyond the current line's maximum character limit. This is normal behaivour, caused by the display's memory 
#    being assigned in that order.

# 3) Coordinates (row number and column number) start at 0.

# 4) You can change your display's address when initializing the display object, as well as your display's dimensions (number of lines and columns)
