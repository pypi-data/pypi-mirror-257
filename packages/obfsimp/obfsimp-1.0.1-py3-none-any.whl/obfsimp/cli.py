from obfsimp import Obfuscator
import sys


def yesno(prompt):
    inp = input(prompt + " (y/n) ")
    while inp not in list("yYnN"):
        inp = input(prompt + " (y/n) ")
    return inp.lower() == "y"


def _cli():
    print("Welcome to the obfsimp Python obfuscator!")
    fn = input("Input file name you want to obfuscate: ")
    options = {}
    try:
        with open(fn, "r", encoding="utf-8") as f:
            code = f.read()
    except BaseException as e:
        print("Cannot read file, error is: " + str(e))
        sys.exit()
    if yesno("Do you want to remove comments and docstrings?"):
        options["remove_comments"] = True
    if yesno("Do you want to wrap the program in an exec expression?"):
        options["exec"] = True
        enc = input(
            "What encryption do you want to use? ((n)o/(b)ase64/base64-(l)zma/(e)scape) "
        )
        while enc.lower() not in [
            "n",
            "b",
            "l",
            "e",
            "no",
            "base64",
            "base64-lzma",
            "escape",
        ]:
            enc = input(
                "What encryption do you want to use? ((n)o/(b)ase64/base64-(l)zma/(e)scape) "
            )
        enc = enc.lower()
        if enc != "n" and enc != "no":
            if enc == "b":
                enc = "base64"
            if enc == "l":
                enc = "base64-lzma"
            if enc == "e":
                enc = "escape"
            options["exec_crypt"] = enc
    if yesno("Do you want the program to ignore errors?"):
        options["error_free"] = True
    if yesno("Do you want to obfuscate variable names?"):
        options["rename_variables"] = True
        renamer = input(
            "What renamer do you want to use? ((h)ex/(o)0/(l)1/(u)nderscore/(c)har) default is hex "
        )
        if renamer.lower() not in [
            "h",
            "o",
            "l",
            "u",
            "c",
            "hex",
            "o0",
            "l1",
            "underscore",
            "char",
        ]:
            renamer = "hex"
        renamer = renamer.lower()
        if renamer == "h":
            renamer = "hex"
        if renamer == "l":
            renamer = "l1"
        if renamer == "o":
            renamer = "o0"
        if renamer == "u":
            renamer = "underscore"
        if renamer == "c":
            renamer = "char"
        options["renamer"] = renamer
        inp = input(
            "Do you want to export some names? separate them with spaces (If you don't want just input nothing) "
        ).split()
        options["exports"] = inp
    if yesno("Do you want to obfuscate strings?"):
        options["string_obf"] = True
        if yesno("Do you want to add random strings?"):
            options["random_strings"] = True
        enc = input(
            "What encryption do you want to use? ((n)o/(b)ase64/base64-(l)zma) "
        )
        while enc.lower() not in ["n", "b", "l", "no", "base64", "base64-lzma"]:
            enc = input(
                "What encryption do you want to use? ((n)o/(b)ase64/base64-(l)zma) "
            )
        enc = enc.lower()
        if enc != "n" and enc != "no":
            if enc == "b":
                enc = "base64"
            if enc == "l":
                enc = "base64-lzma"
            if enc == "e":
                enc = "escape"
            options["encrypt"] = enc
    if yesno("Do you want to add junk code?"):
        options["add_code"] = True
        num = input("How much junk code do you want to add? default is 10 ")
        if not num.isdigit():
            num = 10
        else:
            num = int(num)
        options["code_amount"] = num
    if yesno(
        "Do you want to convert code to code that only uses magic functions? (Only suitable for small programs)"
    ):
        options["magic"] = True
    print("Start obfuscating...")
    o = Obfuscator(**options)
    obfuscated = o(code)
    print("Done!")
    fn = input("Output file name: ")
    try:
        with open(fn, "w", encoding="utf-8") as f:
            f.write(obfuscated)
    except BaseException as e:
        print("Cannot write file, error is: " + str(e))
        sys.exit()
    print("That's it! obfuscated code has been successfully written to " + fn)
