import os


def clearscreen():
    os.system("cls" if os.name in ("nt", "dos") else "clear")


def die(output=""):
    if output:
        print(output)
    input("Premi un tasto per uscire")
    exit()
