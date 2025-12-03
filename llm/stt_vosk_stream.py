from sunfounder_voice_assistant.stt import STT

stt = STT(language="en-us")

while True:
    print("Say something")
    for result in stt.listen(stream=True):
        if result["done"]:
            print(f"\r\x1b[Kfinal: {result['final']}")
        else:
            print(f"\r\x1b[Kpartial: {result['partial']}", end="", flush=True)
