import tkinter as tk
from Model import MapLoader
from Controller import SetUpGame
from Controller.Battle import attack
from Model.Territory import *
from Controller.Reinforce import get_reinforcements


class GameBoard(tk.Frame):

    def __init__(self, parent, players, map_file, *args, **kwargs):
        self.parent = parent

        self.players = players

        self.game_map = MapLoader.load_fresh_map(map_file + ".json")
        self.game_map, self.current_player_nr = SetUpGame.set_up_game(self.players, self.game_map)

        self.current_player = self.players[self.current_player_nr % len(self.players)]

        self.reinforcements = get_reinforcements(self.current_player, self.game_map)

        self.selected_territory = Territory("None")

        self.map_image = tk.PhotoImage(file=map_file + ".png")
        w = self.map_image.width()
        h = self.map_image.height()

        self.canvas = tk.Canvas(self.parent, width=w, height=h)
        self.canvas.pack()
        self.parent.update()
        self.canvas.create_image(0, 0, image=self.map_image, anchor='nw')
        self.canvas.bind('<Button-1>', self.click_left)

        for territory in self.game_map.get_all_territories():
            self.draw_armies(territory)

        self.pop_up = False
        self.move_to_phase("Reinforce")

    ########################################

    def click_left(self, event):
        clicked_on = self.game_map.get_closest_territory([event.x,event.y])
        if str(event.widget).__contains__('.!label'):
            clicked_on = self.game_map.get_closest_territory([event.widget.winfo_x(),event.widget.winfo_y()])


        if self.pop_up is True:
            self.clear_pop_up()
        elif self.current_phase is "Reinforce":
            self.click_reinforce(clicked_on)
        elif self.current_phase is "Combat":
            self.click_combat(clicked_on)
        elif self.current_phase is "Fortify":
            self.click_fortify(clicked_on)

    ########################################

    def click_reinforce(self, clicked_on):
        if clicked_on.owner is not self.current_player:
            return
        self.show_reinforce_slider(clicked_on)

    def reinforce(self,territory, amount):
        territory.armies += amount
        self.reinforcements -= amount

    #######################################

    def click_combat(self, clicked_on):
        if clicked_on.owner is self.current_player:
            self.update_selected(clicked_on)
            return
        elif self.selected_territory.name is not "None":
            self.query_combat(clicked_on)
            return

    def query_combat(self,clicked_on):
        print("Fight: " + clicked_on.name)

    ########################################

    def click_fortify(self, clicked_on):
        return
        # TODO: implement proper fortify
        # if clicked_on.ownes is not self.current_player:
        #     return
        # elif clicked_on.ownes is self.current_player and self.selected_territory.name is "None":
        #     self.selected_territory = clicked_on
        #     return
        # elif self.selected_territory.name is not "None":
        #     self.query_fortify(clicked_on)
        #     return

    def query_fortify(self,clicked_on):
        ()

    ######################################

    def clear_pop_up(self):
        self.pop_up = False
        self.selected_territory = Territory("None")
        self.canvas.delete('popup')

    def move_to_phase(self,new_phase):
        self.current_phase = new_phase
        self.clear_pop_up()
        self.show_new_phase()
        print(self.current_player[0] + " is now in the " + self.current_phase + " phase.")

    def draw_armies(self, territory, selected=False):
        [x, y] = territory.location

        self.canvas.delete(territory.name)
        block = tk.Label(self.canvas, text = str(territory.armies), relief='raised', font="helvetica 14", foreground="white", background=territory.owner[1])
        block.bind('<Button-1>', self.click_left)
        self.canvas.create_window(x-5, y-10, window=block, tags=territory.name)
        if selected:
            self.canvas.delete('selected')
            block = tk.Label(self.canvas, text = str(territory.armies), relief='raised', font="helvetica 28", foreground=territory.owner[1], background="white", bd=10)
            block.bind('<Button-1>', self.click_left)
            self.canvas.create_window(x-5, y-10, window=block, tags='selected')

    def update_selected(self, clicked_on):
        self.selected_territory = clicked_on
        if self.selected_territory.name is not "None":
            self.draw_armies(self.selected_territory, selected=True)

    ######################################

    def show_new_phase(self):
        # TODO: implement announcement of the new phase
        x, y = self.canvas.winfo_width(),self.canvas.winfo_height()
        block = tk.Label(self.canvas, text=self.current_player[0] + " \n " + self.current_phase + " Phase")
        block.configure(relief='raised', font="helvetica 42", foreground="white", background=self.current_player[1], bd=10)
        block.bind('<Button-1>', self.click_left)
        self.canvas.create_window(x/2, y/2, window=block, tags='popup')
        self.pop_up = True

    def show_reinforce_slider(self, clicked_on):
        self.clear_pop_up()
        self.update_selected(clicked_on)
        x, y = self.canvas.winfo_width(),self.canvas.winfo_height()

        name_tag = tk.Label(self.canvas, text=self.current_player[0])
        name_tag.configure(relief='raised', font="helvetica 42", foreground="white", background=self.current_player[1], bd=10)
        self.canvas.create_window(x/2, y/6, window=name_tag, tags='popup')

        block = tk.Label(self.canvas, text="Deploying new troops at " + self.selected_territory.name.replace('_',' ') + "\n Currently holds " + str(self.selected_territory.armies) + " armies.")
        block.configure(relief='raised', font="helvetica 28", foreground="white", background=self.current_player[1], bd=10)
        self.canvas.create_window(x/2, y/3, window=block, tags='popup')

        scale = tk.Scale(self.canvas, from_=1, to=self.reinforcements)
        scale.configure(relief='raised', font="helvetica 28", foreground="white", background=self.current_player[1], bd=10, orient=tk.HORIZONTAL, length = x/2)
        self.canvas.create_window(x/2, y/2, window=scale, tags='popup')

        def confirm():
            self.reinforce(self.selected_territory,scale.get())
            self.update_selected(self.selected_territory)
            if self.reinforcements is 0:
                self.move_to_phase("Combat")

        confirmed = tk.Button(self.canvas, text = "Deploy Armies", command=confirm)
        confirmed.configure(relief='raised', font="helvetica 28", foreground="white", background=self.current_player[1], bd=10)
        self.canvas.create_window(x/2, y*2/3, window=confirmed, tags='popup')

        self.pop_up = True


if __name__ == "__main__":
    root = tk.Tk()
    root.title("RiskPython")
    GameBoard(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
