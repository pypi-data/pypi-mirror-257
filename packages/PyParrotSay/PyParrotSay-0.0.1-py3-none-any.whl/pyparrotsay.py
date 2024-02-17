from colorama import Style as st
from colorama import Fore
import os

class ParrotSay:
    def __init__(self) -> None:
        self._deftxt = "DEFAULT TEXT"

    def say(self, text: str = None) -> None:
        if text == None:
            print(Fore.YELLOW + f"""
     (\"{self._deftxt}\")
       \\
        \\
        __,---.
       /__|o\\  )
        `-\\ / /
          ,) (,
         //   \\\\
        {{(     )}}
  =======""===""===============
          |||||
           |||
            |
"""  + st.RESET_ALL)
        else:
            print(Fore.YELLOW + f"""
     (\"{text}\")
       \\
        \\
        __,---.
       /__|o\\  )
        `-\\ / /
          ,) (,
         //   \\\\
        {{(     )}}
  =======""===""===============
          |||||
           |||
            |
""" + st.RESET_ALL)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

ParrotSay().say("SEX")