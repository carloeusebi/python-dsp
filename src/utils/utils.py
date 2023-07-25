import os


def clearscreen():
    os.system("cls" if os.name in ("nt", "dos") else "clear")


def die(output=""):
    if output:
        print(output)
    input("Premi un tasto per uscire")
    exit()


def test_passed():
    """
    Utility to escape the a while True while testing
    """
    return False
