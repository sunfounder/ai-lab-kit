from fusion_hat.llm import OpenAI
from secret import OPENAI_API_KEY
from fusion_hat.motor import Motor
from fusion_hat.modules import Buzzer
from fusion_hat.pin import Pin
import random,time
from fusion_hat.stt import STT

stt = STT(language="en-us")

motor = Motor('M0')
button = Pin(17, mode=Pin.IN, pull=Pin.PULL_UP, bounce_time=0.05)
buzzer = Buzzer(Pin(4))
speed = 0

def beep():
    buzzer.on()
    time.sleep(0.1)
    buzzer.off()

last_triggered = 0 

def speed_up():
    global speed,last_triggered
    if time.time() - last_triggered < 0.5:  # 500ms debounce
        return
    last_triggered = time.time()
    speed += 10
    beep()
    if speed > 100:
        motor.stop()
        speed = 0
    else:
        motor.power(speed)
    print(f"Speed set to: {speed}%")

button.when_activated = speed_up

# Function to parse natural language response and set appropriate speed
def parse_response_for_speed(text_response):
    """
    Parse the LLM's natural language response to determine speed setting.
    Looks for keywords related to different speed levels.
    Returns the speed level to set (100, 50, 25, or 0)
    """
    text_lower = text_response.lower()
    

    
    # Check for "slow" or "low" keywords
    if any(word in text_lower for word in ['slow', 'low', '25%', 'quarter', 'minimum', 'gentle']):
        return 25
    
    # Check for "medium" or "half" keywords
    if any(word in text_lower for word in ['medium', 'half', '50%', 'moderate', 'normal']):
        return 50
    
    # Check for "fast" or "high" or "full" keywords
    if any(word in text_lower for word in ['fast', 'high', 'full', '100%', 'maximum']):
        return 100

    # Check for "stop" or "off" keywords - highest priority
    if any(word in text_lower for word in ['stop', 'off', 'zero', ' 0%', 'turn off', 'shut off', 'halt']):
        return 0

    # If no specific keywords found, return -1 to indicate no speed change
    return -1

# Setup LLM
INSTRUCTIONS = '''
You are a fan control assistant. Your task is to interpret the user's speech input and respond with natural language.

### Input Format:
The user will speak their command for fan control.

### CRITICAL RULES:
1. **BE DECISIVE**: Always take clear action based on user requests. Do NOT ask follow-up questions.
2. **NO CLARIFICATION QUESTIONS**: Never ask "Would you like me to..." or "Should I..." questions.
3. **ASSUME INTENT**: If the user's request is ambiguous, make a reasonable assumption and take action.
4. **CONFIRM ACTION**: Always state what action you are taking in your respons

### Response Guidelines:
1. Respond naturally and conversationally to the user's request.
2. Acknowledge what the user asked for.
3. Use clear language about what action you're taking.
4. Use keywords in your response that indicate speed levels:
   - For maximum speed: use words like "fast", "high", "full speed", "maximum"
   - For medium speed: use words like "medium", "half speed", "50%"
   - For low speed: use words like "slow", "low", "quarter speed", "25%"
   - For stopping: use words like "stop", "off", "zero", "turning off"
5. If the user asks about current status, respond with helpful information.



### Example Responses:

**When asked to go fast:**
"I'll set the fan to maximum speed for you. Full speed activated!"

**When asked to slow down:**
"Reducing the fan speed to low. Enjoy the gentle breeze."

**When asked for medium speed:**
"Setting the fan to medium speed. This should be comfortable."

**When asked to stop:**
"Stopping the fan now. The motor is turned off."

**When asked about status:**
"Your fan is currently at 50% speed. Would you like me to adjust it?"

'''

WELCOME = "Hello, I am a fan control assistant. You can ask me to set the fan to fast, medium, slow, or stop it completely. You can also press the button to increase the speed by 10% or decrease it by 10%. If you ask about the current status, I will tell you the current speed. If you don't know what to do, you can ask me for instructions. Good luck!"

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

def main():

    while True:
        print("Say something")
        for result in stt.listen(stream=True):
            if result["done"]:
                print(f"\r\x1b[Kfinal: {result['final']}")
                input_text = result['final']
                
                # Add current speed context to the input
                contextual_input = f"Current speed is {speed}%. User says: {input_text}"
                
                # Response with stream
                response = llm.prompt(contextual_input, stream=True)
                
                # Collect the full response
                full_response = ""
                for next_word in response:
                    if next_word:
                        print(next_word, end="", flush=True)
                        full_response += next_word
                
                print("\n")  # Add newline after response
                
                # Parse the response to determine speed setting
                new_speed = parse_response_for_speed(full_response)
                
                # Apply speed change if detected
                if new_speed >= 0:
                    speed = new_speed
                    motor.power(speed)
                    print(f"Speed set to: {speed}%")
                else:
                    print("No speed change detected in response")
                    
            else:
                print(f"\r\x1b[Kpartial: {result['partial']}", end="", flush=True)
try:
    main()
except KeyboardInterrupt:
    # Stop the motor when the script is interrupted
    motor.power(0)
while True:
    print("Say something")
    for result in stt.listen(stream=True):
        if result["done"]:
            print(f"\r\x1b[Kfinal: {result['final']}")
            input_text = result['final']
            
            # Add current speed context to the input
            contextual_input = f"Current speed is {speed}%. User says: {input_text}"
            
            # Response with stream
            response = llm.prompt(contextual_input, stream=True)
            
            # Collect the full response
            full_response = ""
            for next_word in response:
                if next_word:
                    print(next_word, end="", flush=True)
                    full_response += next_word
            
            print("\n")  # Add newline after response
            
            # Parse the response to determine speed setting
            new_speed = parse_response_for_speed(full_response)
            
            # Apply speed change if detected
            if new_speed >= 0:
                speed = new_speed
                motor.power(speed)
                print(f"Speed set to: {speed}%")
            else:
                print("No speed change detected in response")
                
        else:
            print(f"\r\x1b[Kpartial: {result['partial']}", end="", flush=True)
