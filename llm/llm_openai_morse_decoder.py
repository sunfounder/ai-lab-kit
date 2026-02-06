from fusion_hat.llm import OpenAI
from secret import OPENAI_API_KEY
from fusion_hat.pin import Pin
import random,time



# Register OpenAI API
# openai.com

# Export your openai api key with :LLM_API_KEY
# export LLM_API_KEY=sk-xxxxxxxxxxxxxxxxx


# setup GPIO
morse_input = Pin(22, mode=Pin.IN, pull= Pin.PULL_DOWN, bounce_time=0.05)
start_stop_button = Pin(17, mode=Pin.IN, pull= Pin.PULL_DOWN, bounce_time=0.05)
led = Pin(27, Pin.OUT)  # indicate LED to GPIO 27

# store the morse code events
morse_events = []
input_active = False  # flag to indicate if the input is active



# Setup LLM
INSTRUCTIONS = "You are a Morse code decoder. Decode based on the button press time, interpreting short presses as dots and long presses as dashes. The message you receive may be a word or a sentence, please decode it and output it."

WELCOME = "Hello, I am a Morse code decoder. Please press the button to start decoding. When you are done, press the button again to stop."

llm = OpenAI(
    api_key=OPENAI_API_KEY,
    model="gpt-4o",
)

# Set how many messages to keep
llm.set_max_messages(20)
# Set instructions
llm.set_instructions(INSTRUCTIONS)
# Set welcome message
llm.set_welcome(WELCOME)

print(WELCOME)



# send the morse code to the AI for decoding
def decode_and_print():
    global morse_events

    input_text = str(morse_events)# Response with stream
    response = llm.prompt(input_text, stream=True)
    for next_word in response:
        if next_word:
            print(next_word, end="", flush=True)
    print("")

    morse_events = []  # clear the morse code events

# morse code input
start_time = 0


def morse_input_pressed():
    global start_time
    start_time = time.time()  
    morse_events.append(('pressed', start_time))
    print(f" Pressed at {start_time} -", end="")

def morse_input_released():
    global morse_events,start_time
    release_time = time.time()  
    if release_time - start_time < 0.1:
        return  # debounce
    morse_events.append(('released', release_time))
    print(f" {release_time}")

# start/stop button
def handle_start_stop():
    global input_active,morse_events
    if input_active:
        led.off()
        print("Input stopped and decoded.")
        decode_and_print()
        input_active = False
    else:
        input_active = True
        morse_events.clear()
        led.on()
        print("Input started.")


# add event listeners
start_stop_button.when_activated = handle_start_stop
morse_input.when_activated = morse_input_pressed
morse_input.when_deactivated = morse_input_released



try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    pass






# decode and print
'''
To decode the Morse code message based on the button press times provided, we need to interpret the duration of each press. Typically, a short press (dot) is around 0.2 to 0.3 seconds, while a long press (dash) is about 0.5 seconds or longer. Let's analyze the press durations:

1. `1767773542.1257536` to `1767773542.285196` - Duration: ~0.16 seconds - Dot (.)
2. `1767773542.4936137` to `1767773542.6315389` - Duration: ~0.14 seconds - Dot (.)
3. `1767773542.9092748` to `1767773543.0543947` - Duration: ~0.15 seconds - Dot (.)
4. `1767773544.2299025` to `1767773544.5774245` - Duration: ~0.35 seconds - Dash (-)
5. `1767773545.1017563` to `1767773545.4954002` - Duration: ~0.39 seconds - Dash (-)
6. `1767773546.11932` to `1767773546.5881057` - Duration: ~0.47 seconds - Dash (-)
7. `1767773547.824543` to `1767773547.9534554` - Duration: ~0.13 seconds - Dot (.)
8. `1767773548.1879761` to `1767773548.2895174` - Duration: ~0.10 seconds - Dot (.)
9. `1767773548.5281847` to `1767773548.6453152` - Duration: ~0.12 seconds - Dot (.)

Now let's decode the sequence into letters using Morse code:

- `...` (Dot Dot Dot) = S
- `---` (Dash Dash Dash) = O
- `...` (Dot Dot Dot) = S

Putting it all together, the decoded message is "SOS".
'''