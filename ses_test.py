import pyttsx3

motor = pyttsx3.init()
sesler = motor.getProperty('voices')

print("BİLGİSAYARDAKİ SESLER:\n" + "-"*30)
for ses in sesler:
    print(f"İsim: {ses.name}")
    print(f"ID: {ses.id}\n")