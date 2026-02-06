from fusion_hat.stt import Vosk as STT

stt = STT(language="en-us")

try:
    while True:
        print("Say something")
        for result in stt.listen(stream=True):
            if result["done"]:
                print(f"\r\x1b[Kfinal: {result['final']}")
            else:
                print(f"\r\x1b[Kpartial: {result['partial']}", end="", flush=True)

except KeyboardInterrupt:
    # Clean exit on Ctrl+C (do not print a traceback)
    print("\nExiting...")

finally:
    # If the STT class provides a cleanup method, call it here.
    # For example: stt.close() or stt.stop()
    pass
