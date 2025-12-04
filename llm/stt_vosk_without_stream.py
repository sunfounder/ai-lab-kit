from fusion_hat.stt import STT

stt = STT(language="en-us")

while True:
    print("Say something")
    result = stt.listen(stream=False)
    print(result)