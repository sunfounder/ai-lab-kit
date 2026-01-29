from fusion_hat.llm import OpenAI
from secret import OPENAI_API_KEY
from fusion_hat.adc import ADC
from fusion_hat.pin import Pin
from fusion_hat.tts import Pico2Wave
import random,time



# Register OpenAI API
# openai.com

# Export your openai api key with :LLM_API_KEY
# export LLM_API_KEY=sk-xxxxxxxxxxxxxxxxx


# Setup TTS
tts = Pico2Wave()
tts.set_lang('en-US')


# Setup Joystick
btn_pin = Pin(17, mode=Pin.IN, pull=Pin.PULL_UP, bounce_time=0.05)
x_axis = ADC('A1')
y_axis = ADC('A0')

def MAP(x, in_min, in_max, out_min, out_max):
    """
    Map a value from one range to another.
    """
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def activate():
    global smash_tips
    smash_tips = True
        
btn_pin.when_activated = activate

# Setup LLM
INSTRUCTIONS = "This is a blindfolded watermelon-smashing game. A point representing a watermelon is randomly generated within a 20x20 meter area with coordinates ranging from (-10,-10) to (10,10). The player starts from the origin (0,0) and moves using a joystick. Even if the player can't see anything, they press a button to perform a smash action. After smashing, you will receive the watermelon's and player's coordinates. You need to advise the player on the direction of the watermelon, like 'The watermelon is ten meters to your northeast.' If the smash coordinates match, the game ends. Your responses will be converted into speech via TTS, so please keep them brief, ideally within two sentences."

WELCOME = "Hello, I am Blindfolded Watermelon Smashing Game Assistant. Use the joystick to move and press the button to smash. I will guide you to find the watermelon. Good luck!"

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


# Define the map size and the joystick pins
watermelon_x, watermelon_y = random.randint(-10, 10), random.randint(-10, 10)
player_x, player_y = 0, 0
smash_tips = False

while True:
    x_val = MAP(x_axis.read(), 0, 4095, -100, 100)
    y_val = MAP(y_axis.read(), 0, 4095, -100, 100)
    if x_val > 80:
        player_x += 1
    elif x_val < -80:
        player_x -= 1
    if y_val > 80:
        player_y -= 1
    elif y_val < -80:
        player_y += 1
    # print('Watermelon position: %d, %d  ' % (watermelon_x, watermelon_y))
    # print('Player position: %d, %d  ' % (player_x, player_y))

    time.sleep(0.3)

    if smash_tips:
        smash_tips = False
        print("Smash!")
        if (player_x, player_y) == (watermelon_x, watermelon_y):
            print("Target hit!")
            tts.say("Target hit!")
            break
        else:
            input_text = f"Watermelon position: ({watermelon_x}, {watermelon_y}), Player position: ({player_x}, {player_y})"
            # Response with stream
            response = llm.prompt(input_text, stream=True)
            string = ""
            for next_word in response:
                if next_word:
                    # print(next_word, end="", flush=True)
                    string += next_word
            # print("")
            print("AI: " + string)
            tts.say(string)
print("Game over!")