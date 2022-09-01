from CharPi import HD44780I2CDriver

display = HD44780I2Cdriver(lines=4, columns=20) # 4 rows, 20 colums display
display.writeString("Hello, World!", delay = 0.1, newlineDelay = 0.3) # write a string with the specified delays. 
display.writeString("I'm using a HD44780 display!", lineNum = 2, columnNum = 0) # write a string, starting at the specified coordinates

# Useful to know: 
# 1) writeString() automatically writes on the next line when needed, unless the disableAutoNewline argument is set to True.
# 2) Coordinates (row number and column number) start at 0.
