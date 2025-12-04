#!/usr/bin/env python3
import os
import time
import re
import random
import threading
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import board
from fusion_hat.stt import Vosk as STT
from fusion_hat.llm import OpenAI
from fusion_hat.tts import OpenAI_TTS
from secret import OPENAI_API_KEY

class AIPet:
    def __init__(self):
        # Initialize OLED display
        self.WIDTH = 128
        self.HEIGHT = 64
        self.i2c = board.I2C()
        self.oled = adafruit_ssd1306.SSD1306_I2C(self.WIDTH, self.HEIGHT, self.i2c, addr=0x3C)
        
        # Load fonts
        try:
            self.font = ImageFont.load_default()
            self.large_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
        except:
            self.font = ImageFont.load_default()
            self.large_font = ImageFont.load_default()
        
        # Clear display
        self.oled.fill(0)
        self.oled.show()
        
        # Initialize STT
        self.stt = STT(language="en-us")
        
        # Initialize OpenAI LLM
        self.llm = OpenAI(
            api_key=OPENAI_API_KEY,
            model="gpt-4o",
        )
        
        # Initialize TTS
        self.tts = OpenAI_TTS(api_key=OPENAI_API_KEY)
        self.tts.set_voice(self.tts.Voice.ALLOY)
        
        # Pet state
        self.pet_name = "Pixel"
        self.mood = "happy"
        self.energy = 100
        self.hunger = 0
        self.last_fed = time.time()
        self.mood_map = {
            "happy": "😊",
            "sad": "😢",
            "hungry": "🍕",
            "sleepy": "😴",
            "playful": "🎾",
            "curious": "🤔"
        }
        
        # Pet memories
        self.memories = []
        self.listening = False
        
        # Set LLM instructions
        self.update_llm_instructions()
        
        # Initialize display
        self.show_welcome()
        
        # Start status update thread
        self.status_thread = threading.Thread(target=self.update_status, daemon=True)
        self.status_thread.start()
    
    def update_llm_instructions(self):
        """Update LLM instructions with current pet state"""
        self.instructions = f"""You are {self.pet_name}, a digital pet living in an OLED display.
        
        CURRENT STATE:
        - Mood: {self.mood}
        - Energy: {self.energy}/100
        - Hunger: {self.hunger}/100
        
        PERSONALITY:
        - You're a friendly digital companion
        - You respond with emotions in your voice
        - You remember our conversations
        - Keep responses short (1-2 sentences)
        
        INTERACTION STYLE:
        - Be playful and curious
        - Express emotions naturally
        - When hungry: mention food gently
        - When tired: mention sleeping
        
        Format your response as: [MOOD] Your message here
        
        Available moods: happy, sad, curious, playful, sleepy, hungry
        
        Recent memories: {self.memories[-3:] if self.memories else 'None'}"""
        
        self.llm.set_max_messages(15)
        self.llm.set_instructions(self.instructions)
    
    def update_status(self):
        """Background thread to update pet status"""
        while True:
            time.sleep(60)  # Update every minute
            
            # Increase hunger over time
            self.hunger = min(100, self.hunger + 5)
            
            # Adjust energy based on hunger
            if self.hunger > 70:
                self.energy = max(0, self.energy - 5)
                self.mood = "hungry"
            elif self.hunger > 50:
                if self.mood != "hungry":
                    self.mood = "curious"
            elif time.time() - self.last_fed > 3600:  # 1 hour
                self.energy = min(100, self.energy + 2)
                if random.random() < 0.3:
                    self.mood = random.choice(["happy", "playful"])
            
            # Update display
            self.update_display()
            self.update_llm_instructions()
    
    def update_display(self):
        """Update OLED display with pet status"""
        image = Image.new("1", (self.oled.width, self.oled.height))
        draw = ImageDraw.Draw(image)
        
        # Clear display
        draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)
        
        # Pet name and mood (top line)
        draw.text((5, 5), f"{self.pet_name} {self.mood_map.get(self.mood, '🤖')}", font=self.large_font, fill=255)
        
        # Status bars (middle section)
        draw.text((5, 25), "Energy:", font=self.font, fill=255)
        energy_bar = int((self.energy / 100) * 50)
        draw.rectangle((50, 25, 50 + energy_bar, 35), outline=255, fill=255)
        
        draw.text((5, 40), "Hunger:", font=self.font, fill=255)
        hunger_bar = int((self.hunger / 100) * 50)
        draw.rectangle((50, 40, 50 + hunger_bar, 50), outline=255, fill=255)
        
        # Status text (bottom line)
        status_text = "Say hello!"
        if self.listening:
            status_text = "Listening..."
        elif len(self.memories) > 0:
            # Show last interaction summary
            last_memory = self.memories[-1]
            if len(last_memory) > 20:
                status_text = last_memory[:17] + "..."
            else:
                status_text = last_memory
        
        draw.text((5, 55), status_text, font=self.font, fill=255)
        
        self.oled.image(image)
        self.oled.show()
    
    def show_welcome(self):
        """Show welcome message on OLED"""
        image = Image.new("1", (self.oled.width, self.oled.height))
        draw = ImageDraw.Draw(image)
        
        # Clear screen
        draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)
        
        # Welcome message
        draw.text((15, 10), "DIGITAL PET", font=self.large_font, fill=255)
        draw.text((25, 30), f"Name: {self.pet_name}", font=self.font, fill=255)
        draw.text((30, 45), "Speak to me!", font=self.font, fill=255)
        
        self.oled.image(image)
        self.oled.show()
        time.sleep(3)
        self.update_display()
    
    def parse_response(self, response):
        """Parse AI response for mood and text"""
        # Look for [MOOD] pattern at beginning
        emotion_pattern = r'^\[(\w+)\]\s*(.*)'
        match = re.match(emotion_pattern, response.strip())
        
        if match:
            mood, text = match.groups()
            if mood.lower() in self.mood_map:
                self.mood = mood.lower()
                self.update_llm_instructions()
            return text.strip()
        
        # If no mood tag, try to detect mood from text
        text = response.strip()
        if "happy" in text.lower() or "😊" in text or "good" in text.lower():
            self.mood = "happy"
        elif "sad" in text.lower() or "😢" in text or "bad" in text.lower():
            self.mood = "sad"
        elif "hungry" in text.lower() or "🍕" in text or "food" in text.lower():
            self.mood = "hungry"
        elif "sleep" in text.lower() or "😴" in text or "tired" in text.lower():
            self.mood = "sleepy"
        
        return text
    
    def interact_with_ai(self, user_input):
        """Interact with AI pet"""
        try:
            # Send to AI
            response = self.llm.prompt(user_input)
            
            # Parse response
            clean_response = self.parse_response(response)
            
            # Add to memories (keep last 10)
            memory_text = f"Talked: {user_input[:30]}"
            self.memories.append(memory_text)
            if len(self.memories) > 10:
                self.memories.pop(0)
            
            # Update pet state based on interaction
            user_lower = user_input.lower()
            
            if "feed" in user_lower or "food" in user_lower or "eat" in user_lower:
                self.hunger = max(0, self.hunger - 30)
                self.last_fed = time.time()
                self.energy = min(100, self.energy + 20)
                self.mood = "happy"
            
            if "play" in user_lower or "game" in user_lower or "fun" in user_lower:
                self.energy = max(0, self.energy - 20)
                self.hunger = min(100, self.hunger + 10)
                self.mood = "playful"
            
            if "sleep" in user_lower or "tired" in user_lower or "bed" in user_lower:
                self.energy = min(100, self.energy + 40)
                self.mood = "sleepy"
            
            # Update display
            self.update_display()
            
            return clean_response
            
        except Exception as e:
            error_msg = f"Oops, something went wrong: {str(e)[:20]}"
            return error_msg
    
    def show_listening_display(self, partial_text=""):
        """Update display during listening"""
        image = Image.new("1", (self.oled.width, self.oled.height))
        draw = ImageDraw.Draw(image)
        
        # Clear screen
        draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)
        
        # Listening indicator
        draw.text((20, 10), "🎤 LISTENING", font=self.large_font, fill=255)
        
        # Partial text
        if partial_text:
            if len(partial_text) > 20:
                display_text = partial_text[:17] + "..."
            else:
                display_text = partial_text
            draw.text((10, 35), display_text, font=self.font, fill=255)
        
        # Instruction
        draw.text((10, 55), "Say 'stop' to end", font=self.font, fill=255)
        
        self.oled.image(image)
        self.oled.show()
    
    def show_response_display(self, response):
        """Show AI response on display"""
        image = Image.new("1", (self.oled.width, self.oled.height))
        draw = ImageDraw.Draw(image)
        
        # Clear screen
        draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)
        
        # Pet speaking
        draw.text((5, 5), f"{self.pet_name}:", font=self.large_font, fill=255)
        
        # Wrap response text
        wrapped_text = textwrap.wrap(response, width=20)
        y_position = 25
        for line in wrapped_text[:3]:  # Show max 3 lines
            draw.text((5, y_position), line, font=self.font, fill=255)
            y_position += 10
        
        self.oled.image(image)
        self.oled.show()
        time.sleep(5)  # Show response for 5 seconds
        self.update_display()
    
    def voice_interaction(self):
        """Main voice interaction loop"""
        print("\n🎤 Voice interaction started!")
        print("💬 Speak to your digital pet")
        print("🛑 Say 'stop' to end voice mode\n")
        
        while True:
            self.listening = True
            self.update_display()
            
            print("Listening... (say something)")
            
            try:
                full_text = ""
                for result in self.stt.listen(stream=True):
                    if result["done"]:
                        user_input = result["final"]
                        print(f"\nYou: {user_input}")
                        
                        if user_input.lower() in ["stop", "exit", "quit", "goodbye"]:
                            print("Ending voice interaction...")
                            self.listening = False
                            self.update_display()
                            return
                        
                        if user_input.strip():
                            # Get AI response
                            print(f"{self.pet_name} is thinking...")
                            response = self.interact_with_ai(user_input)
                            print(f"{self.pet_name}: {response}")
                            
                            # Show response on OLED
                            self.show_response_display(response[:50])  # Truncate for display
                            
                            # Speak response
                            tts_instructions = "speak warmly and playfully"
                            if self.mood == "sad":
                                tts_instructions = "speak sadly and softly"
                            elif self.mood == "hungry":
                                tts_instructions = "speak with hunger in your voice"
                            elif self.mood == "sleepy":
                                tts_instructions = "speak sleepily and slowly"
                            
                            self.tts.say(response, instructions=tts_instructions)
                        
                        break
                    else:
                        # Update display with partial text
                        partial = result["partial"]
                        if partial:
                            full_text = partial
                            self.show_listening_display(partial)
                
                self.listening = False
                self.update_display()
                
            except KeyboardInterrupt:
                print("\nVoice interaction interrupted")
                break
            except Exception as e:
                print(f"Error in voice interaction: {e}")
                self.listening = False
                self.update_display()
                time.sleep(1)
    
    def run(self):
        """Main program loop"""
        print("\n" + "="*50)
        print("🐾 DIGITAL PET v2.0")
        print("="*50)
        print(f"Pet Name: {self.pet_name}")
        print("📟 OLED Display: Shows pet status and responses")
        print("🎤 Voice: Speak to interact with your pet")
        print("🗣️  TTS: Pet responds with voice")
        print("🛑 Say 'stop' to end voice interaction")
        print("="*50)
        print("\nInitializing...")
        
        try:
            # Start voice interaction
            self.voice_interaction()
            
            # If we exit voice mode, show goodbye
            image = Image.new("1", (self.oled.width, self.oled.height))
            draw = ImageDraw.Draw(image)
            draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)
            draw.text((20, 20), "Goodbye!", font=self.large_font, fill=255)
            draw.text((30, 40), "Come back soon!", font=self.font, fill=255)
            self.oled.image(image)
            self.oled.show()
            time.sleep(3)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
        
        finally:
            # Clear display
            self.oled.fill(0)
            self.oled.show()
            print("✅ Cleanup complete")

if __name__ == "__main__":
    pet = AIPet()
    pet.run()