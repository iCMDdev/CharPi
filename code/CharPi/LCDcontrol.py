from time import sleep

# Pin initialisation
# GPIO setup

class HD44780_4bitDriver:
    # control mode - 4bit or 8bit
    import RPi.GPIO as GPIO
    lineOffset = (0x00, 0x40, 0x14, 0x54)
    RSpin = 25
    ENpin = 24
    Dpins = (23, 17, 27, 22)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RSpin, GPIO.OUT)
    GPIO.setup(ENpin, GPIO.OUT)
    for i in range(0, 4):
        GPIO.setup(Dpins[i], GPIO.OUT)
    for i in range(0, 4):
        GPIO.setup(Dpins[i], GPIO.LOW)
    mode = 4
    RS = False
    RW = False
    E = False
    totalLines = None
    totalColumns = None
    line = 0
    column = 0
    
    def __init__(self, lines=2, columns=16, font=8, cursor=0, blink=0):
        self.totalLines = lines
        self.totalColumns = columns
        self.GPIO.setup(self.RSpin, self.GPIO.LOW)
        self.GPIO.setup(self.ENpin, self.GPIO.LOW)
        sleep(0.015)
        self.writeBits(0x33)  # init
        sleep(0.005)
        self.writeBits(0x32)  # init 4 bit
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
        #print(" hexdata:")
        #print(bin(hexData))
        bits = (240 & hexData) >> 4
        #print(" first 4 bits:")
        #print(bin(bits))
        if self.RS == True:
            self.GPIO.output(self.RSpin, self.GPIO.HIGH)
        elif self.RS == False:
            self.GPIO.output(self.RSpin, self.GPIO.LOW)
        #if self.RW == True:
            #self.GPIO.output(self.RWpin, GPIO.HIGH)
        self.delayMicroseconds(1)
        
        for i in range(0, 4):
            #print(self.Dpins[3-i], (bits & (0b1000 >> i))>>(3-i), bin(bits))
            self.GPIO.output(self.Dpins[3-i], (bits & (0b1000 >> i))>>(3-i))
            self.delayMicroseconds(1)
        self.GPIO.output(self.ENpin, False)
        self.delayMicroseconds(1) # 1 microsecond pause - enable pulse must be > 450ns 
        self.GPIO.output(self.ENpin, True)
        self.delayMicroseconds(1) # 1 microsecond pause - enable pulse must be > 450ns 
        self.GPIO.output(self.ENpin, False)
        self.delayMicroseconds(1) #commands need > 37us to settle
            
        # last 4 bits:
        bits = (15 & hexData)
        #print(" last:")
        #print(bin(bits))
        self.delayMicroseconds(1)
        for i in range(0,4):
            #print(self.Dpins[3-i], bin((bits & (0b1000 >> i))>>(3-i)), bin(bits))
            """if (bits & (0b1000 >> i))>>(3-i) == self.GPIO.HIGH:
                print('true', (bits & (0b1000 >> i))>>(3-i))"""
            self.GPIO.output(self.Dpins[3-i], (bits & (0b1000 >> i))>>(3-i))
            self.delayMicroseconds(10)
        self.GPIO.output(self.ENpin, False)
        self.delayMicroseconds(1) # 1 microsecond pause - enable pulse must be > 450ns 
        self.GPIO.output(self.ENpin, True)
        self.delayMicroseconds(1) # 1 microsecond pause - enable pulse must be > 450ns 
        self.GPIO.output(self.ENpin, False)
        self.delayMicroseconds(1) #commands need > 37us to settle
        sleep(0.01)
        
    def delayMicroseconds(self, microseconds):
        seconds = microseconds / float(1000000)   # divide microseconds by 1 million for seconds
        sleep(seconds)
    """
    def allOff(self):
        #GPIO.output(self.E, 0)
        for pin in self.DB:
            #GPIO.setup(pin, 0)
    """
    def functionSet(self, DL, N, F):
        """
        From the datasheet:
        https://www.sparkfun.com/datasheets/LCD/HD44780.pdf
        
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
        Function from the datasheet. It has no parameters.
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
        """
        #lineOffset = (0x00, 0x40, 0x14, 0x54)    # modify this to modify where each line starts
        
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
        self.RS = 0
        self.DDRAMaddress(self.lineOffset[lineNum]+columnNum)
        self.line = lineNum
        self.column = columnNum
        self.RS = 1
        
        linerIndex = 0
        for char in range(0, len(string)):
            if string[char] != '\n':
                # function calling itself if a string with more than one character is parsed into an array
                afterRecursivity=False
                if type(string[char]) == str and len(string[char])>1:
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
                    sleep(0.1)
                if columnNum < self.totalColumns-1 and afterRecursivity == False:
                    columnNum+=1     
                
                elif afterRecursivity == False:
                    columnNum=0
                    lineNum+=1
                    if lineNum > self.totalLines-1:
                        lineNum = 0
                    self.RS = 0
                    self.DDRAMaddress(self.lineOffset[lineNum]+columnNum)
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
                self.DDRAMaddress(self.lineOffset[lineNum]+columnNum)
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
        self.RS = 1
        self.writeBits(char)
        self.delayMicroseconds(100)
        self.RS = 0
    
    def DDRAMaddress(self, address):
        """
        This function sets the DDRAM address.
        After setting a DDRAM address, all write data is written into the DDRAM
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
        self.RS = 0
        self.CGRAMaddress(address << 3)
        self.RS = 1
        for line in charArr:
            #print(bin(line))
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
            
    #def readAddress(self)
        
    #def readBusyFlag(self):
    #def readBits


    
class HD44780I2Cdriver:
    import smbus
    # control mode - 4bit or 8bit
    bus = smbus.SMBus(1)
    i2cAddress = 0x27
    mode = 4
    RS = False
    RW = False
    E = False
    backlight = True
    totalLines = None
    totalColumns = None
    line = 0
    column = 0
    
    def __init__(self, lines=2, columns=16, font=8, cursor=0, blink=0, address=0x27):
        self.totalLines = lines
        self.totalColumns = columns
        self.i2cAddress = address
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
        seconds = microseconds / float(1000000)   # divide microseconds by 1 million for seconds
        sleep(seconds)
    """
    def allOff(self):
        #GPIO.output(self.E, 0)
        for pin in self.DB:
            #GPIO.setup(pin, 0)
    """
    def functionSet(self, DL, N, F):
        """
        From the datasheet:
        https://www.sparkfun.com/datasheets/LCD/HD44780.pdf
        
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
        Function from the datasheet. It has no parameters.
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
        
    def writeString(self, string, lineNum=-1, columnNum=-1, delay=0.05, newlineDelay=0, disableAutoNewline=False):
        """
        This function writes the parsed string to the register.
        '\n' is used as a newline character.
        """
        lineOffset = (0x00, 0x40, 0x14, 0x54)    # modify this to modify where each line starts
        
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
        
        if disableAutoNewline:
            self.delayMicroseconds(4)
            for char in range(0, len(string)):
                if string[char] != '\n':
                    self.RS=1
                    if type(string[char]) == str: # support for both str and 'int' character codes
                        self.writeBits(ord(string[char]))
                    columnNum += 1
                    self.column=columnNum
                    sleep(delay)
                else:
                    columnNum = 0
                    self.column=0
                    lineNum+=1
                    self.line=lineNum
                    self.RS = 0
                    self.DDRAMaddress(lineOffset[lineNum])
                    self.RS = 1
                    sleep(newlineDelay)
                    self.delayMicroseconds(4)
            self.RS = 0
                    
        else:
            linerIndex = 0
            for char in range(0, len(string)):
                if string[char] != '\n':
                    # function calling itself if a string with more than one character is parsed into an array
                    afterRecursivity=False
                    if type(string[char]) == str and len(string[char])>1:
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
                        sleep(0.1)
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
        self.RS = 1
        self.writeBits(char)
        self.delayMicroseconds(100)
        self.RS = 0
    
    def DDRAMaddress(self, address):
        """
        This function sets the DDRAM address.
        After setting a DDRAM address, all write data is written into the DDRAM
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
        self.RS = 0
        self.CGRAMaddress(address << 3)
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
            
    #def readAddress(self)
        
    #def readBusyFlag(self):
    #def readBits

    
class HD44780CustomDriver:
    # control mode - 4bit or 8bit
    mode = 4
    RS = False
    RW = False
    E = False
    backlight = True
    totalLines = None
    totalColumns = None
    line = 0
    column = 0
    
    def __init__(self, callback, lines=2, columns=16, font=8, cursor=0, blink=0):
        self.totalLines = lines
        self.totalColumns = columns
        
        if not callable(callback):
            raise TypeError("You need to provide a data write function through the callback parameter.")
        
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
        # 0b (PIN 1) (PIN 2) (PIN 3) (PIN 4) (BACKLIGHT) (none) (RW) (RS)
        
        # first 4 bits:
        i2cdata = 240 & hexData
        if self.RS == True:
            i2cdata = i2cdata | 1
        if self.RW == True:
            i2cdata = i2cdata | 2
        if self.backlight == True:
            i2cdata = i2cdata | 8
        self.delayMicroseconds(1)
        self.callback(i2cdata | 4)
        self.delayMicroseconds(1)
        self.callback(i2cdata)
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
        self.callback(i2cdata | 4)
        self.delayMicroseconds(1)
        self.callback(i2cdata)
        self.delayMicroseconds(1)
        sleep(0.01)
        
    def delayMicroseconds(self, microseconds):
        seconds = microseconds / 1000000.0
        sleep(seconds)
    """
    def allOff(self):
        #GPIO.output(self.E, 0)
        for pin in self.DB:
            #GPIO.setup(pin, 0)
    """
    def functionSet(self, DL, N, F):
        """
        From the datasheet:
        https://www.sparkfun.com/datasheets/LCD/HD44780.pdf
        
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
        Function from the datasheet. It has no parameters.
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
        
    def writeString(self, string, lineNum=-1, columnNum=-1, delay=0.05, newlineDelay=0, disableAutoNewline=False):
        """
        This function writes the parsed string to the register.
        '\n' is used as a newline character.
        """
        lineOffset = (0x00, 0x40, 0x14, 0x54)    # modify this to modify where each line starts
        
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
        
        if disableAutoNewline:
            self.delayMicroseconds(4)
            for char in range(0, len(string)):
                if string[char] != '\n':
                    self.RS=1
                    if type(string[char]) == str: # support for both str and 'int' character codes
                        self.writeBits(ord(string[char]))
                    columnNum += 1
                    self.column=columnNum
                    sleep(delay)
                else:
                    columnNum = 0
                    self.column=0
                    lineNum+=1
                    self.line=lineNum
                    self.RS = 0
                    self.DDRAMaddress(lineOffset[lineNum])
                    self.RS = 1
                    sleep(newlineDelay)
                    self.delayMicroseconds(4)
            self.RS = 0
                    
        else:
            linerIndex = 0
            for char in range(0, len(string)):
                if string[char] != '\n':
                    # function calling itself if a string with more than one character is parsed into an array
                    afterRecursivity=False
                    if type(string[char]) == str and len(string[char])>1:
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
                        sleep(0.1)
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
        self.RS = 1
        self.writeBits(char)
        self.delayMicroseconds(100)
        self.RS = 0
    
    def DDRAMaddress(self, address):
        """
        This function sets the DDRAM address.
        After setting a DDRAM address, all write data is written into the DDRAM
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
        self.RS = 0
        self.CGRAMaddress(address << 3)
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
            
    #def readAddress(self)
        
    #def readBusyFlag(self):
    #def readBits   
