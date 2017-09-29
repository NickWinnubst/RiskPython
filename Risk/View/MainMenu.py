import tkinter as tk
from View.Board import Board
from View.GameBoard import GameBoard

class MainMenu(tk.Frame):

    def __init__(self, parent, *args, **kwargs):

        self.parent = parent

        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.display = tk.PhotoImage(file="../Maps/click-to-start.png")
        w = self.display.width()
        h = self.display.height()

        self.canvas = tk.Canvas(self.parent, width=w, height=h)
        self.canvas.pack()
        self.parent.update()
        self.canvas.create_image(0, 0, image=self.display, anchor='nw')
        self.canvas.bind('<Button-1>', self.show_player_count_slider)

        self.board = None

        self.players = [["Black Player","black"],["Red Player","red"],["Blue Player","blue"],["Pink Player","magenta"],["Orange Player","orange"],["Brown Player","saddle brown"]]

    def clear(self):
        for item in self.parent.winfo_children():
            item.destroy()


    def show_player_count_slider(self,event):
        x, y = self.canvas.winfo_width(),self.canvas.winfo_height()

        block = tk.Label(self.canvas, text="Select Player Count")
        block.configure(relief='raised', font="helvetica 28", foreground="black", background="white", bd=10)
        self.canvas.create_window(x/2, y/3, window=block, tags='popup')

        scale = tk.Scale(self.canvas, from_=2, to=len(self.players))
        scale.configure(relief='raised', font="helvetica 28", foreground="black", background="white", bd=10, orient=tk.HORIZONTAL, length = x/2)
        self.canvas.create_window(x/2, y/2, window=scale, tags='popup')

        def confirm():
            s = scale.get()
            self.clear()
            self.board = GameBoard(self.parent,[self.players[p] for p in range(0,s)], "../Maps/risk-1-original")

        confirmed = tk.Button(self.canvas, text = "Confirm", command=confirm)
        confirmed.configure(relief='raised', font="helvetica 28", foreground="black", background="white", bd=10)
        self.canvas.create_window(x/2, y*2/3, window=confirmed, tags='popup')


if __name__ == "__main__":
    root = tk.Tk()
    root.title("RiskPython")
    MainMenu(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
