from CharPi import HD44780I2Cdriver

display = HD44780I2Cdriver(lines=4, columns=20) # 20x4 display at default address 0x27

display.NewCharacter([0b00000,
                      0b01000,
                      0b01011,
                      0b00000,
                      0b10001,
                      0b10001,
                      0b01110,
                      0b00000], 0) # create a new custom character with code 0

display.NewCharacter([0b00000,
                      0b01010,
                      0b01010,
                      0b00000,
                      0b10001,
                      0b10001,
                      0b01110,
                      0b00000], 1) # create a new custom character with code 1

display.writeString("Hello world!")
display.writeString(["I'm using CharPi \nHD44780 Library! ", 0, "\nHow cool is that!", 1], lineNum = 1, columnNum = 0)
