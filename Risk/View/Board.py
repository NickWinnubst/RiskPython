import tkinter as tk
from Model import MapLoader
from Controller import SetUpGame
from Controller.Battle import attack
from Model.Territory import *
from Controller.Reinforce import get_reinforcements


class Board(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        self.parent = parent

        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.players = [["Fred","blue"],["George","green"],["Ron","red"]]

        self.game_map = MapLoader.load_fresh_map("../Maps/risk-1-original.json")
        self.game_map = SetUpGame.set_up_game([p[0] for p in self.players], self.game_map)

        self.current_player_nr = 0
        self.reinforcements = get_reinforcements(self.players[self.current_player_nr%len(self.players)][0],self.game_map)

        self.previous = Territory("None")
        self.fighting_countries = [self.previous, self.previous]

        self.display = tk.PhotoImage(file="../Maps/risk-1-original.png")
        self.display_map = tk.Label(root, image=self.display)
        self.display_map.bind('<Button-1>', self.left_click)

        self.update()

        self.game_map.print()

    def next_turn(self):
        if self.reinforcements > 0:
            return
        self.current_player_nr += 1
        self.reinforcements = get_reinforcements(self.players[self.current_player_nr%len(self.players)][0],self.game_map)
        self.update()

    def left_click(self,event):
        self.fighting_countries = self.location_data(event)
        try:
            self.pop_up.destroy()
        except AttributeError:
            ()
        if self.reinforcements > 0 and self.fighting_countries[1].owner is self.players[self.current_player_nr%len(self.players)][0]:
            self.fighting_countries[1].armies += 1
            self.reinforcements -= 1
        elif self.fighting_countries[0].name in self.fighting_countries[1].connections and self.fighting_countries[0].armies > 1 and self.fighting_countries[0].owner is not self.fighting_countries[1].owner and self.fighting_countries[0].owner is self.players[self.current_player_nr%len(self.players)][0]:
            self.pop_up_attack()

        self.update()

    def location_data(self,event):
        selected = self.game_map.get_closest_territory([event.x,event.y])
        self.print_location_data(selected,event)

        previous = self.previous
        self.previous = selected
        return previous, selected

    def print_location_data(self,selected, event):
        print("----------------------------------")
        print("Clicked at: %s, %s" % (event.x,event.y))
        print("Closest territory: %s" % selected.name)
        print("Territory owner: %s" % selected.owner)
        print("Army count: %s" % selected.armies)
        print("Connected to %s: %s" % (self.previous.name, self.previous.name in selected.connections))

    # Query attack
    def pop_up_attack(self):
        self.pop_up = tk.Toplevel()
        self.pop_up.geometry("20x40+590+400")
        label1 = tk.Label(self.pop_up, text="Attack " + self.fighting_countries[1].name + "?")
        label1.pack()
        label2 = tk.Button(self.pop_up, text="GO!", command=self.execute_attack)
        label2.pack()

    def execute_attack(self):
        success = False
        if self.fighting_countries[0].armies > 1 and self.fighting_countries[1].armies > 0 and self.fighting_countries[0].owner is not self.fighting_countries[1].owner:
            attackers_lost, defenders_lost = attack(min(3, self.fighting_countries[0].armies - 1), min(2, self.fighting_countries[1].armies))
            self.fighting_countries[0].armies -= attackers_lost
            self.fighting_countries[1].armies -= defenders_lost
        if self.fighting_countries[1].armies == 0:
            self.fighting_countries[1].armies = self.fighting_countries[0].armies - 1
            self.fighting_countries[0].armies = 1
            self.fighting_countries[1].owner = self.fighting_countries[0].owner
            success = True

        if self.fighting_countries[0].armies == 1:
            self.pop_up.destroy()
            if success is not True:
                self.previous = Territory("None")
        self.update()

    # Update the visuals.
    def update(self):
        for label in self.display_map.winfo_children():
            label.destroy()
        for territory in self.game_map.get_all_territories():
            label = tk.Label(self.display_map, text=str(territory.armies))
            label.place(x=territory.location[0], y=territory.location[1])
            label.configure(font="helvetica 14",relief="raised", foreground="white", background=self.players[[p[0] for p in self.players].index(territory.owner)][1])
            if self.fighting_countries[1] is territory:
                label.configure(font="helvetica 20 bold")
            elif self.fighting_countries[0] is territory and self.fighting_countries[0].name in self.fighting_countries[1].connections:
                label.configure(font="helvetica 20 bold")

        self.current_player_label = tk.Label(self.display_map, text=self.players[self.current_player_nr%len(self.players)][0])
        self.current_player_label.configure(font="helvetica 14 bold",relief="raised", foreground="white", background=self.players[self.current_player_nr%len(self.players)][1])
        self.current_player_label.place(x=1000,y=350)

        next_turn_button = tk.Button(self.display_map, text="Next Turn", command=self.next_turn)
        next_turn_button.configure(font="helvetica 14 bold",relief="raised", foreground="white", background="black")
        next_turn_button.place(x=1000,y=400)

        if self.reinforcements > 0:
            self.reinforcements_label = tk.Button(self.display_map, text="Reinforce: " + str(self.reinforcements), command=self.next_turn)
        else:
            self.reinforcements_label = tk.Button(self.display_map, text="Battle!", command=self.next_turn)
        self.reinforcements_label.configure(font="helvetica 14 bold",relief="raised", foreground="white", background=self.players[self.current_player_nr%len(self.players)][1])
        self.reinforcements_label.place(x=1000,y=300)

        self.display_map.pack()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("RiskPython")
    Board(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
