import winsound as sd
def beefsound():
    fr = 2000 # range = 37 ~ 32767
    du = 1000 # 1000 ms = 1 second
    sd.Beep(fr,du)
