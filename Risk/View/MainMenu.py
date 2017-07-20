import tkinter as tk
from Model import MapLoader
from Controller import SetUpGame

class MainMenu(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.game_map = MapLoader.load_fresh_map("../Maps/risk-1-original.json")
        self.game_map = SetUpGame.set_up_game([1,2,3], self.game_map)

        #self.new_game_button = tk.Button(root, text="Print Test Map", command = self.game_map.print)
        #self.new_game_button.pack()
        self.display = tk.PhotoImage(file="../Maps/risk-1-original.png")
        self.display_map = tk.Label(root, image=self.display)

        def motion(event):
            print("Clicked at: %s, %s" % (event.x,event.y))

        self.display_map.bind('<Button-1>', motion)
        self.display_map.pack()

        self.game_map.print()



if __name__ == "__main__":
    root = tk.Tk()
    MainMenu(root).pack(side="top", fill="both", expand=True)
    root.mainloop()