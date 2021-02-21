"""
This module contains functions, which
help user to navigate and search data in
.json file.
"""


import blessed
import json
import pprint


def read_json(path: str) -> object:
    """
    This function reads a .json file and returns
    python objects(dict, str, etc).
    """
    if path[-5:] != ".json":
        return error_screen() 
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return search(data, False)
    except FileNotFoundError:
        return error_screen()


def search(data: object, par: bool) -> str:
    """
    This function will define type of object,
    and depending of type will call function
    variant_screen().
    """
    if (not isinstance(data, dict)
    and (not isinstance(data, list))
    and (not isinstance(data, str))
    and (not isinstance(data, int))
    and (not isinstance(data, float))
    and (not isinstance(data, bool))
    and (not isinstance(data, tuple))):
        return error_screen()
    if par:
        try:
            parents.pop()
            parents.pop()
        except:
            pass
    parents.append(data)
    if isinstance(data, dict):
        return variant_screen("dict", list(data.keys()), data, parents)
    elif isinstance(data, list):
        return variant_screen("list", data, "", parents)
    elif isinstance(data, str):
        return variant_screen("string", data, "", parents)


def start_screen() -> str:
    """
    This function prints greetings screen.
    """
    term = blessed.Terminal()
    print(term.clear + term.move_y(term.height // 3) + term.center(f"H\
ello, this program will help you to navigate in your{term.green} .jso\
n {term.normal}file. Please, type path to your{term.green} .js\
on {term.normal}file:"))
    while True:
        path = input()
        return read_json(path)


def variant_screen(obj: str, variants: list, data: object, parents: list) -> str:
    """
    This function will interact with user and
    make another actions depending of user's choice.
    """
    term = blessed.Terminal()
    if obj == "dict":
        print(term.clear + term.move_y(term.height//3) + term.center(f"Pl\
ease, type {term.magenta}index{term.normal} of interesting element in lis\
t of keys, or {term.red}'Q'{term.normal}+ENTER to quit"))
        print()
        print(variants)
        print(term.center("First element has index 1."))
        while True:
            try:
                key = input()
                key = int(key)
            except:
                if key == "Q" or key == "q":
                    print(term.clear)
                    return
                continue
            if (isinstance(key, int) and (key < len(variants)+1)
            and key > -1):
                print(term.clear + term.move_y(term.height//3))
                print(term.center(f"You chose '{variants[key-1]}'. Typ\
e {term.green}'D'{term.normal}+ENTER to go deepe\
r, {term.orange}'P'{term.normal}+ENTER for previous step, o\
r {term.cyan}'S'{term.normal}+ENTER to print all options"))
                key_0 = input()
                if key_0 == "D" or key_0 == "d":
                    return search(data[variants[key-1]], False)
                elif key_0 == "S" or key_0 == "s":
                    print(term.clear)
                    pprint.pprint(data)
                    print(term.center(f"Type {term.blue}'X'{term.normal}+\
ENTER to restart, {term.red}'Q' {term.normal}to quit, o\
r {term.orange}'P'{term.normal}+ENTER for previous step."))
                    while True:
                        key = input()
                        if key == "X" or key == "x":
                            parents = []
                            return start_screen()
                        elif key == "Q" or key == "q":
                            print(term.clear)
                            return
                        elif key == "P" or key == "p":
                            return search(variants, False)
                elif key_0 == "Q" or key_0 == "q":
                    print(term.clear)
                    return
                elif key_0 == "P" or key_0 == "p":
                    try:
                        return search(parents[-2], True)
                    except IndexError:
                        return search(parents[-1], True)
                else:
                    continue
            else:
                continue
    elif obj == "list":
        if len(variants) == 1 and isinstance(variants[0], dict):
            return search(variants[0], False)
        elif len(variants) == 1 and isinstance(variants[0], list):
            return variant_screen("list", variants[0], "", parents)
        else:
            lst = []
            for item in variants:
                if isinstance(item, dict):
                    lst.append("dict")
                else:
                    lst.append(item)
        print(term.clear + term.move_y(term.height//3) + term.center(f"Ple\
ase, type {term.magenta}index{term.normal} of interesting element in list o\
f keys, or {term.red}'Q'{term.normal}+ENTER to quit"))
        print()
        print(lst)
        print(term.center(f"First element has index 1. Lenght of list of op\
tions is {len(lst)}"))
        while True:
            try:
                key = input()
                key = int(key)
            except:
                if key == "Q" or key == "q":
                    return
                continue
            if (isinstance(key, int) and (key < len(lst)+1)
            and key > -1):
                print(term.clear + term.move_y(term.height//3))
                print(term.center(f"You chose '{lst[key-1]}'. Ty\
pe {term.green}'D'{term.normal}+ENTER to go deepe\
r, {term.orange}'P'{term.normal}+ENTER to go to previous step,o\
r {term.cyan}'S'{term.normal}+ENTER to print all options"))
                key_0 = input()
                if key_0 == "D" or key_0 == "d":
                    return search(variants[key-1], False)
                elif key_0 == "S" or key_0 == "s":
                    print(term.clear + term.move_y(term.height//3))
                    pprint.pprint(variants)
                    print(term.center(f"Type {term.blue}'X'{term.normal}+\
ENTER to restart, {term.red}'Q' {term.normal}to quit, or {term.purple}'P\
'{term.normal}+ENTER for previous step."))
                    while True:
                        key = input()
                        if key == "X" or key == "x":
                            parents = []
                            return start_screen()
                        elif key == "Q" or key == "q":
                            print(term.clear)
                            return
                        elif key == "P" or key == "p":
                            return search(variants, False)
                elif key_0 == "Q" or key_0 == "q":
                    print(term.clear)
                    return
                elif key_0 == "P" or key_0 == "p":
                    return search(parents[-2], True)
                else:
                    continue
            else:
                continue
    else:
        print(term.clear + term.move_y(term.height//3) + term.center(f"He\
re is last element of this branch:"))
        print(term.center(f"{variants}"))
        print(term.center(f"Type {term.blue}'X'{term.normal}+ENTER to rest\
art, {term.red}'Q' {term.normal}to quit"))
        while True:
            key = input()
            if key == "X" or key == "x":
                parents = []
                return start_screen()
            elif key == "Q" or key == "q":
                print(term.clear)
                return


def error_screen() -> str:
    """
    This function prints error screen if something
    wronge happens.
    """
    term = blessed.Terminal()
    print(term.clear + term.move_y(term.height//3) + term.center(f"Plea\
se, enter {term.red}correct {term.normal}path to {term.green}.json fil\
e{term.normal}."))
    print()
    print(term.center(f"If your path is {term.green}correct{term.normal}, f\
ile may have {term.purple}unexpected {term.normal}types of data."))
    print()
    print(term.center(f"Type {term.blue}'X'{term.normal}+ENTER to restart o\
r {term.red}'Q' {term.normal}to quit."))
    while True:
        key = input()
        if key == "X" or key == "x":
            parents = []
            return start_screen()
        elif key == "Q" or key == "q":
            print(term.clear)
            return
        else:
            continue


if __name__ == "__main__":
    parents = []
    start_screen()