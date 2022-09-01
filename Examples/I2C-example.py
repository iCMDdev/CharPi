from CharPi import HD44780I2CDriver

display = HD44780I2Cdriver(lines=4, columns=20) # 4 rows, 20 colums display
display.writeString("Hello World! I'm using a HD44780 display!", delay = 0.1, newlineDelay = 0.3) # write a string with the specified delays
