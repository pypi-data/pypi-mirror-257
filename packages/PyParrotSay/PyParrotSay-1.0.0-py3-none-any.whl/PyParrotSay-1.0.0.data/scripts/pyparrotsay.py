class ParrotSay:
    def __init__(self, rgb: list = [232,155,23]) -> None:
        from sty import fg, Style, RgbFg
        from tkinter import ttk
        import tkinter as tk
        import webbrowser
        import os
        self.fg = fg
        self.style = Style
        self.rgbfg = RgbFg
        self.ttk = ttk
        self.tk = tk
        self.os = os
        self.web = webbrowser
        self._deftxt = "DEFAULT TEXT"
        self.R = int(rgb[0])
        self.G = int(rgb[1])
        self.B = int(rgb[2])
        self.rgb_list = rgb
        self.about_root = self.tk.Tk()
        self.about_root.withdraw()

    def say(self, text: str = None) -> None:
        self.fg.custom = self.style(self.rgbfg(self.R, self.G, self.B))
        if text == None:
            print(self.fg.custom + f"""
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
"""  + self.fg.rs)
        else:
            print(self.fg.custom + f"""
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
""" + self.fg.rs)

    def clear_screen(self) -> None:
        self.os.system('cls' if self.os.name == 'nt' else 'clear')

    def about_parrotsay(self) -> None:
        self.about_root.title("About PyParrotSay")
        self.about_root.geometry("500x500")
        self.about_root.config(bg="#505050")
        title = self.ttk.Label(self.about_root, text="About PyParrotSay", font=('Impact', 23))
        title.config(foreground="#ffffff", background="#505050")
        title.pack(pady=20)
        github_button = self.ttk.Button(self.about_root, text="Github Repo", command=lambda: self.web.open_new_tab("https://github.com/DevHollo/pyparrotsay/tree/main"))
        github_button.pack(pady=20)
        pypi_button = self.ttk.Button(self.about_root, text="PyPi Page", command=lambda: self.web.open_new_tab("https://pypi.org/project/PyParrotSay/"))
        pypi_button.pack(pady=20)
        self.about_root.deiconify()
        self.about_root.mainloop()