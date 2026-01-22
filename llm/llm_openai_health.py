from fusion_hat.llm import OpenAI
from secret import OPENAI_API_KEY
import time
from fusion_hat.stt import STT
from fusion_hat.adc import ADC
import math
from fusion_hat.tts import Pico2Wave

# setup tts & stt
tts = Pico2Wave()
tts.set_lang('en-US')
stt = STT(language="en-us")


# Register OpenAI API
# openai.com

# Export your openai api key with :LLM_API_KEY
# export LLM_API_KEY=sk-xxxxxxxxxxxxxxxxx


# setup ADC for thermistor reading
thermistor = ADC('A3')

# Setup LLM
INSTRUCTIONS = '''
You are a health assistant. Your task is to assess the user's body temperature based on the thermistor reading and provide appropriate health advice.

The thermistor reading represents body temperature in Celsius.

### Input Format:
"thermistor: [value], message: [user query]"

### Output Guidelines:
1. If temperature < 35.0°C, warn about hypothermia and suggest warming up.
2. If 35.0°C ≤ temperature ≤ 37.5°C, confirm normal temperature and reassure the user.
3. If 37.5°C < temperature ≤ 38.5°C, indicate mild fever and suggest rest and hydration.
4. If temperature > 38.5°C, alert about high fever and recommend medical attention.
5. Include the temperature value in your response to justify your assessment.
6. Your reply should be brief and concise, no more than two sentences.

### Example Input:
thermistor: 39.0, message: I feel unwell.

### Example Output:
Your body temperature is 39.0°C, which indicates a high fever. Please rest, stay hydrated, and consider seeking medical advice if symptoms persist.
'''

WELCOME = "Hello, I am a health assistant. Please hold your thermometer and I will assess your body temperature based on the thermistor reading. If you feel unwell, please provide your symptoms and I will provide appropriate health advice."

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

def temperature():
    while True:
        analogVal = thermistor.read()
        Vr = 3.3 * float(analogVal) / 4095
        if 3.3 - Vr < 0.1:
            print("Please check the sensor")
            continue
        Rt = 10000 * Vr / (3.3 - Vr)
        temp = 1 / (((math.log(Rt / 10000)) / 3950) + (1 / (273.15 + 25)))
        Cel = temp - 273.15
        return Cel


while True:
    print("Say something")
    for result in stt.listen(stream=True):
        if result["done"]:
            print(f"\r\x1b[Kfinal: {result['final']}")
            #input_text = result['final']
            input_text = f"thermistor: {temperature()}, message: {result['final']}"
            # Response with stream
            response = llm.prompt(input_text, stream=True)
            string = ""
            for next_word in response:
                if next_word:
                    print(next_word, end="", flush=True)
                    string += next_word
            tts.say(string)
            print("")

        else:
            print(f"\r\x1b[Kpartial: {result['partial']}", end="", flush=True)

