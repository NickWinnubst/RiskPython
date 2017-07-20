import tkinter as tk
from Model import MapLoader
from Controller import SetUpGame

class MainMenu(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.players = [["Fred","blue"],["George","green"],["Ron","red"]]

        self.game_map = MapLoader.load_fresh_map("../Maps/risk-1-original.json")
        self.game_map = SetUpGame.set_up_game([p[0] for p in self.players], self.game_map)

        #self.new_game_button = tk.Button(root, text="Print Test Map", command = self.game_map.print)
        #self.new_game_button.pack()
        self.display = tk.PhotoImage(file="../Maps/risk-1-original.png")
        self.display_map = tk.Label(root, image=self.display)

        def motion(event):
            print("----------------------------------")
            print("Clicked at: %s, %s" % (event.x,event.y))
            print("Closest territory: %s" % self.game_map.get_closest_territory([event.x,event.y]).name)
            print("Territory owner: %s" % self.game_map.get_closest_territory([event.x,event.y]).owner)
            print("Army count: %s" % self.game_map.get_closest_territory([event.x,event.y]).armies)

        self.display_map.bind('<Button-1>', motion)
        for territory in self.game_map.get_all_territories():
            label = tk.Label(self.display_map, text=str(territory.armies))
            label.place(x=territory.location[0], y=territory.location[1])
            label.configure(font="helvetica 14 bold",relief="raised", foreground="white", background=self.players[[p[0] for p in self.players].index(territory.owner)][1])
        self.display_map.pack()

        self.game_map.print()



if __name__ == "__main__":
    root = tk.Tk()
    root.title("RiskPython")
    MainMenu(root).pack(side="top", fill="both", expand=True)
    root.mainloop()