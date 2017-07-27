import tkinter as tk
from Model import MapLoader
from Controller import SetUpGame
from Controller.Battle import attack
from Model.Territory import *
from Controller.Reinforce import *


class GameBoard(tk.Frame):

    def __init__(self, parent, players, map_file, *args, **kwargs):
        self.parent = parent

        self.players = players

        self.game_map = MapLoader.load_fresh_map(map_file + ".json")
        self.game_map, self.current_player_nr = SetUpGame.set_up_game(self.players, self.game_map)

        self.current_player = self.players[self.current_player_nr % len(self.players)]

        self.reinforcements = get_reinforcements(self.current_player, self.game_map)

        self.selected_territory = Territory("None")
        self.targeted_territory = Territory("None")
        self.attacking_armies = 0

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
        elif self.selected_territory.name is not "None" and clicked_on.name in self.selected_territory.connections:
            self.update_targeted(clicked_on)
            self.show_attack_slider(clicked_on)
            return

    def attack(self,attack_from, attack_to, amount):
        score, attack_dice, defend_dice = attack(amount,min(attack_to.armies,2))
        attack_from.armies -= score[0]
        attack_to.armies -= score[1]
        self.update_selected(attack_from)
        self.update_targeted(attack_to)
        self.draw_dice(attack_from, attack_dice,attack_to,defend_dice)
        if attack_to.armies is 0:
            self.draw_attack_complete_slider(attack_from, attack_to, amount)


    def attack_complete(self, attack_from, attack_to, amount):
        attack_from.armies -= amount
        attack_to.set_owner(attack_from.owner, amount)
        self.update_selected(attack_from)
        self.update_targeted(attack_to)


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
        self.canvas.delete("selected")
        self.canvas.delete("target")
        self.selected_territory = Territory("None")
        self.targeted_territory = Territory("None")
        self.attacking_armies = 0
        self.canvas.delete('popup')

        self.draw_next_phase_button()

    def next_phase(self):
        if self.current_phase is "Reinforce" and self.reinforcements is 0:
            self.move_to_phase("Combat")
        elif self.current_phase is "Combat":
            self.move_to_phase("Transfer")
        elif self.current_phase is "Transfer":
            self.current_player_nr += 1
            self.current_player = self.players[self.current_player_nr % len(self.players)]
            self.reinforcements = get_reinforcements(self.current_player, self.game_map)
            self.move_to_phase("Reinforce")

    def move_to_phase(self,new_phase):
        self.current_phase = new_phase
        self.clear_pop_up()
        self.show_new_phase(new_phase)
        print(self.current_player[0] + " is now in the " + self.current_phase + " phase.")

    def draw_armies(self, territory, selected=""):
        [x, y] = territory.location

        self.canvas.delete(territory.name)
        block = tk.Label(self.canvas, text = str(territory.armies), relief='raised', font="helvetica 14", foreground="white", background=territory.owner[1])
        block.bind('<Button-1>', self.click_left)
        self.canvas.create_window(x-5, y-10, window=block, tags=territory.name)
        if selected is not "":
            self.canvas.delete(selected)
            block = tk.Label(self.canvas, text = str(territory.armies), relief='raised', font="helvetica 28", foreground=territory.owner[1], background="white", bd=10)
            block.bind('<Button-1>', self.click_left)
            self.canvas.create_window(x-5, y-10, window=block, tags=selected)

    def update_selected(self, clicked_on):
        self.selected_territory = clicked_on
        if self.selected_territory.name is not "None":
            self.draw_armies(self.selected_territory, selected="selected")

    def update_targeted(self, clicked_on):
        self.targeted_territory = clicked_on
        if self.targeted_territory.name is not "None":
            self.draw_armies(self.targeted_territory, selected="target")

