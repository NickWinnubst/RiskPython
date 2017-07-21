import tkinter as tk
from Model import MapLoader
from Controller import SetUpGame
from Controller.Battle import attack
from Model.Territory import *

class MainMenu(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        self.parent = parent

        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.players = [["Fred","blue"],["George","green"],["Ron","red"]]

        self.game_map = MapLoader.load_fresh_map("../Maps/risk-1-original.json")
        self.game_map = SetUpGame.set_up_game([p[0] for p in self.players], self.game_map)

        self.previous = Territory("None")
        self.attack = [self.previous,self.previous]

        self.display = tk.PhotoImage(file="../Maps/risk-1-original.png")
        self.display_map = tk.Label(root, image=self.display)
        self.display_map.bind('<Button-1>', self.left_click)

        self.update()

        self.game_map.print()

    def left_click(self,event):
        self.attack = self.print_location_data(event)
        try:
            self.pop_up.destroy()
        except AttributeError:
            ()
        if self.attack[0].name in self.attack[1].connections and self.attack[0].armies > 1 and self.attack[0].owner is not self.attack[1].owner:
            self.pop_up_attack()

    def print_location_data(self,event):
        selected = self.game_map.get_closest_territory([event.x,event.y])
        print("----------------------------------")
        print("Clicked at: %s, %s" % (event.x,event.y))
        print("Closest territory: %s" % selected.name)
        print("Territory owner: %s" % selected.owner)
        print("Army count: %s" % selected.armies)
        print("Connected to %s: %s" % (self.previous.name, self.previous.name in selected.connections))
        previous = self.previous
        self.previous = selected
        return (previous, selected)

    def pop_up_attack(self):
        self.pop_up = tk.Toplevel()
        self.pop_up.geometry("20x40+200+200")
        label1 = tk.Label(self.pop_up, text="Attack?")
        label1.pack()
        label2 = tk.Button(self.pop_up, text="GO!", command=self.execute_attack)
        label2.pack()

    def execute_attack(self):
        success = False
        if self.attack[0].armies > 1 and self.attack[1].armies > 0 and self.attack[0].owner is not self.attack[1].owner:
            attackers_lost, defenders_lost = attack(min(3,self.attack[0].armies-1),min(2,self.attack[1].armies))
            self.attack[0].armies -= attackers_lost
            self.attack[1].armies -= defenders_lost
        if self.attack[1].armies == 0:
            self.attack[1].armies = self.attack[0].armies-1
            self.attack[0].armies = 1
            self.attack[1].owner = self.attack[0].owner
            success = True

        if self.attack[0].armies == 1:
            self.pop_up.destroy()
            if success is not True:
                self.previous = Territory("None")
        self.update()

    def update(self):
        for label in self.display_map.winfo_children():
            label.destroy()
        for territory in self.game_map.get_all_territories():
            label = tk.Label(self.display_map, text=str(territory.armies))
            label.place(x=territory.location[0], y=territory.location[1])
            label.configure(font="helvetica 14 bold",relief="raised", foreground="white", background=self.players[[p[0] for p in self.players].index(territory.owner)][1])
        self.display_map.pack()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("RiskPython")
    MainMenu(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
