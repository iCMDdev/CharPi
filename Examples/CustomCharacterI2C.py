from CharPi import HD44780I2Cdriver

display = HD44780I2Cdriver(lines=4, columns=20, address=0x27, font=8) # 4 rows, 20 colums display, at I2C address 0x27, with the standard 5x8 font
# Tip: Use font=10 for displays with 5x10 fonts.

display.control(power=1, backlight=1, increment=1, shift=0, cursor=1, blink=1)
"""
The display.control() function can set the following display settings:
  - power: sets the display (liquid crystal, not backlight!) on (1) or off (0)
  - backlight: sets the backlight on (1) or off (0)
  - increment: sets the cursor move direction (1 = increment, 0 = decrement)
  - shift: turns on (1) the option to shift the display when cursor is moved
  - cursor: sets the cursor visible (1) or hidden (0)
  - blink: if cursor is visible, makes the cursor blink (1) or continously stay on (0)
  
The following configuration is the default one:
    display.control(power=1, backlight=1, increment=1, shift=0, cursor=0, blink=0)
"""
# Custom Characters

# Function is defines as: display.NewCharacter(characterArray, character code)
display.NewCharacter([0b01010,
                      0b01010,
                      0b01010,
                      0b00000,
                      0b10001,
                      0b10001,
                      0b01110,
                      0b00000], 0) # Created a smiley face at character code 0

display.NewCharacter([0b00000,
                      0b01000,
                      0b01011,
                      0b00000,
                      0b10001,
                      0b10001,
                      0b01110,
                      0b00000], 1) # Created a smiley face at character code 1


display.writeString("Custom Characters:", delay = 0.1, newlineDelay = 0.3) # write a string with the specified delays. 

# Function is defines as: display.writeChar(character_address)
display.writeChar(0) # write character with code 0
display.writeChar(1) # write character with code 1

# Fun fact: you can use writeString() to write custom characters as well, by placing them in an array! The array can also contain strings as elements.
display.writeString(["Hello!", 0, 1, "\nHow cool is that!?"], lineNum = 1, columnNum = 0, delay = 0.1, newlineDelay = 0.3)

"""
Useful things to know:
1) You can only create 8 characters for 5x8 fonts, and 4 for 5x10 fonts (hardware limit)
2) Each custom character is saved by the display at a specific address in it's memory
3) The custom character's code can range from 0 to 7. You'll need use this address in order to save a new
   character (using the newCharacter() method), as well as to show it on the display (with writeChar())
4) The NewCharacter() method takes an array of (binary) integers as shown above. 1 means the pixel should be on, and 0 means it should be off.
5) Usually, HD44780 displays use 8 pixel width x 5 pixel height characters, but others use 5x10. Check your display to make sure which one you should use.
6) The writeChar() method will write a character with the character code (address) provided as an argument. 
   This means that if you send an address not equal to a custom character address, the display will print the character with the equivalent
   (ASCII) code.
"""
