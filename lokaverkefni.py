from machine import Pin, PWM
from time import ticks_ms
import urandom

# Ljósa stillingar
led_1 = Pin(11, Pin.OUT)
led_2 = Pin(12, Pin.OUT)
led_3 = Pin(13, Pin.OUT)
led_4 = Pin(14, Pin.OUT)
led_5 = Pin(15, Pin.OUT)
led_6 = Pin(16, Pin.OUT)
led_7 = Pin(10, Pin.OUT)

# Takkastillingar
takki = Pin(9, Pin.IN, Pin.PULL_UP)

# Buzzer
buzzer=PWM(Pin(14),2446)

#tengja saman leds
leds = [led_1, led_2, led_3, led_4, led_5, led_6]

#seta players í hópa
players = [1, 1, 1, 1]  # Initial positions
current_player = 0  # Start with player 1

while True:
    buzzer.deinit()
    if takki.value():  # Button is pressed
        teningur = urandom.randint(1, 6)  # Roll dice
        players[current_player] += teningur  # Move current player

        # Light up corresponding LED based on dice roll
        led_7.value(1)  # Indicate action
        leds[teningur - 1].value(1)  # Light up based on dice roll

        print(f"Player {current_player+1} rolled {teningur}, now at position {players[current_player]}")

        # Special positions that send players backward
        setbacks = {34: 11, 32: 21, 16: 6}
        if players[current_player] in setbacks:
            print(f"Player {current_player+1} landed on {players[current_player]}! Moving back to {setbacks[players[current_player]]}.")
            players[current_player] = setbacks[players[current_player]]

        # Check for win condition
        if players[current_player] >= 36:
            print(f"Leikurinn er búinn! Player {current_player+1} vann!")
            buzzer.init(2446)
            break  # End the game

        # Turn off LEDs after action
        leds[teningur - 1].value(0)
        led_7.value(0)

        # Move to the next player
        current_player = (current_player + 1) % len(players)

        # Wait for button release before proceeding
        while takki.value():
            pass
    else:
        pass
