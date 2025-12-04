#!/usr/bin/env python3
import os
import time
import re
import base64
import threading
from pathlib import Path
from picamera2 import Picamera2, Preview
from fusion_hat.user_button import UserButton
from fusion_hat.modules import RGB_LED
from fusion_hat.pwm import PWM
from fusion_hat.llm import OpenAI
from fusion_hat.tts import OpenAI_TTS
from secret import OPENAI_API_KEY

class BookCoverAnalyzer:
    def __init__(self):
        # Initialize LED for status feedback
        self.rgb_led = RGB_LED(PWM(0), PWM(1), PWM(2), common=RGB_LED.CATHODE)
        self.set_led_color("blue")  # Ready state
        
        # Initialize OpenAI LLM for image analysis
        self.llm = OpenAI(
            api_key=OPENAI_API_KEY,
            model="gpt-4o",  # GPT-4o supports image input
        )
        
        # Initialize TTS for audio responses
        self.tts = OpenAI_TTS(api_key=OPENAI_API_KEY)
        self.tts.set_voice(self.tts.Voice.ALLOY)
        
        # Initialize camera
        self.camera = Picamera2()
        self.camera.configure(self.camera.create_preview_configuration(main={"size": (800, 600)}))
        
        # Initialize button
        self.btn = UserButton()
        
        # Set up directories
        self.real_user = os.getenv("SUDO_USER") or os.getlogin()
        self.user_home = f"/home/{self.real_user}"
        self.pictures_dir = Path(self.user_home) / "Pictures" / "book_covers"
        self.pictures_dir.mkdir(parents=True, exist_ok=True)
        
        # Threading locks
        self.photo_lock = threading.Lock()
        self.photo_index = 1
        
        # Set LLM instructions
        self.instructions = """You are a book expert. Analyze book covers that are sent to you.
        
        When you receive a book cover image, provide:
        1. Book title (if identifiable from cover)
        2. Author (if identifiable from cover)
        3. Brief summary of what the book is about (50 words)
        4. Overall rating/reception (e.g., "Highly acclaimed", "Classic", "Popular", etc.)
        
        Keep your response under 100 words total.
        Speak in a friendly, informative tone suitable for an audio response.
        
        If the image is not a book cover or is unclear, politely say you can't identify it and ask for another photo."""
        
        self.llm.set_max_messages(10)
        self.llm.set_instructions(self.instructions)
        
    def set_led_color(self, color_name):
        """Set RGB LED color for status feedback"""
        color_map = {
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255),
            "yellow": (255, 255, 0),
            "purple": (255, 0, 255),
            "white": (255, 255, 255),
            "off": (0, 0, 0),
        }
        
        if color_name in color_map:
            self.rgb_led.color(color_map[color_name])
    
    def encode_image(self, image_path):
        """Encode image to base64 for OpenAI API"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def capture_photo(self):
        """Capture a photo and return the filepath"""
        with self.photo_lock:
            filepath = self.pictures_dir / f"book_cover_{self.photo_index:03d}.jpg"
            print(f"\n📸 Capturing photo: {filepath}")
            
            # LED feedback: yellow for capturing
            self.set_led_color("yellow")
            
            # Capture image
            self.camera.capture_file(str(filepath))
            
            # Increment counter for next photo
            self.photo_index += 1
            
            print("✅ Photo captured successfully")
            return str(filepath)
    
    def analyze_book_cover(self, image_path):
        """Send book cover image to OpenAI for analysis"""
        print("\n🤔 Analyzing book cover...")
        
        # LED feedback: purple for processing
        self.set_led_color("purple")
        
        try:
            # Encode the image
            base64_image = self.encode_image(image_path)
            
            # Prepare messages for OpenAI with image
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Please analyze this book cover and tell me about the book in under 100 words."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
            
            # Get analysis from OpenAI
            print("🔄 Sending to AI for analysis...")
            response = self.llm._openai.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=150  # Limit response length
            )
            
            analysis = response.choices[0].message.content
            print(f"\n📚 Analysis:\n{analysis}")
            
            # LED feedback: green for success
            self.set_led_color("green")
            
            return analysis
            
        except Exception as e:
            print(f"❌ Error analyzing image: {e}")
            # LED feedback: red for error
            self.set_led_color("red")
            return f"Sorry, I couldn't analyze the book cover. Error: {str(e)}"
    
    def speak_response(self, text):
        """Convert text to speech"""
        print("\n🔊 Speaking response...")
        
        # Clean up text for TTS (remove markdown, etc.)
        clean_text = re.sub(r'[*_\[\]()#]', '', text)
        
        # Speak with friendly instructions
        self.tts.say(clean_text, instructions="speak clearly and warmly")
        print("✅ Response spoken")
        
        # Return to ready state
        self.set_led_color("blue")
    
    def button_handler(self):
        """Handle button press: capture photo, analyze, and speak"""
        print("\n" + "="*50)
        print("🔄 Processing request...")
        
        # Step 1: Capture photo
        try:
            image_path = self.capture_photo()
        except Exception as e:
            print(f"❌ Failed to capture photo: {e}")
            self.set_led_color("red")
            self.tts.say("Sorry, I couldn't take a photo. Please try again.")
            self.set_led_color("blue")
            return
        
        # Step 2: Analyze with AI
        analysis = self.analyze_book_cover(image_path)
        
        # Step 3: Speak the analysis
        self.speak_response(analysis)
        
        print(f"✅ Complete! Photo saved at: {image_path}")
        print("="*50 + "\n")
    
    def run(self):
        """Main program loop"""
        # Set button callback
        self.btn.set_on_click(self.button_handler)
        
        # Start camera preview
        print("📷 Starting camera preview...")
        self.camera.start_preview(Preview.QT)
        self.camera.start()
        
        # LED feedback: blue for ready
        self.set_led_color("blue")
        
        print("\n" + "="*50)
        print("BOOK COVER ANALYZER")
        print("="*50)
        print("\nReady to analyze book covers!")
        print("Press the USR button to capture and analyze a book cover")
        print("I will speak the analysis aloud")
        print("LED colors:")
        print("   🔵 Blue: Ready")
        print("   🟡 Yellow: Capturing photo")
        print("   🟣 Purple: Analyzing with AI")
        print("   🟢 Green: Analysis successful")
        print("   🔴 Red: Error occurred")
        print(f"Photos saved to: {self.pictures_dir}")
        print("Press Ctrl+C to exit")
        print("="*50 + "\n")
        
        try:
            # Keep program running
            while True:
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            
        finally:
            # Cleanup
            self.camera.stop_preview()
            self.camera.close()
            self.set_led_color("off")
            print("✅ Cleanup complete")

if __name__ == "__main__":
    analyzer = BookCoverAnalyzer()
    analyzer.run()