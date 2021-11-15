import smbus # I2C
from time import sleep
    
class HD44780I2Cdriver:
    bus = smbus.SMBus(1)
    i2cAddress = 0x27   # Default I2C address of an unmodified backpack. Change it in your program if yours has a different one
    mode = 4
    RS = False          # RS, RW and E are pins that are used in different low-level functions. Check the HD44780 documentation for more info.
    RW = False          
    E = False
    backlight = True    # Changing this value will make the display's backlight turn on or off next time when the RPi communicates with the I2C (writeBits())
    totalLines = None   # Initialising display lines & columns
    totalColumns = None
    line = 0            # Current line position
    column = 0          # Current column position
    
    def __init__(self, lines=2, columns=16, font=8, cursor=0, blink=0, address=0x27):
        self.totalLines = lines         # number of lines
        self.totalColumns = columns     # number of columns
        self.i2cAddress = address       # address init
        
        # Display init as described in the datasheet.
        
        sleep(0.015)
        self.writeBits(0b00110011)  # init
        sleep(0.005)
        self.writeBits(0b00110010)  # init 4 bit
        sleep(0.0001)
        
        # FUNCTION SET
        # setting the font variable to F bit value:
        if font==10:
            font = 1
        else:
            font = 0
        
        self.functionSet(self.mode/4-1, lines>1, font)
        sleep(0.0001)
        
        # DISPLAY CONTROL = OFF
        self.displayControl(0, 0, 0)
        sleep(0.0001)
    
        # DISPLAY CLEAR
        self.clear()
        sleep(0.0001)
        
        # ENTRY MODE SET
        self.entryModeSet(1, 0)
        sleep(0.0001)
        
        # DISPLAY ON
        self.displayControl(1, cursor, blink)
        sleep(0.0001)
        
    def writeBits(self, hexData):
        self.delayMicroseconds(1000)
        
        # first 4 bits:
        i2cdata = 240 & hexData
        if self.RS == True:
            i2cdata = i2cdata | 1
        if self.RW == True:
            i2cdata = i2cdata | 2
        if self.backlight == True:
            i2cdata = i2cdata | 8
        self.delayMicroseconds(1)
        self.bus.write_byte(self.i2cAddress, i2cdata | 4)
        self.delayMicroseconds(1)
        self.bus.write_byte(self.i2cAddress, i2cdata)
        self.delayMicroseconds(1)
        
        # last 4 bits:
        i2cdata = (15 & hexData) << 4
        if self.RS == True:
            i2cdata = i2cdata | 1
        if self.RW == True:
            i2cdata = i2cdata | 2
        if self.backlight == True:
            i2cdata = i2cdata | 8
        
        self.delayMicroseconds(1)
        self.bus.write_byte(self.i2cAddress, i2cdata | 4)
        self.delayMicroseconds(1)
        self.bus.write_byte(self.i2cAddress, i2cdata)
        self.delayMicroseconds(1)
        sleep(0.01)
        
    def delayMicroseconds(self, microseconds):
        """
        Easier way to sleep by typing the delay time in microseconds.
        """
        s = microseconds / float(1000000)
        sleep(s)
    """
    def allOff(self):
        # This function turn all pins off, but it isn't used in the I2C mode.
        #GPIO.output(self.E, 0)
        for pin in self.DB:
            #GPIO.setup(pin, 0)
    """
    def functionSet(self, DL, N, F):
        """
        From the datasheet:
        DL = data format (4 bits = 0, 8 bits = 1)
        N  = number of lines (2 lines = 1, 1 line = 0)
        F  = font size (5x10 dots = 1, 5x8 dots = 0)
        """
        if DL == 1:
            DL = 0b00110000
        else:
            DL = 0b00100000
        if N == 1:
            N = 0b00101000
        else:
            N = 0b00100000
        if F == 1:
            F = 0b00100100
        else:
            F = 0b00100000
        self.writeBits(0b00100000 | DL | N | F)
        
    def displayControl(self, displayState, cursorState, cursorBlink):
        """
        Low-level function from the datasheet.
        displayState = display on (1) / off (0)
        cursorState  = cursor on (1) / off (0)
        cursorBlink  = cursor blink on (1) / off (0)
        """
        if displayState == True:
            displayState = 0b00001100
        if cursorState == True:
            cursorState = 0b00001010
        if cursorBlink == True:
            cursorBlink = 0b00001001
        # when any of the previous attr = off, main number bitwise OR-ing 0b00001000 with 0 has no effect
        self.writeBits(0b00001000 | displayState | cursorState | cursorBlink)
    
    def clear(self):
        """
        Function from the datasheet that clears the display and resets the cursor's position. It has no parameters.
        """
        self.line=0
        self.column=0
        self.writeBits(0b00000001)
        sleep(0.001)
    
    def entryModeSet(self, ID, S):
        """
        Info from the datasheet:
        ID = increment (1) / decrement (0) the cursor position after each data write / read operation
        S = display shift (1 = display shift, 0 = no display shift)
        """
        if ID == 1:
            ID = 0b00000110
        if S == 1:
            S = 0b00000101
        # if S / ID = 0, bitwise OR-ing the main number with ID / S has no effect
        self.writeBits(0b00000100 | ID | S)
        
    def writeString(self, string, lineNum=-1, columnNum=-1, delay=0.05, newlineDelay=0):
        """
        This function writes the parsed string to the register.
        '\n' is used as a newline character.
        The string parameter is the message that you want to show on the display. It could be a string (str), a character code (int) or a Python list that contains both.
        Character codes are usually used to print custom characters.
        lineNum and columnNum parameters can be used to indicate the cursor's starting position.
        delay and newlineDelay parameters are variables that change the delay after each character (or line).
        """
        lineOffset = (0x00, 0x40, 0x14, 0x54)    # will be changed to RowAddresses variable in a future update
        
        if lineNum > 3:
            raise ValueError("Parsed line index is out of range.")
        if lineNum > 3:
            raise ValueError("Parsed column index is out of range.")
        
        if lineNum == -1:
            lineNum = self.line
        if columnNum == -1:
            columnNum = self.column
        if columnNum > self.totalColumns-1:
            lineNum = lineNum + 1
            columnNum = 0
        if lineNum > self.totalLines-1:
            lineNum = 0
        self.RS=0
        self.DDRAMaddress(lineOffset[lineNum]+columnNum)
        self.line = lineNum
        self.column = columnNum
        self.RS = 1
        
        linerIndex = 0
        for char in range(0, len(string)):
            if string[char] != '\n':
                afterRecursivity=False
                if type(string[char]) == str and len(string[char])>1:
                    # recursive function (calling itself) if a string with more than one character is parsed into a Python list
                    self.line=lineNum
                    self.column=columnNum
                    afterRecursivity=True
                    self.writeString(string[char], delay=delay, newlineDelay=newlineDelay)
                    self.RS=1
                    lineNum = self.line
                    columnNum = self.column
                   
                elif type(string[char]) == str: # support for both str and 'int' character codes
                    self.writeBits(ord(string[char]))
                elif type(string[char]) == int:
                    self.writeBits(string[char])
                    #sleep(0.1) # should be removed?
                if columnNum < self.totalColumns-1 and afterRecursivity == False:
                    columnNum+=1     
                
                elif afterRecursivity == False:
                    columnNum=0
                    lineNum+=1
                    if lineNum > self.totalLines-1:
                        lineNum = 0
                    self.RS = 0
                    self.DDRAMaddress(lineOffset[lineNum]+columnNum)
                    self.RS = 1
                    sleep(newlineDelay)
                    self.delayMicroseconds(4)
                sleep(delay) 
            else:
                columnNum=0
                lineNum+=1
                if lineNum > self.totalLines-1:
                    lineNum = 0
                self.RS = 0
                self.DDRAMaddress(lineOffset[lineNum]+columnNum)
                self.RS = 1
                sleep(newlineDelay)
                self.delayMicroseconds(4)
        self.line = lineNum
        self.column = columnNum
        self.RS=0
    
    def control(self, power=1, backlight=1, increment=1, shift=0, cursor=0, blink=0):
        """
        This function combines the majority of the display's control functions to make it easier
        for the user to manage their device in one single place.
        """
        self.backlight = backlight
        self.entryModeSet(increment, shift)
        self.displayControl(power, cursor, blink)
    
    def writeChar(self, char):
        """
        This simple function writes a character.
        The char parameter should be a character code (int).
        """
        self.RS = 1
        self.writeBits(char)
        self.delayMicroseconds(100)
        self.RS = 0
    
    def DDRAMaddress(self, address):
        """
        This function sets the DDRAM address.
        After setting a DDRAM address, all write data is written into the DDRAM.
        """
        self.writeBits(0b10000000 | address)
        
    def CGRAMaddress(self, address):
        """
        This function sets the CGRAM address.
        After setting a CGRAM address, all write data is written into the CGRAM.
        """
        self.writeBits(0b01000000 | address)
    
    def NewCharacter(self, charArr, address):
        """
        This function simplifies the character creation process.
        The charArr parameter needs to be an an array made out of 8 binary values.
        """

        self.CGRAMaddress(address)
        self.RS = 1
        for line in charArr:
            self.writeBits(line)
        self.RS = 0
    
    def shift(self, display, cursor, position):
        """
        This function shifts the display and / or the cursor.
        """
        if display == True:
            display = 0b00011000
        if position == True:
            position = 0b00010100
        for i in range(0, position):
            self.writeBits(0b00010000 | display | cursor)
                                                                                                                                                                                                                                                   
    def returnHome(self):
        """
        This function returns the cursor and the display shift to the original position, withoutt changing the DDRAM contents.
        """
        self.line=0
        self.column=0
        self.writeBits(0b00000010)
        sleep(0.1)
        
    def scroll(self, pos, speed=0):
        """
        This function scrolls the display.
        """
        for i in range(0, pos):
            self.writeBits(0b00011000)
            sleep(speed)
            
    #def readAddress(self) - future update
    #def readBusyFlag(self): - future update
    #def readBits - future update