######################################

    def show_new_phase(self, new_phase):
        # TODO: implement announcement of the new phase
        x, y = self.canvas.winfo_width(),self.canvas.winfo_height()

        block = tk.Label(self.canvas, text=self.current_player[0] + " \n " + self.current_phase + " Phase")
        block.configure(relief='raised', font="helvetica 42", foreground="white", background=self.current_player[1], bd=10)
        block.bind('<Button-1>', self.click_left)
        self.canvas.create_window(x/2, y/3, window=block, tags='popup')

        if new_phase is "Reinforce":
            block = tk.Label(self.canvas, text=str(self.reinforcements) + " Reinforcements \n\n" + str(get_territory_reinforcements(self.current_player,self.game_map)[1]) + " from Territories \n" + str(get_region_reinforcements(self.current_player, self.game_map)[1]) + " from Regions")
            block.configure(relief='raised', font="helvetica 28", foreground="white", background=self.current_player[1], bd=10)
            block.bind('<Button-1>', self.click_left)
            self.canvas.create_window(x/2, y*2/3, window=block, tags='popup')

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
        scale.set(self.reinforcements)
        scale.configure(relief='raised', font="helvetica 28", foreground="white", background=self.current_player[1], bd=10, orient=tk.HORIZONTAL, length = x/2)
        self.canvas.create_window(x/2, y/2, window=scale, tags='popup')

        def confirm():
            self.reinforce(self.selected_territory,scale.get())
            self.update_selected(self.selected_territory)
            self.clear_pop_up()
            if self.reinforcements is 0:
                self.move_to_phase("Combat")

        confirmed = tk.Button(self.canvas, text = "Deploy Armies", command=confirm)
        confirmed.configure(relief='raised', font="helvetica 28", foreground="white", background=self.current_player[1], bd=10)
        self.canvas.create_window(x/2, y*2/3, window=confirmed, tags='popup')

        self.pop_up = True

    def show_attack_slider(self, clicked_on):
        self.update_targeted(clicked_on)
        x, y = self.canvas.winfo_width(),self.canvas.winfo_height()

        name_tag = tk.Label(self.canvas, text=self.current_player[0])
        name_tag.configure(relief='raised', font="helvetica 42", foreground="white", background=self.current_player[1], bd=10)
        self.canvas.create_window(x/3, y/6, window=name_tag, tags='popup')

        name_tag = tk.Label(self.canvas, text=self.targeted_territory.owner[0])
        name_tag.configure(relief='raised', font="helvetica 42", foreground="white", background=self.targeted_territory.owner[1], bd=10)
        self.canvas.create_window(x*2/3, y/6, window=name_tag, tags='popup')

        block = tk.Label(self.canvas, text="Attacking \n from " + self.selected_territory.name.replace('_',' ') + " (" + str(self.selected_territory.armies) + ")\n to " + self.targeted_territory.name.replace('_',' ') + " (" + str(self.targeted_territory.armies) + ")")
        block.configure(relief='raised', font="helvetica 28", foreground="white", background=self.current_player[1], bd=10)
        self.canvas.create_window(x/2, y/3, window=block, tags='popup')

        scale = tk.Scale(self.canvas, from_=1, to=min(self.selected_territory.armies-1,3))
        scale.set(min(self.selected_territory.armies-1,3))
        scale.configure(relief='raised', font="helvetica 28", foreground="white", background=self.current_player[1], bd=10, orient=tk.HORIZONTAL, length = x/2)
        self.canvas.create_window(x/2, y/2, window=scale, tags='popup')

        def confirm():
            self.attack(self.selected_territory, self.targeted_territory, scale.get())

        confirmed = tk.Button(self.canvas, text = "Attack!", command=confirm)
        confirmed.configure(relief='raised', font="helvetica 28", foreground="white", background=self.current_player[1], bd=10)
        self.canvas.create_window(x/2, y*2/3, window=confirmed, tags='popup')

        self.pop_up = True

    def draw_dice(self, attacker, attack_dice, defender, defend_dice):
        self.clear_pop_up()
        x, y = self.canvas.winfo_width(),self.canvas.winfo_height()
        attack_text = attacker.name.replace('_',' ') + " "
        for die in attack_dice:
            attack_text += " " + str(die) + " "
        block = tk.Label(self.canvas, text=attack_text)
        block.configure(relief='raised', font="helvetica 42", foreground="white", background=attacker.owner[1], bd=10)
        self.canvas.create_window(x/2, y*4/9, window=block, tags='popup')

        defend_text = defender.name.replace('_',' ') + " "
        for die in defend_dice:
            defend_text += " " + str(die) + " "
        block = tk.Label(self.canvas, text=defend_text)
        block.configure(relief='raised', font="helvetica 42", foreground="white", background=defender.owner[1], bd=10)
        self.canvas.create_window(x/2, y*5/9, window=block, tags='popup')

        self.pop_up = True

    def draw_attack_complete_slider(self, attack_from, attack_to, amount):
        self.clear_pop_up()
        self.update_selected(attack_to)
        x, y = self.canvas.winfo_width(),self.canvas.winfo_height()

        name_tag = tk.Label(self.canvas, text=self.current_player[0])
        name_tag.configure(relief='raised', font="helvetica 42", foreground="white", background=self.current_player[1], bd=10)
        self.canvas.create_window(x/2, y/6, window=name_tag, tags='popup')

        block = tk.Label(self.canvas, text="Conquered " + attack_to.name.replace('_',' ') + "\n from " + attack_from.name.replace('_',' '))
        block.configure(relief='raised', font="helvetica 28", foreground="white", background=self.current_player[1], bd=10)
        self.canvas.create_window(x/2, y/3, window=block, tags='popup')

        scale = tk.Scale(self.canvas, from_=amount, to=attack_from.armies-1)
        scale.set(attack_from.armies-1)
        scale.configure(relief='raised', font="helvetica 28", foreground="white", background=self.current_player[1], bd=10, orient=tk.HORIZONTAL, length = x/2)
        self.canvas.create_window(x/2, y/2, window=scale, tags='popup')

        def confirm():
            self.attack_complete(attack_from, attack_to,scale.get())
            self.update_selected(attack_from)
            self.update_targeted(attack_to)
            self.clear_pop_up()

        confirmed = tk.Button(self.canvas, text = "Deploy Armies", command=confirm)
        confirmed.configure(relief='raised', font="helvetica 28", foreground="white", background=self.current_player[1], bd=10)
        self.canvas.create_window(x/2, y*2/3, window=confirmed, tags='popup')

        self.pop_up = True

    def draw_next_phase_button(self):
        x, y = self.canvas.winfo_width(),self.canvas.winfo_height()
        next_phase_button = tk.Button(self.canvas, text="End\n" + self.current_phase + "\nPhase", command=self.next_phase)
        next_phase_button.configure(font="helvetica 20 bold",relief="raised", foreground="white", background=self.current_player[1])
        self.canvas.create_window(1075, y/2, window=next_phase_button, tags='popup')

if __name__ == "__main__":
    root = tk.Tk()
    root.title("RiskPython")
    GameBoard(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
