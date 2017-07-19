import tkinter as tk
from Model import MapLoader
from Controller import SetUpGame


class MainMenu(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.game_map = MapLoader.load_fresh_map("../Maps/TestMap.json")
        self.game_map = SetUpGame.set_up_game([1,2,3], self.game_map)

        self.new_game_button = tk.Button(self, text="Print Test Map", command = self.game_map.print)
        self.new_game_button.pack()


if __name__ == "__main__":
    root = tk.Tk()
    MainMenu(root).pack(side="top", fill="both", expand=True)
    root.mainloop()