
from machine import Pin, PWM
from time import ticks_ms
import urandom

# LED tengingar (6 LED)

leds = [Pin(i, Pin.OUT) for i in range(11, 17)]
led_7 = Pin(10, Pin.OUT)  # kast LED

takki = Pin(9, Pin.IN, Pin.PULL_UP)
buzzer = PWM(Pin(14), 2446)

players = [1, 1, 1, 1]
current_player = 0

last_press_time = 0
press_interval = 1000
button_was_pressed = False

led_on = False
led_on_start = 0
led_on_duration = 1000

while True:
    buzzer.deinit()
    now = ticks_ms()
    button_state = takki.value()

    # Slökkva á LED eftir 1 sekúndu
    if led_on and (now - led_on_start) > led_on_duration:
        for led in leds:
            led.value(0)
        led_7.value(0)
        led_on = False

    if button_state == 0:
        if not button_was_pressed and (now - last_press_time) > press_interval:
            last_press_time = now
            button_was_pressed = True

            teningur = urandom.randint(1, 6)
            players[current_player] += teningur

            # Kveikja á LED 1 til teningur
            for i in range(teningur):
                leds[i].value(1)

            led_7.value(1)
            led_on = True
            led_on_start = now

            print(f"Player {current_player+1} kastar {teningur}, staða: {players[current_player]}")

            setbacks = {34: 11, 32: 21, 16: 6}
            if players[current_player] in setbacks:
                print(f"Player {current_player+1} lenti á reit {players[current_player]}! Færist aftur í {setbacks[players[current_player]]}.")
                players[current_player] = setbacks[players[current_player]]

            if players[current_player] >= 36:
                print(f"Leikurinn er búinn! Player {current_player+1} vann!")
                buzzer.init(2446)
                break

            current_player = (current_player + 1) % len(players)

    else:
        button_was_pressed = False

