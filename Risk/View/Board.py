import tkinter as tk
from Model import MapLoader
from Controller import SetUpGame
from Controller.Battle import attack
from Model.Territory import *
from Controller.Reinforce import get_reinforcements


class Board(tk.Frame):

    def __init__(self, parent, players, *args, **kwargs):
        self.parent = parent

        self.players = players

        self.game_map = MapLoader.load_fresh_map("../Maps/risk-1-original.json")
        self.game_map = SetUpGame.set_up_game([p[0] for p in self.players], self.game_map)

        self.current_player_nr = 0
        self.reinforcements = get_reinforcements(self.players[self.current_player_nr%len(self.players)][0],self.game_map)

        self.previous = Territory("None")
        self.fighting_countries = [self.previous, self.previous]

        self.display = tk.PhotoImage(file="../Maps/risk-1-original.png")
        self.display_map = tk.Label(self.parent, image=self.display)
        self.display_map.bind('<Button-1>', self.left_click)

        self.update()

        self.game_map.print()

    def next_turn(self):
        if self.reinforcements > 0:
            return
        self.current_player_nr += 1
        while not self.game_map.has_a_territory(self.players[self.current_player_nr%len(self.players)][0]):
            self.current_player_nr += 1
        self.reinforcements = get_reinforcements(self.players[self.current_player_nr%len(self.players)][0],self.game_map)
        self.update()

    def left_click(self,event):
        self.fighting_countries = self.location_data(event)
        try:
            self.pop_up_result.destroy()
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
        #self.pop_up.geometry("80x40+590+400")
        self.pop_up.configure(background="black")
        label1 = tk.Label(self.pop_up, text="Attack " + self.fighting_countries[1].name + " from " + self.fighting_countries[0].name + "?")
        label1.configure(font="helvetica 14 bold",relief="raised", foreground="white", background="black")
        label1.pack()
        label2 = tk.Button(self.pop_up, text="Attack!", command=self.execute_attack)
        label2.configure(font="helvetica 14 bold",relief="raised", foreground="white", background="black")
        label2.place(x=300,y=500)
        label2.pack()

    def pop_up_win(self):
        self.pop_up_win = tk.Toplevel()
        self.pop_up_win.configure(background="black")
        label1 = tk.Label(self.pop_up_win, text=self.players[self.current_player_nr%len(self.players)][0] + " has won the game!")
        label1.configure(font="helvetica 14 bold",relief="raised", foreground="white", background="black")
        label1.pack()

    def pop_up_result(self,result):
        self.result_pop_up = tk.Toplevel()
        self.result_pop_up.configure(background="black")
        label1 = tk.Label(self.result_pop_up, text="Attacking armies lost " + str(result[0]))
        label1.configure(font="helvetica 14 bold",relief="raised", foreground="white", background="black")
        label1.pack()
        label2 = tk.Label(self.result_pop_up, text="Defending armies lost " + str(result[1]))
        label2.configure(font="helvetica 14 bold",relief="raised", foreground="white", background="black")
        label2.pack()
        label3 = tk.Button(self.result_pop_up, text="Close", command=self.result_pop_up.destroy)
        label3.configure(font="helvetica 14 bold",relief="raised", foreground="white", background="black")
        label3.pack()

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
        try:
            self.pop_up_result([attackers_lost,defenders_lost])
        except UnboundLocalError:
            ()
        self.update()

    # Update the visuals.
    def update(self):
        for label in self.display_map.winfo_children():
            label.destroy()
        for territory in self.game_map.get_all_territories():
            label = tk.Label(self.display_map, text=str(territory.armies))
            label.place(x=territory.location[0]-5, y=territory.location[1]-10)
            label.configure(font="helvetica 14",relief="raised", foreground="white", background=self.players[[p[0] for p in self.players].index(territory.owner)][1])
            if self.fighting_countries[1] is territory:
                label.configure(font="helvetica 24 bold", foreground=self.players[[p[0] for p in self.players].index(territory.owner)][1], background="white")
            elif self.fighting_countries[0] is territory and self.fighting_countries[0].name in self.fighting_countries[1].connections:
                label.configure(font="helvetica 20 bold", foreground=self.players[[p[0] for p in self.players].index(territory.owner)][1], background="white")

        self.current_player_label = tk.Label(self.display_map, text=self.players[self.current_player_nr%len(self.players)][0])
        self.current_player_label.configure(font="helvetica 14 bold",relief="raised", foreground="white", background=self.players[self.current_player_nr%len(self.players)][1])
        self.current_player_label.place(x=1000,y=350)

        next_turn_button = tk.Button(self.display_map, text="Next Turn", command=self.next_turn)
        next_turn_button.configure(font="helvetica 14 bold",relief="raised", foreground="white", background="black")
        next_turn_button.place(x=1000,y=400)

        if self.reinforcements > 0:
            self.reinforcements_label = tk.Label(self.display_map, text="Reinforce: " + str(self.reinforcements))
        else:
            self.reinforcements_label = tk.Label(self.display_map, text="Battle!")
        self.reinforcements_label.configure(font="helvetica 14 bold",relief="raised", foreground="white", background=self.players[self.current_player_nr%len(self.players)][1])
        self.reinforcements_label.place(x=1000,y=300)

        self.display_map.pack()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("RiskPython")
    Board(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
