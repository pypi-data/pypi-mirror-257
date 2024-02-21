from colorism import FG, BG

def test():
    # FG._palette
    # FG._rainbow_palette
    # FG._color_legend

    BG._palette
    BG._rainbow_palette
    BG._color_legend

    print(FG.Aquamarine2, "hellooo", FG.RESET)
    print(FG.num2escape(78), "hellooo", FG.RESET)

    print(FG.blink(f"{FG.SeaGreen3}hellooooooooooo{FG.RESET}"))
    print(FG.underline("hellooooooooooo"))
    print(FG.bold("hellooooooooooo"))
    print(FG.dim("hellooooooooooo"))
    print(FG.italic("hellooooooooooo"))
    print(FG.invert("hellooooooooooo"))
    print(FG.hidden("hellooooooooooo"))
    print(FG.strikethrough("hellooooooooooo"))

    print(f"{FG.BOLD + FG.UNDERLINE + FG.GREEN + BG.rgb2escape(0, 255, 255)} Hello World {FG.RESET_ALL} hellooo")
    print(f"{FG.hsl2escape(60, 100, 25) + BG.rgb2escape(255, 255, 255)} Hello World {FG.RESET + BG.RESET}")
    print("\x1b[5;31m # Set style to bold, red foreground.")
    print("\x1b[5;32m # Set style to bold, green foreground.")
    print("\x1b[5;33m # Set style to bold, yellow foreground.")
    print("\x1b[4;33m # Set style to underline, yellow foreground.\x1b[0m")
    
if __name__ == "__main__":
    test()