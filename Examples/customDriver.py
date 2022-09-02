from CharPi import HD44780CustomDriver

def callbackHandler(command):
  # This function should handle the command
  # AKA send it to the display (or even a display simulator)
  print(bin(command))

print("Starting init sequence by calling object:")
display = HD44780CustomDriver(callbackHandler, lines=4, columns=16) # initializing this object will actually make it communicate with the display (CharPi sends the display init sequence)
print("Init done. Writing string:")
display.writeString("Hello world!")
