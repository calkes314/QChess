import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageTk

# --- Mapping ---
FIGURE_UNICODE = {
    "King":   ("♔", "♚"),
    "Queen":  ("♕", "♛"),
    "Rook":   ("♖", "♜"),
    "Bishop": ("♗", "♝"),
    "Knight": ("♘", "♞"),
    "Pawn":   ("♙", "♟"),
}
#chessboard
def zeichne_schachbrett(spielstand, feldgrosse=60):
    breite = hohe = feldgrosse * 8
    bild = Image.new("RGB", (breite, hohe), "white")
    draw = ImageDraw.Draw(bild)

    farbe_hell = (240, 217, 181)
    farbe_dunkel = (181, 136, 99)

    for y in range(8):
        for x in range(8):
            farbe = farbe_hell if (x + y) % 2 == 0 else farbe_dunkel
            draw.rectangle([
                (x * feldgrosse, y * feldgrosse),
                ((x + 1) * feldgrosse, (y + 1) * feldgrosse)
            ], fill=farbe)

    try:
        font = ImageFont.truetype("DejaVuSans.ttf", int(feldgrosse * 0.8))
    except:
        font = ImageFont.load_default()

    for farbe_index, farbe in enumerate(spielstand):
        for figurenname, (x, y) in farbe:
            figurenname = figurenname.capitalize()

            symbol = FIGURE_UNICODE[figurenname][0 if farbe_index == 0 else 1]
            pos_x = (x - 1) * feldgrosse + feldgrosse // 5
            pos_y = (8 - y) * feldgrosse + feldgrosse // 8
            draw.text((pos_x, pos_y), symbol, fill="black", font=font)

    return bild

# --- GUI Viewer ---
class SchachbrettViewer:
    def __init__(self, root, positionen):
        self.root = root
        self.positionen = positionen
        self.index = 0

        # 💡 WICHTIG: Liste von Bildern speichern
        # Stellungen: Liste von Spielständen, z. B. [[weiß, schwarz], [weiß, schwarz], ...]
        self.pil_bilder = []
        self.tk_bilder = []

        for pos in positionen:
            pil_bild = zeichne_schachbrett(pos)
            self.pil_bilder.append(pil_bild)  # Optional: Zum späteren Speichern
            self.tk_bilder.append(ImageTk.PhotoImage(pil_bild))  # Muss separat sein

        self.label = tk.Label(root, image=self.tk_bilder[self.index])
        self.label.pack()

        root.bind("<Left>", self.zurueck)
        root.bind("<Right>", self.vor)
        root.bind("<Escape>", lambda e: root.destroy())
        self.update_title()

    def vor(self, event=None):
        if self.index < len(self.tk_bilder) - 1:
            self.index += 1
            self.label.config(image=self.tk_bilder[self.index])
            self.update_title()

    def zurueck(self, event=None):
        if self.index > 0:
            self.index -= 1
            self.label.config(image=self.tk_bilder[self.index])
            self.update_title()

    def update_title(self):
        self.root.title(f"Schachbrett {self.index + 1} / {len(self.tk_bilder)} – Pfeile ← → benutzen")


# --- Aufrufbare Funktion ---
def starte_viewer_mit_positionen(positionen):
    root = tk.Tk()
    viewer = SchachbrettViewer(root, positionen)
    root.mainloop()



#White Attacks


#attack of white Pawn
def attack_wPawn1(n):
    attack = []
    position = wPawn1(n)
    woccupied = white_occupied(n)
    boccupied = black_occupied(n)
    x = position[0]
    y = position[1]
    state = game_state_white[n][0][0]
    if state == "Pawn":
        if 9 - y > 1:
            newpos = (x, y + 1)
            if not((newpos in woccupied) or (newpos in boccupied)):
                attack.append(newpos)
        if 9 - y > 1:
            if 9 - x > 1:
                newpos = (x + 1, y + 1)
                if newpos in boccupied:
                    attack.append(newpos)
        if 9 - y > 1:
            if x > 1:
                newpos = (x - 1, y + 1)
                if newpos in boccupied:
                    attack.append(newpos)
        if y == 2:
            newpos = (x, y + 2)
            new2pos = (x, y+1)
            if not (newpos in woccupied or newpos in boccupied or new2pos in woccupied or new2pos in boccupied):
                attack.append(newpos)
    if state == "Queen":
        # move left down
        for i in range(1, 7):
            if x > i:
                if y > i:
                    newpos = (x - i, y - i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
                    # move right up
        for i in range(1, 7):
            if 9 - x > i:
                if 9 - y > i:
                    newpos = (x + i, y + i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
                    # move right down
        for i in range(1, 7):
            if y > i:
                if 9 - x > i:
                    newpos = (x + i, y - i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
        # move left up
        for i in range(1, 7):
            if 9 - y > i:
                if x > i:
                    newpos = (x - i, y + i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
        # move left
        for i in range(1, 7):
            if x > i:
                newpos = (x - i, y)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move right
        for i in range(1, 7):
            if 9 - x > i:
                newpos = (x + i, y)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move down
        for i in range(1, 7):
            if y > i:
                newpos = (x, y - i)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
        # move up
        for i in range(1, 7):
            if 9 - y > i:
                newpos = (x, y + i)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
    if state == "Knight":
        if x - 2 > 0:
            if y - 1 > 0:
                newpos = (x - 2, y - 1)
                if not (newpos in woccupied):
                    attack.append(newpos)
            if y + 1 < 9:
                newpos = (x - 2, y + 1)
                if not (newpos in woccupied):
                    attack.append(newpos)
        if x + 2 < 9:
            if y - 1 > 0:
                newpos = (x + 2, y - 1)
                if not (newpos in woccupied):
                    attack.append(newpos)
            if y + 1 < 9:
                newpos = (x + 2, y + 1)
                if not (newpos in woccupied):
                    attack.append(newpos)
        if x - 1 > 0:
            if y - 2 > 0:
                newpos = (x - 1, y - 2)
                if not (newpos in woccupied):
                    attack.append(newpos)
            if y + 2 < 9:
                newpos = (x - 1, y + 2)
                if not (newpos in woccupied):
                    attack.append(newpos)
        if x + 1 < 9:
            if y - 2 > 0:
                newpos = (x + 1, y - 2)
                if not (newpos in woccupied):
                    attack.append(newpos)
            if y + 2 < 9:
                newpos = (x + 1, y + 2)
                if not (newpos in woccupied):
                    attack.append(newpos)
    if state == "Rook":
        # move left
        for i in range(1, 7):
            if x - 1 > i:
                newpos = (x - i, y)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move right
        for i in range(1, 7):
            if 9 - x > i:
                newpos = (x + i, y)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move down
        for i in range(1, 7):
            if y - 1 > i:
                newpos = (x, y - i)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
        # move up
        for i in range(1, 7):
            if 9 - y > i:
                newpos = (x, y + i)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
    if state == "Bishop":
        #move left down
        for i in range(1, 7):
            if x > i:
                if y > i:
                    newpos = (x - i, y - i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
                    # move right up
        for i in range(1, 7):
            if 9 - x > i:
                if 9 - y > i:
                    newpos = (x + i, y + i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
                    # move right down
        for i in range(1, 7):
            if y > i:
                if 9 - x > i:
                    newpos = (x + i, y - i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
        # move left up
        for i in range(1, 7):
            if 9 - y > i:
                if x > i:
                    newpos = (x - i, y + i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
    return attack

#attack of white Pawn
def attack_wPawn2(n):
    attack = []
    position = wPawn2(n)
    woccupied = white_occupied(n)
    boccupied = black_occupied(n)
    x = position[0]
    y = position[1]
    state = game_state_white[n][1][0]
    if state == "Pawn":
        if 9 - y > 1:
            newpos = (x, y + 1)
            if not((newpos in woccupied) or (newpos in boccupied)):
                attack.append(newpos)
        if 9 - y > 1:
            if 9 - x > 1:
                newpos = (x + 1, y + 1)
                if newpos in boccupied:
                    attack.append(newpos)
        if 9 - y > 1:
            if x > 1:
                newpos = (x - 1, y + 1)
                if newpos in boccupied:
                    attack.append(newpos)
        if y == 2:
            newpos = (x, y + 2)
            new2pos = (x, y + 1)
            if not (newpos in woccupied or newpos in boccupied or new2pos in woccupied or new2pos in boccupied):
                attack.append(newpos)
    if state == "Queen":
        # move left down
        for i in range(1, 7):
            if x > i:
                if y  > i:
                    newpos = (x - i, y - i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
                    # move right up
        for i in range(1, 7):
            if 9 - x > i:
                if 9 - y > i:
                    newpos = (x + i, y + i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
                    # move right down
        for i in range(1, 7):
            if y > i:
                if 9 - x > i:
                    newpos = (x + i, y - i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
        # move left up
        for i in range(1, 7):
            if 9 - y > i:
                if x  > i:
                    newpos = (x - i, y + i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
        # move left
        for i in range(1, 7):
            if x  > i:
                newpos = (x - i, y)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move right
        for i in range(1, 7):
            if 9 - x > i:
                newpos = (x + i, y)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move down
        for i in range(1, 7):
            if y > i:
                newpos = (x, y - i)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
        # move up
        for i in range(1, 7):
            if 9 - y > i:
                newpos = (x, y + i)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
    if state == "Knight":
        if x - 2 > 0:
            if y - 1 > 0:
                newpos = (x - 2, y - 1)
                if not (newpos in woccupied):
                    attack.append(newpos)
            if y + 1 < 9:
                newpos = (x - 2, y + 1)
                if not (newpos in woccupied):
                    attack.append(newpos)
        if x + 2 < 9:
            if y - 1 > 0:
                newpos = (x + 2, y - 1)
                if not (newpos in woccupied):
                    attack.append(newpos)
            if y + 1 < 9:
                newpos = (x + 2, y + 1)
                if not (newpos in woccupied):
                    attack.append(newpos)
        if x - 1 > 0:
            if y - 2 > 0:
                newpos = (x - 1, y - 2)
                if not (newpos in woccupied):
                    attack.append(newpos)
            if y + 2 < 9:
                newpos = (x - 1, y + 2)
                if not (newpos in woccupied):
                    attack.append(newpos)
        if x + 1 < 9:
            if y - 2 > 0:
                newpos = (x + 1, y - 2)
                if not (newpos in woccupied):
                    attack.append(newpos)
            if y + 2 < 9:
                newpos = (x + 1, y + 2)
                if not (newpos in woccupied):
                    attack.append(newpos)
    if state == "Rook":
        # move left
        for i in range(1, 7):
            if x - 1 > i:
                newpos = (x - i, y)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move right
        for i in range(1, 7):
            if 9 - x > i:
                newpos = (x + i, y)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move down
        for i in range(1, 7):
            if y - 1 > i:
                newpos = (x, y - i)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
        # move up
        for i in range(1, 7):
            if 9 - y > i:
                newpos = (x, y + i)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
    if state == "Bishop":
        #move left down
        for i in range(1, 7):
            if x > i:
                if y > i:
                    newpos = (x - i, y - i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
                    # move right up
        for i in range(1, 7):
            if 9 - x > i:
                if 9 - y > i:
                    newpos = (x + i, y + i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
                    # move right down
        for i in range(1, 7):
            if y > i:
                if 9 - x > i:
                    newpos = (x + i, y - i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
        # move left up
        for i in range(1, 7):
            if 9 - y > i:
                if x > i:
                    newpos = (x - i, y + i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
    return attack

#attack of white Pawn
def attack_wPawn3(n):
    attack = []
    position = wPawn3(n)
    woccupied = white_occupied(n)
    boccupied = black_occupied(n)
    x = position[0]
    y = position[1]
    state = game_state_white[n][2][0]
    if state == "Pawn":
        if 9 - y > 1:
            newpos = (x, y + 1)
            if not((newpos in woccupied) or (newpos in boccupied)):
                attack.append(newpos)
        if 9 - y > 1:
            if 9 - x > 1:
                newpos = (x + 1, y + 1)
                if newpos in boccupied:
                    attack.append(newpos)
        if 9 - y > 1:
            if x - 1 > 1:
                newpos = (x - 1, y + 1)
                if newpos in boccupied:
                    attack.append(newpos)
        if y == 2:
            newpos = (x, y + 2)
            new2pos = (x, y + 1)
            if not (newpos in woccupied or newpos in boccupied or new2pos in woccupied or new2pos in boccupied):
                attack.append(newpos)
    if state == "Queen":
        # move left down
        for i in range(1, 7):
            if x > i:
                if y > i:
                    newpos = (x - i, y - i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
                    # move right up
        for i in range(1, 7):
            if 9 - x > i:
                if 9 - y > i:
                    newpos = (x + i, y + i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
                    # move right down
        for i in range(1, 7):
            if y > i:
                if 9 - x > i:
                    newpos = (x + i, y - i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
        # move left up
        for i in range(1, 7):
            if 9 - y > i:
                if x > i:
                    newpos = (x - i, y + i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
        # move left
        for i in range(1, 7):
            if x > i:
                newpos = (x - i, y)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move right
        for i in range(1, 7):
            if 9 - x > i:
                newpos = (x + i, y)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move down
        for i in range(1, 7):
            if y > i:
                newpos = (x, y - i)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
        # move up
        for i in range(1, 7):
            if 9 - y > i:
                newpos = (x, y + i)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
    if state == "Knight":
        if x - 2 > 0:
            if y - 1 > 0:
                newpos = (x - 2, y - 1)
                if not (newpos in woccupied):
                    attack.append(newpos)
            if y + 1 < 9:
                newpos = (x - 2, y + 1)
                if not (newpos in woccupied):
                    attack.append(newpos)
        if x + 2 < 9:
            if y - 1 > 0:
                newpos = (x + 2, y - 1)
                if not (newpos in woccupied):
                    attack.append(newpos)
            if y + 1 < 9:
                newpos = (x + 2, y + 1)
                if not (newpos in woccupied):
                    attack.append(newpos)
        if x - 1 > 0:
            if y - 2 > 0:
                newpos = (x - 1, y - 2)
                if not (newpos in woccupied):
                    attack.append(newpos)
            if y + 2 < 9:
                newpos = (x - 1, y + 2)
                if not (newpos in woccupied):
                    attack.append(newpos)
        if x + 1 < 9:
            if y - 2 > 0:
                newpos = (x + 1, y - 2)
                if not (newpos in woccupied):
                    attack.append(newpos)
            if y + 2 < 9:
                newpos = (x + 1, y + 2)
                if not (newpos in woccupied):
                    attack.append(newpos)
    if state == "Rook":
        # move left
        for i in range(1, 7):
            if x - 1 > i:
                newpos = (x - i, y)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move right
        for i in range(1, 7):
            if 9 - x > i:
                newpos = (x + i, y)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move down
        for i in range(1, 7):
            if y - 1 > i:
                newpos = (x, y - i)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
        # move up
        for i in range(1, 7):
            if 9 - y > i:
                newpos = (x, y + i)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
    if state == "Bishop":
        #move left down
        for i in range(1, 7):
            if x > i:
                if y  > i:
                    newpos = (x - i, y - i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
                    # move right up
        for i in range(1, 7):
            if 9 - x > i:
                if 9 - y > i:
                    newpos = (x + i, y + i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
                    # move right down
        for i in range(1, 7):
            if y > i:
                if 9 - x > i:
                    newpos = (x + i, y - i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
        # move left up
        for i in range(1, 7):
            if 9 - y > i:
                if x > i:
                    newpos = (x - i, y + i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
    return attack


#attack of white Pawn
def attack_wPawn4(n):
    attack = []
    position = wPawn4(n)
    woccupied = white_occupied(n)
    boccupied = black_occupied(n)
    x = position[0]
    y = position[1]
    state = game_state_white[n][3][0]
    if state == "Pawn":
        if 9 - y > 1:
            newpos = (x, y + 1)
            if not((newpos in woccupied) or (newpos in boccupied)):
                attack.append(newpos)
        if 9 - y > 1:
            if 9 - x > 1:
                newpos = (x + 1, y + 1)
                if newpos in boccupied:
                    attack.append(newpos)
        if 9 - y > 1:
            if x > 1:
                newpos = (x - 1, y + 1)
                if newpos in boccupied:
                    attack.append(newpos)
        if y == 2:
            newpos = (x, y + 2)
            new2pos = (x, y + 1)
            if not (newpos in woccupied or newpos in boccupied or new2pos in woccupied or new2pos in boccupied):
                attack.append(newpos)
    if state == "Queen":
        # move left down
        for i in range(1, 7):
            if x > i:
                if y > i:
                    newpos = (x - i, y - i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
                    # move right up
        for i in range(1, 7):
            if 9 - x > i:
                if 9 - y > i:
                    newpos = (x + i, y + i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
                    # move right down
        for i in range(1, 7):
            if y > i:
                if 9 - x > i:
                    newpos = (x + i, y - i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
        # move left up
        for i in range(1, 7):
            if 9 - y > i:
                if x > i:
                    newpos = (x - i, y + i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
        # move left
        for i in range(1, 7):
            if x > i:
                newpos = (x - i, y)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move right
        for i in range(1, 7):
            if 9 - x > i:
                newpos = (x + i, y)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move down
        for i in range(1, 7):
            if y > i:
                newpos = (x, y - i)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
        # move up
        for i in range(1, 7):
            if 9 - y > i:
                newpos = (x, y + i)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
    if state == "Knight":
        if x - 2 > 0:
            if y - 1 > 0:
                newpos = (x - 2, y - 1)
                if not (newpos in woccupied):
                    attack.append(newpos)
            if y + 1 < 9:
                newpos = (x - 2, y + 1)
                if not (newpos in woccupied):
                    attack.append(newpos)
        if x + 2 < 9:
            if y - 1 > 0:
                newpos = (x + 2, y - 1)
                if not (newpos in woccupied):
                    attack.append(newpos)
            if y + 1 < 9:
                newpos = (x + 2, y + 1)
                if not (newpos in woccupied):
                    attack.append(newpos)
        if x - 1 > 0:
            if y - 2 > 0:
                newpos = (x - 1, y - 2)
                if not (newpos in woccupied):
                    attack.append(newpos)
            if y + 2 < 9:
                newpos = (x - 1, y + 2)
                if not (newpos in woccupied):
                    attack.append(newpos)
        if x + 1 < 9:
            if y - 2 > 0:
                newpos = (x + 1, y - 2)
                if not (newpos in woccupied):
                    attack.append(newpos)
            if y + 2 < 9:
                newpos = (x + 1, y + 2)
                if not (newpos in woccupied):
                    attack.append(newpos)
    if state == "Rook":
        # move left
        for i in range(1, 7):
            if x > i:
                newpos = (x - i, y)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move right
        for i in range(1, 7):
            if 9 - x > i:
                newpos = (x + i, y)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move down
        for i in range(1, 7):
            if y > i:
                newpos = (x, y - i)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
        # move up
        for i in range(1, 7):
            if 9 - y > i:
                newpos = (x, y + i)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
    if state == "Bishop":
        #move left down
        for i in range(1, 7):
            if x > i:
                if y > i:
                    newpos = (x - i, y - i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
                    # move right up
        for i in range(1, 7):
            if 9 - x > i:
                if 9 - y > i:
                    newpos = (x + i, y + i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
                    # move right down
        for i in range(1, 7):
            if y > i:
                if 9 - x > i:
                    newpos = (x + i, y - i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
        # move left up
        for i in range(1, 7):
            if 9 - y > i:
                if x > i:
                    newpos = (x - i, y + i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
    return attack

#attack of white Pawn
def attack_wPawn5(n):
    attack = []
    position = wPawn5(n)
    woccupied = white_occupied(n)
    boccupied = black_occupied(n)
    x = position[0]
    y = position[1]
    state = game_state_white[n][4][0]
    if state == "Pawn":
        if 9 - y > 1:
            newpos = (x, y + 1)
            if not((newpos in woccupied) or (newpos in boccupied)):
                attack.append(newpos)
        if 9 - y > 1:
            if 9 - x > 1:
                newpos = (x + 1, y + 1)
                if newpos in boccupied:
                    attack.append(newpos)
        if 9 - y > 1:
            if x > 1:
                newpos = (x - 1, y + 1)
                if newpos in boccupied:
                    attack.append(newpos)
        if y == 2:
            newpos = (x, y + 2)
            new2pos = (x, y + 1)
            if not (newpos in woccupied or newpos in boccupied or new2pos in woccupied or new2pos in boccupied):
                attack.append(newpos)
    if state == "Queen":
        # move left down
        for i in range(1, 7):
            if x > i:
                if y > i:
                    newpos = (x - i, y - i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
                    # move right up
        for i in range(1, 7):
            if 9 - x > i:
                if 9 - y > i:
                    newpos = (x + i, y + i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
                    # move right down
        for i in range(1, 7):
            if y > i:
                if 9 - x > i:
                    newpos = (x + i, y - i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
        # move left up
        for i in range(1, 7):
            if 9 - y > i:
                if x > i:
                    newpos = (x - i, y + i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
        # move left
        for i in range(1, 7):
            if x > i:
                newpos = (x - i, y)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move right
        for i in range(1, 7):
            if 9 - x > i:
                newpos = (x + i, y)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move down
        for i in range(1, 7):
            if y > i:
                newpos = (x, y - i)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
        # move up
        for i in range(1, 7):
            if 9 - y > i:
                newpos = (x, y + i)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
    if state == "Knight":
        if x - 2 > 0:
            if y - 1 > 0:
                newpos = (x - 2, y - 1)
                if not (newpos in woccupied):
                    attack.append(newpos)
            if y + 1 < 9:
                newpos = (x - 2, y + 1)
                if not (newpos in woccupied):
                    attack.append(newpos)
        if x + 2 < 9:
            if y - 1 > 0:
                newpos = (x + 2, y - 1)
                if not (newpos in woccupied):
                    attack.append(newpos)
            if y + 1 < 9:
                newpos = (x + 2, y + 1)
                if not (newpos in woccupied):
                    attack.append(newpos)
        if x - 1 > 0:
            if y - 2 > 0:
                newpos = (x - 1, y - 2)
                if not (newpos in woccupied):
                    attack.append(newpos)
            if y + 2 < 9:
                newpos = (x - 1, y + 2)
                if not (newpos in woccupied):
                    attack.append(newpos)
        if x + 1 < 9:
            if y - 2 > 0:
                newpos = (x + 1, y - 2)
                if not (newpos in woccupied):
                    attack.append(newpos)
            if y + 2 < 9:
                newpos = (x + 1, y + 2)
                if not (newpos in woccupied):
                    attack.append(newpos)
    if state == "Rook":
        # move left
        for i in range(1, 7):
            if x - 1 > i:
                newpos = (x - i, y)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move right
        for i in range(1, 7):
            if 9 - x > i:
                newpos = (x + i, y)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move down
        for i in range(1, 7):
            if y - 1 > i:
                newpos = (x, y - i)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
        # move up
        for i in range(1, 7):
            if 9 - y > i:
                newpos = (x, y + i)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
    if state == "Bishop":
        #move left down
        for i in range(1, 7):
            if x > i:
                if y > i:
                    newpos = (x - i, y - i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
                    # move right up
        for i in range(1, 7):
            if 9 - x > i:
                if 9 - y > i:
                    newpos = (x + i, y + i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
                    # move right down
        for i in range(1, 7):
            if y > i:
                if 9 - x > i:
                    newpos = (x + i, y - i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
        # move left up
        for i in range(1, 7):
            if 9 - y > i:
                if x > i:
                    newpos = (x - i, y + i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
    return attack

#attack of white Pawn
def attack_wPawn6(n):
    attack = []
    position = wPawn6(n)
    woccupied = white_occupied(n)
    boccupied = black_occupied(n)
    x = position[0]
    y = position[1]
    state = game_state_white[n][5][0]
    if state == "Pawn":
        if 9 - y > 1:
            newpos = (x, y + 1)
            if not((newpos in woccupied) or (newpos in boccupied)):
                attack.append(newpos)
        if 9 - y > 1:
            if 9 - x > 1:
                newpos = (x + 1, y + 1)
                if newpos in boccupied:
                    attack.append(newpos)
        if 9 - y > 1:
            if x > 1:
                newpos = (x - 1, y + 1)
                if newpos in boccupied:
                    attack.append(newpos)
        if y == 2:
            newpos = (x, y + 2)
            new2pos = (x, y + 1)
            if not (newpos in woccupied or newpos in boccupied or new2pos in woccupied or new2pos in boccupied):
                attack.append(newpos)
    if state == "Queen":
        # move left down
        for i in range(1, 7):
            if x > i:
                if y > i:
                    newpos = (x - i, y - i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
                    # move right up
        for i in range(1, 7):
            if 9 - x > i:
                if 9 - y > i:
                    newpos = (x + i, y + i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
                    # move right down
        for i in range(1, 7):
            if y > i:
                if 9 - x > i:
                    newpos = (x + i, y - i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
        # move left up
        for i in range(1, 7):
            if 9 - y > i:
                if x > i:
                    newpos = (x - i, y + i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
        # move left
        for i in range(1, 7):
            if x > i:
                newpos = (x - i, y)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move right
        for i in range(1, 7):
            if 9 - x > i:
                newpos = (x + i, y)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move down
        for i in range(1, 7):
            if y > i:
                newpos = (x, y - i)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
        # move up
        for i in range(1, 7):
            if 9 - y > i:
                newpos = (x, y + i)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
    if state == "Knight":
        if x - 2 > 0:
            if y - 1 > 0:
                newpos = (x - 2, y - 1)
                if not (newpos in woccupied):
                    attack.append(newpos)
            if y + 1 < 9:
                newpos = (x - 2, y + 1)
                if not (newpos in woccupied):
                    attack.append(newpos)
        if x + 2 < 9:
            if y - 1 > 0:
                newpos = (x + 2, y - 1)
                if not (newpos in woccupied):
                    attack.append(newpos)
            if y + 1 < 9:
                newpos = (x + 2, y + 1)
                if not (newpos in woccupied):
                    attack.append(newpos)
        if x - 1 > 0:
            if y - 2 > 0:
                newpos = (x - 1, y - 2)
                if not (newpos in woccupied):
                    attack.append(newpos)
            if y + 2 < 9:
                newpos = (x - 1, y + 2)
                if not (newpos in woccupied):
                    attack.append(newpos)
        if x + 1 < 9:
            if y - 2 > 0:
                newpos = (x + 1, y - 2)
                if not (newpos in woccupied):
                    attack.append(newpos)
            if y + 2 < 9:
                newpos = (x + 1, y + 2)
                if not (newpos in woccupied):
                    attack.append(newpos)
    if state == "Rook":
        # move left
        for i in range(1, 7):
            if x > i:
                newpos = (x - i, y)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move right
        for i in range(1, 7):
            if 9 - x > i:
                newpos = (x + i, y)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move down
        for i in range(1, 7):
            if y > i:
                newpos = (x, y - i)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
        # move up
        for i in range(1, 7):
            if 9 - y > i:
                newpos = (x, y + i)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
    if state == "Bishop":
        #move left down
        for i in range(1, 7):
            if x > i:
                if y > i:
                    newpos = (x - i, y - i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
                    # move right up
        for i in range(1, 7):
            if 9 - x > i:
                if 9 - y > i:
                    newpos = (x + i, y + i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
                    # move right down
        for i in range(1, 7):
            if y > i:
                if 9 - x > i:
                    newpos = (x + i, y - i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
        # move left up
        for i in range(1, 7):
            if 9 - y > i:
                if x > i:
                    newpos = (x - i, y + i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
    return attack


#attack of white Pawn
def attack_wPawn7(n):
    attack = []
    position = wPawn7(n)
    woccupied = white_occupied(n)
    boccupied = black_occupied(n)
    x = position[0]
    y = position[1]
    state = game_state_white[n][6][0]
    if state == "Pawn":
        if 9 - y > 1:
            newpos = (x, y + 1)
            if not((newpos in woccupied) or (newpos in boccupied)):
                attack.append(newpos)
        if 9 - y > 1:
            if 9 - x > 1:
                newpos = (x + 1, y + 1)
                if newpos in boccupied:
                    attack.append(newpos)
        if 9 - y > 1:
            if x > 1:
                newpos = (x - 1, y + 1)
                if newpos in boccupied:
                    attack.append(newpos)
        if y == 2:
            newpos = (x, y + 2)
            new2pos = (x, y + 1)
            if not (newpos in woccupied or newpos in boccupied or new2pos in woccupied or new2pos in boccupied):
                attack.append(newpos)
    if state == "Queen":
        # move left down
        for i in range(1, 7):
            if x > i:
                if y > i:
                    newpos = (x - i, y - i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
                    # move right up
        for i in range(1, 7):
            if 9 - x > i:
                if 9 - y > i:
                    newpos = (x + i, y + i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
                    # move right down
        for i in range(1, 7):
            if y > i:
                if 9 - x > i:
                    newpos = (x + i, y - i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
        # move left up
        for i in range(1, 7):
            if 9 - y > i:
                if x > i:
                    newpos = (x - i, y + i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
        # move left
        for i in range(1, 7):
            if x > i:
                newpos = (x - i, y)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move right
        for i in range(1, 7):
            if 9 - x > i:
                newpos = (x + i, y)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move down
        for i in range(1, 7):
            if y > i:
                newpos = (x, y - i)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
        # move up
        for i in range(1, 7):
            if 9 - y > i:
                newpos = (x, y + i)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
    if state == "Knight":
        if x - 2 > 0:
            if y - 1 > 0:
                newpos = (x - 2, y - 1)
                if not (newpos in woccupied):
                    attack.append(newpos)
            if y + 1 < 9:
                newpos = (x - 2, y + 1)
                if not (newpos in woccupied):
                    attack.append(newpos)
        if x + 2 < 9:
            if y - 1 > 0:
                newpos = (x + 2, y - 1)
                if not (newpos in woccupied):
                    attack.append(newpos)
            if y + 1 < 9:
                newpos = (x + 2, y + 1)
                if not (newpos in woccupied):
                    attack.append(newpos)
        if x - 1 > 0:
            if y - 2 > 0:
                newpos = (x - 1, y - 2)
                if not (newpos in woccupied):
                    attack.append(newpos)
            if y + 2 < 9:
                newpos = (x - 1, y + 2)
                if not (newpos in woccupied):
                    attack.append(newpos)
        if x + 1 < 9:
            if y - 2 > 0:
                newpos = (x + 1, y - 2)
                if not (newpos in woccupied):
                    attack.append(newpos)
            if y + 2 < 9:
                newpos = (x + 1, y + 2)
                if not (newpos in woccupied):
                    attack.append(newpos)
    if state == "Rook":
        # move left
        for i in range(1, 7):
            if x > i:
                newpos = (x - i, y)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move right
        for i in range(1, 7):
            if 9 - x > i:
                newpos = (x + i, y)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move down
        for i in range(1, 7):
            if y > i:
                newpos = (x, y - i)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
        # move up
        for i in range(1, 7):
            if 9 - y > i:
                newpos = (x, y + i)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
    if state == "Bishop":
        #move left down
        for i in range(1, 7):
            if x > i:
                if y > i:
                    newpos = (x - i, y - i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
                    # move right up
        for i in range(1, 7):
            if 9 - x > i:
                if 9 - y > i:
                    newpos = (x + i, y + i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
                    # move right down
        for i in range(1, 7):
            if y > i:
                if 9 - x > i:
                    newpos = (x + i, y - i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
        # move left up
        for i in range(1, 7):
            if 9 - y > i:
                if x > i:
                    newpos = (x - i, y + i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
    return attack

#attack of white Pawn
def attack_wPawn8(n):
    attack = []
    position = wPawn8(n)
    woccupied = white_occupied(n)
    boccupied = black_occupied(n)
    x = position[0]
    y = position[1]
    state = game_state_white[n][7][0]
    if state == "Pawn":
        if 9 - y > 1:
            newpos = (x, y + 1)
            if not((newpos in woccupied) or (newpos in boccupied)):
                attack.append(newpos)
        if 9 - y > 1:
            if 9 - x > 1:
                newpos = (x + 1, y + 1)
                if newpos in boccupied:
                    attack.append(newpos)
        if 9 - y > 1:
            if x > 1:
                newpos = (x - 1, y + 1)
                if newpos in boccupied:
                    attack.append(newpos)
        if y == 2:
            newpos = (x, y + 2)
            new2pos = (x, y + 1)
            if not (newpos in woccupied or newpos in boccupied or new2pos in woccupied or new2pos in boccupied):
                attack.append(newpos)
    if state == "Queen":
        # move left down
        for i in range(1, 7):
            if x > i:
                if y > i:
                    newpos = (x - i, y - i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
                    # move right up
        for i in range(1, 7):
            if 9 - x > i:
                if 9 - y > i:
                    newpos = (x + i, y + i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
                    # move right down
        for i in range(1, 7):
            if y > i:
                if 9 - x > i:
                    newpos = (x + i, y - i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
        # move left up
        for i in range(1, 7):
            if 9 - y > i:
                if x > i:
                    newpos = (x - i, y + i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
        # move left
        for i in range(1, 7):
            if x > i:
                newpos = (x - i, y)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move right
        for i in range(1, 7):
            if 9 - x > i:
                newpos = (x + i, y)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move down
        for i in range(1, 7):
            if y > i:
                newpos = (x, y - i)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
        # move up
        for i in range(1, 7):
            if 9 - y > i:
                newpos = (x, y + i)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
    if state == "Knight":
        if x - 2 > 0:
            if y - 1 > 0:
                newpos = (x - 2, y - 1)
                if not (newpos in woccupied):
                    attack.append(newpos)
            if y + 1 < 9:
                newpos = (x - 2, y + 1)
                if not (newpos in woccupied):
                    attack.append(newpos)
        if x + 2 < 9:
            if y - 1 > 0:
                newpos = (x + 2, y - 1)
                if not (newpos in woccupied):
                    attack.append(newpos)
            if y + 1 < 9:
                newpos = (x + 2, y + 1)
                if not (newpos in woccupied):
                    attack.append(newpos)
        if x - 1 > 0:
            if y - 2 > 0:
                newpos = (x - 1, y - 2)
                if not (newpos in woccupied):
                    attack.append(newpos)
            if y + 2 < 9:
                newpos = (x - 1, y + 2)
                if not (newpos in woccupied):
                    attack.append(newpos)
        if x + 1 < 9:
            if y - 2 > 0:
                newpos = (x + 1, y - 2)
                if not (newpos in woccupied):
                    attack.append(newpos)
            if y + 2 < 9:
                newpos = (x + 1, y + 2)
                if not (newpos in woccupied):
                    attack.append(newpos)
    if state == "Rook":
        # move left
        for i in range(1, 7):
            if x > i:
                newpos = (x - i, y)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move right
        for i in range(1, 7):
            if 9 - x > i:
                newpos = (x + i, y)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move down
        for i in range(1, 7):
            if y > i:
                newpos = (x, y - i)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
        # move up
        for i in range(1, 7):
            if 9 - y > i:
                newpos = (x, y + i)
                if not (newpos in woccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
    if state == "Bishop":
        #move left down
        for i in range(1, 7):
            if x > i:
                if y > i:
                    newpos = (x - i, y - i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
                    # move right up
        for i in range(1, 7):
            if 9 - x > i:
                if 9 - y > i:
                    newpos = (x + i, y + i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
                    # move right down
        for i in range(1, 7):
            if y > i:
                if 9 - x > i:
                    newpos = (x + i, y - i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
        # move left up
        for i in range(1, 7):
            if 9 - y > i:
                if x > i:
                    newpos = (x - i, y + i)
                    if not (newpos in woccupied):
                        attack.append(newpos)
                        if newpos in boccupied:
                            break
                    else:
                        break
    return attack


#attack of first white rook
def attack_wRook1(n):
    attack = []
    position = wRook1(n)
    woccupied = white_occupied(n)
    boccupied = black_occupied(n)
    x = position[0]
    y = position[1]
    #move left
    for i in range(1, 7):
        if x > i:
            newpos = (x-i, y)
            if not(newpos in woccupied):
                attack.append(newpos)
                if newpos in boccupied:
                    break
            else: break
            #move right
    for i in range(1, 7):
        if 9-x > i:
            newpos = (x+i, y)
            if not(newpos in woccupied):
                attack.append(newpos)
                if newpos in boccupied:
                    break
            else: break
            #move down
    for i in range(1, 7):
        if y > i:
            newpos = (x, y-i)
            if not(newpos in woccupied):
                attack.append(newpos)
                if newpos in boccupied:
                    break
            else: break
    #move up
    for i in range(1, 7):
        if 9-y > i:
            newpos = (x, y+i)
            if not (newpos in woccupied):
                attack.append(newpos)
                if newpos in boccupied:
                    break
            else:
                break
    return attack








#attack of first white Knight
def attack_wKnight1(n):
    attack = []
    position = wKnight1(n)
    woccupied = white_occupied(n)
    x = position[0]
    y = position[1]
    if x-2 > 0:
        if y-1 > 0:
            newpos = (x-2, y-1)
            if not(newpos in woccupied):
                attack.append(newpos)
        if y+1 < 9:
            newpos = (x-2, y+1)
            if not(newpos in woccupied):
                attack.append(newpos)
    if x+2 < 9:
        if y-1 > 0:
            newpos = (x+2, y-1)
            if not(newpos in woccupied):
                attack.append(newpos)
        if y+1 < 9:
            newpos = (x+2, y+1)
            if not(newpos in woccupied):
                attack.append(newpos)
    if x-1 > 0:
        if y-2 > 0:
            newpos = (x-1, y-2)
            if not(newpos in woccupied):
                attack.append(newpos)
        if y+2 < 9:
            newpos = (x-1, y+2)
            if not(newpos in woccupied):
                attack.append(newpos)
    if x+1 < 9:
        if y-2 > 0:
            newpos = (x+1, y-2)
            if not(newpos in woccupied):
                attack.append(newpos)
        if y+2 < 9:
            newpos = (x+1, y+2)
            if not(newpos in woccupied):
                attack.append(newpos)
    return attack





#attack of the first white Bishop
def attack_wBishop1(n):
    attack = []
    position = wBishop1(n)
    woccupied = white_occupied(n)
    boccupied = black_occupied(n)
    x = position[0]
    y = position[1]
    #move left down
    for i in range(1, 7):
        if x > i:
          if y > i:
            newpos = (x-i, y-i)
            if not(newpos in woccupied):
                attack.append(newpos)
                if newpos in boccupied:
                    break
            else: break
            #move right up
    for i in range(1, 7):
        if 9-x > i:
          if 9-y > i:
            newpos = (x+i, y+i)
            if not(newpos in woccupied):
                attack.append(newpos)
                if newpos in boccupied:
                    break
            else: break
            #move right down
    for i in range(1, 7):
        if y > i:
          if 9 - x > i:
            newpos = (x+i, y-i)
            if not(newpos in woccupied):
                attack.append(newpos)
                if newpos in boccupied:
                    break
            else: break
    #move left up
    for i in range(1, 7):
        if 9-y > i:
          if x > i:
            newpos = (x-i, y+i)
            if not (newpos in woccupied):
                attack.append(newpos)
                if newpos in boccupied:
                    break
            else:
                break
    return attack


#attack of the White Queen
def attack_wQueen(n):
    attack = []
    position = wQueen(n)
    woccupied = white_occupied(n)
    boccupied = black_occupied(n)
    x = position[0]
    y = position[1]
    #move left down
    for i in range(1, 7):
        if x > i:
          if y > i:
            newpos = (x-i, y-i)
            if not(newpos in woccupied):
                attack.append(newpos)
                if newpos in boccupied:
                    break
            else: break
            #move right up
    for i in range(1, 7):
        if 9-x > i:
          if 9-y > i:
            newpos = (x+i, y+i)
            if not(newpos in woccupied):
                attack.append(newpos)
                if newpos in boccupied:
                    break
            else: break
            #move right down
    for i in range(1, 7):
        if y > i:
          if 9 - x > i:
            newpos = (x+i, y-i)
            if not(newpos in woccupied):
                attack.append(newpos)
                if newpos in boccupied:
                    break
            else: break
    #move left up
    for i in range(1, 7):
        if 9-y > i:
          if x > i:
            newpos = (x-i, y+i)
            if not (newpos in woccupied):
                attack.append(newpos)
                if newpos in boccupied:
                    break
            else:
                break
    #move left
    for i in range(1, 7):
        if x > i:
            newpos = (x-i, y)
            if not(newpos in woccupied):
                attack.append(newpos)
                if newpos in boccupied:
                    break
            else: break
            #move right
    for i in range(1, 7):
        if 9-x > i:
            newpos = (x+i, y)
            if not(newpos in woccupied):
                attack.append(newpos)
                if newpos in boccupied:
                    break
            else: break
            #move down
    for i in range(1, 7):
        if y > i:
            newpos = (x, y-i)
            if not(newpos in woccupied):
                attack.append(newpos)
                if newpos in boccupied:
                    break
            else: break
    #move up
    for i in range(1, 7):
        if 9-y > i:
            newpos = (x, y+i)
            if not (newpos in woccupied):
                attack.append(newpos)
                if newpos in boccupied:
                    break
            else:
                break
    return attack




#attack of the white King
def attack_wKing(n):
    attack = []
    position = wKing(n)
    woccupied = white_occupied(n)
    boccupied = black_occupied(n)
    x = position[0]
    y = position[1]
    #move left down
    if x > 1:
        if y > 1:
            newpos = (x-1, y-1)
            if not(newpos in woccupied):
                attack.append(newpos)
            #move right up
    if 9-x > 1:
        if 9-y > 1:
            newpos = (x+1, y+1)
            if not(newpos in woccupied):
                attack.append(newpos)
            #move right down
    if y > 1:
        if 9 - x > 1:
            newpos = (x+1, y-1)
            if not(newpos in woccupied):
                attack.append(newpos)
    #move left up
    if 9-y > 1:
        if x > 1:
            newpos = (x-1, y+1)
            if not (newpos in woccupied):
                attack.append(newpos)
    #move left
    if x > 1:
        newpos = (x-1, y)
        if not(newpos in woccupied):
                attack.append(newpos)
            #move right
    if 9-x > 1:
        newpos = (x+1, y)
        if not(newpos in woccupied):
                attack.append(newpos)
            #move down
    if y > 1:
        newpos = (x, y)
        if not(newpos in woccupied):
                attack.append(newpos)
    #move up
    if 9-y > 1:
        newpos = (x, y+1)
        if not (newpos in woccupied):
                attack.append(newpos)
    return attack




#attack of the second white Bishop
def attack_wBishop2(n):
    attack = []
    position = wBishop2(n)
    woccupied = white_occupied(n)
    boccupied = black_occupied(n)
    x = position[0]
    y = position[1]
    #move left down
    for i in range(1, 7):
        if x > i:
          if y > i:
            newpos = (x-i, y-i)
            if not(newpos in woccupied):
                attack.append(newpos)
                if newpos in boccupied:
                    break
            else: break
            #move right up
    for i in range(1, 7):
        if 9-x > i:
          if 9-y > i:
            newpos = (x+i, y+i)
            if not(newpos in woccupied):
                attack.append(newpos)
                if newpos in boccupied:
                    break
            else: break
            #move right down
    for i in range(1, 7):
        if y > i:
          if 9 - x > i:
            newpos = (x+i, y-i)
            if not(newpos in woccupied):
                attack.append(newpos)
                if newpos in boccupied:
                    break
            else: break
    #move left up
    for i in range(1, 7):
        if 9-y > i:
          if x > i:
            newpos = (x-i, y+i)
            if not (newpos in woccupied):
                attack.append(newpos)
                if newpos in boccupied:
                    break
            else:
                break
    return attack





#attack of second white Knight
def attack_wKnight2(n):
    attack = []
    position = wKnight2(n)
    woccupied = white_occupied(n)
    x = position[0]
    y = position[1]
    if x-2 > 0:
        if y-1 > 0:
            newpos = (x-2, y-1)
            if not(newpos in woccupied):
                attack.append(newpos)
        if y+1 < 9:
            newpos = (x-2, y+1)
            if not(newpos in woccupied):
                attack.append(newpos)
    if x+2 < 9:
        if y-1 > 0:
            newpos = (x+2, y-1)
            if not(newpos in woccupied):
                attack.append(newpos)
        if y+1 < 9:
            newpos = (x+2, y+1)
            if not(newpos in woccupied):
                attack.append(newpos)
    if x-1 > 0:
        if y-2 > 0:
            newpos = (x-1, y-2)
            if not(newpos in woccupied):
                attack.append(newpos)
        if y+2 < 9:
            newpos = (x-1, y+2)
            if not(newpos in woccupied):
                attack.append(newpos)
    if x+1 < 9:
        if y-2 > 0:
            newpos = (x+1, y-2)
            if not(newpos in woccupied):
                attack.append(newpos)
        if y+2 < 9:
            newpos = (x+1, y+2)
            if not(newpos in woccupied):
                attack.append(newpos)
    return attack










#attack of second white rook
def attack_wRook2(n):
    attack = []
    position = wRook2(n)
    woccupied = white_occupied(n)
    boccupied = black_occupied(n)
    x = position[0]
    y = position[1]
    #move left
    for i in range(1, 7):
        if x > i:
            newpos = (x-i, y)
            if not(newpos in woccupied):
                attack.append(newpos)
                if newpos in boccupied:
                    break
            else: break
            #move right
    for i in range(1, 7):
        if 9-x > i:
            newpos = (x+i, y)
            if not(newpos in woccupied):
                attack.append(newpos)
                if newpos in boccupied:
                    break
            else: break
            #move down
    for i in range(1, 7):
        if y > i:
            newpos = (x, y-i)
            if not(newpos in woccupied):
                attack.append(newpos)
                if newpos in boccupied:
                    break
            else: break
    #move up
    for i in range(1, 7):
        if 9-y > i:
            newpos = (x, y+i)
            if not (newpos in woccupied):
                attack.append(newpos)
                if newpos in boccupied:
                    break
            else:
                break
    return attack






























#Black Attacks


#attack of first black rook
def attack_bRook1(n):
    attack = []
    position = bRook1(n)
    woccupied = white_occupied(n)
    boccupied = black_occupied(n)
    x = position[0]
    y = position[1]
    #move left
    for i in range(1, 7):
        if x > i:
            newpos = (x-i, y)
            if not(newpos in boccupied):
                attack.append(newpos)
                if newpos in woccupied:
                    break
            else: break
            #move right
    for i in range(1, 7):
        if 9-x > i:
            newpos = (x+i, y)
            if not(newpos in boccupied):
                attack.append(newpos)
                if newpos in woccupied:
                    break
            else: break
            #move down
    for i in range(1, 7):
        if y > i:
            newpos = (x, y-i)
            if not(newpos in boccupied):
                attack.append(newpos)
                if newpos in woccupied:
                    break
            else: break
    #move up
    for i in range(1, 7):
        if 9-y > i:
            newpos = (x, y+i)
            if not (newpos in boccupied):
                attack.append(newpos)
                if newpos in woccupied:
                    break
            else:
                break
    return attack





#attack of first black Knight
def attack_bKnight1(n):
    attack = []
    position = bKnight1(n)
    boccupied = black_occupied(n)
    x = position[0]
    y = position[1]
    if x-2 > 0:
        if y-1 > 0:
            newpos = (x-2, y-1)
            if not(newpos in boccupied):
                attack.append(newpos)
        if y+1 < 9:
            newpos = (x-2, y+1)
            if not(newpos in boccupied):
                attack.append(newpos)
    if x+2 < 9:
        if y-1 > 0:
            newpos = (x+2, y-1)
            if not(newpos in boccupied):
                attack.append(newpos)
        if y+1 < 9:
            newpos = (x+2, y+1)
            if not(newpos in boccupied):
                attack.append(newpos)
    if x-1 > 0:
        if y-2 > 0:
            newpos = (x-1, y-2)
            if not(newpos in boccupied):
                attack.append(newpos)
        if y+2 < 9:
            newpos = (x-1, y+2)
            if not(newpos in boccupied):
                attack.append(newpos)
    if x+1 < 9:
        if y-2 > 0:
            newpos = (x+1, y-2)
            if not(newpos in boccupied):
                attack.append(newpos)
        if y+2 < 9:
            newpos = (x+1, y+2)
            if not(newpos in boccupied):
                attack.append(newpos)
    return attack





#attack of the first black Bishop
def attack_bBishop1(n):
    attack = []
    position = bBishop1(n)
    woccupied = white_occupied(n)
    boccupied = black_occupied(n)
    x = position[0]
    y = position[1]
    #move left down
    for i in range(1, 7):
        if x > i:
          if y > i:
            newpos = (x-i, y-i)
            if not(newpos in boccupied) or newpos == wKing(n):
                attack.append(newpos)
                if newpos in woccupied:
                    break
            else:
                break
            #move right up
    for i in range(1, 7):
        if 9-x > i:
          if 9-y > i:
            newpos = (x+i, y+i)
            if not(newpos in boccupied):
                attack.append(newpos)
                if newpos in woccupied:
                    break
            else: break
            #move right down
    for i in range(1, 7):
        if y > i:
          if 9 - x > i:
            newpos = (x+i, y-i)
            if not(newpos in boccupied):
                attack.append(newpos)
                if newpos in woccupied:
                    break
            else: break
    #move left up
    for i in range(1, 7):
        if 9-y > i:
          if x > i:
            newpos = (x-i, y+i)
            if not (newpos in boccupied):
                attack.append(newpos)
                if newpos in woccupied:
                    break
            else:
                break
    return attack



#attack of the black Queen - woccupied and boccupied swapped
def attack_bQueen(n):
    attack = []
    position = bQueen(n)
    woccupied = white_occupied(n)
    boccupied = black_occupied(n)
    x = position[0]
    y = position[1]
    #move left down
    for i in range(1, 7):
        if x > i:
          if y > i:
            newpos = (x-i, y-i)
            if not(newpos in boccupied):
                attack.append(newpos)
                if newpos in woccupied:
                    break
            else: break
            #move right up
    for i in range(1, 7):
        if 9-x > i:
          if 9-y > i:
            newpos = (x+i, y+i)
            if not(newpos in boccupied):
                attack.append(newpos)
                if newpos in woccupied:
                    break
            else: break
            #move right down
    for i in range(1, 7):
        if y > i:
          if 9 - x > i:
            newpos = (x+i, y-i)
            if not(newpos in boccupied):
                attack.append(newpos)
                if newpos in woccupied:
                    break
            else: break
    #move left up
    for i in range(1, 7):
        if 9-y > i:
          if x > i:
            newpos = (x-i, y+i)
            if not (newpos in boccupied):
                attack.append(newpos)
                if newpos in woccupied:
                    break
            else:
                break
    #move left
    for i in range(1, 7):
        if x > i:
            newpos = (x-i, y)
            if not(newpos in boccupied):
                attack.append(newpos)
                if newpos in woccupied:
                    break
            else: break
            #move right
    for i in range(1, 7):
        if 9-x > i:
            newpos = (x+i, y)
            if not(newpos in boccupied):
                attack.append(newpos)
                if newpos in woccupied:
                    break
            else: break
            #move down
    for i in range(1, 7):
        if y > i:
            newpos = (x, y-i)
            if not(newpos in boccupied):
                attack.append(newpos)
                if newpos in woccupied:
                    break
            else: break
    #move up
    for i in range(1, 7):
        if 9-y > i:
            newpos = (x, y+i)
            if not (newpos in boccupied):
                attack.append(newpos)
                if newpos in woccupied:
                    break
            else:
                break
    return attack






#attack of the black King
def attack_bKing(n):
    attack = []
    position = bKing(n)
    boccupied = white_occupied(n)
    woccupied = black_occupied(n)
    x = position[0]
    y = position[1]
    #move left down
    if x > 1:
        if y > 1:
            newpos = (x-1, y-1)
            if not(newpos in woccupied):
                attack.append(newpos)
            #move right up
    if 9-x > 1:
        if 9-y > 1:
            newpos = (x+1, y+1)
            if not(newpos in woccupied):
                attack.append(newpos)
            #move right down
    if y > 1:
        if 9 - x > 1:
            newpos = (x+1, y-1)
            if not(newpos in woccupied):
                attack.append(newpos)
    #move left up
    if 9-y > 1:
        if x > 1:
            newpos = (x-1, y+1)
            if not (newpos in woccupied):
                attack.append(newpos)
    #move left
    if x > 1:
        newpos = (x-1, y)
        if not(newpos in woccupied):
                attack.append(newpos)
            #move right
    if 9-x > 1:
        newpos = (x+1, y)
        if not(newpos in woccupied):
                attack.append(newpos)
            #move down
    if y > 1:
        newpos = (x, y-1)
        if not(newpos in woccupied):
                attack.append(newpos)
    #move up
    if 9-y > 1:
        newpos = (x, y+1)
        if not (newpos in woccupied):
                attack.append(newpos)
    return attack





#attack of the second black Bishop
def attack_bBishop2(n):
    attack = []
    position = bBishop2(n)
    woccupied = white_occupied(n)
    boccupied = black_occupied(n)
    x = position[0]
    y = position[1]
    #move left down
    for i in range(1, 7):
        if x > i:
          if y > i:
            newpos = (x-i, y-i)
            if not(newpos in boccupied):
                attack.append(newpos)
                if newpos in woccupied:
                    break
            else: break
            #move right up
    for i in range(1, 7):
        if 9-x > i:
          if 9-y > i:
            newpos = (x+i, y+i)
            if not(newpos in boccupied):
                attack.append(newpos)
                if newpos in woccupied:
                    break
            else: break
            #move right down
    for i in range(1, 7):
        if y > i:
          if 9 - x > i:
            newpos = (x+i, y-i)
            if not(newpos in boccupied):
                attack.append(newpos)
                if newpos in woccupied:
                    break
            else: break
    #move left up
    for i in range(1, 7):
        if 9-y > i:
          if x > i:
            newpos = (x-i, y+i)
            if not (newpos in boccupied):
                attack.append(newpos)
                if newpos in woccupied:
                    break
            else:
                break
    return attack


#attack of second black Knight
def attack_bKnight2(n):
    attack = []
    position = bKnight2(n)
    boccupied = black_occupied(n)
    x = position[0]
    y = position[1]
    if x-2 > 0:
        if y-1 > 0:
            newpos = (x-2, y-1)
            if not(newpos in boccupied):
                attack.append(newpos)
        if y+1 < 9:
            newpos = (x-2, y+1)
            if not(newpos in boccupied):
                attack.append(newpos)
    if x+2 < 9:
        if y-1 > 0:
            newpos = (x+2, y-1)
            if not(newpos in boccupied):
                attack.append(newpos)
        if y+1 < 9:
            newpos = (x+2, y+1)
            if not(newpos in boccupied):
                attack.append(newpos)
    if x-1 > 0:
        if y-2 > 0:
            newpos = (x-1, y-2)
            if not(newpos in boccupied):
                attack.append(newpos)
        if y+2 < 9:
            newpos = (x-1, y+2)
            if not(newpos in boccupied):
                attack.append(newpos)
    if x+1 < 9:
        if y-2 > 0:
            newpos = (x+1, y-2)
            if not(newpos in boccupied):
                attack.append(newpos)
        if y+2 < 9:
            newpos = (x+1, y+2)
            if not(newpos in boccupied):
                attack.append(newpos)
    return attack





#attack of the second black rook

def attack_bRook2(n):
    attack = []
    position = bRook2(n)
    woccupied = white_occupied(n)
    boccupied = black_occupied(n)
    x = position[0]
    y = position[1]
    #move left
    for i in range(1, 7):
        if x > i:
            newpos = (x-i, y)
            if not(newpos in boccupied):
                attack.append(newpos)
                if newpos in woccupied:
                    break
            else: break
            #move right
    for i in range(1, 7):
        if 9-x > i:
            newpos = (x+i, y)
            if not(newpos in boccupied):
                attack.append(newpos)
                if newpos in woccupied:
                    break
            else: break
            #move down
    for i in range(1, 7):
        if y > i:
            newpos = (x, y-i)
            if not(newpos in boccupied):
                attack.append(newpos)
                if newpos in woccupied:
                    break
            else: break
    #move up
    for i in range(1, 7):
        if 9-y > i:
            newpos = (x, y+i)
            if not (newpos in boccupied):
                attack.append(newpos)
                if newpos in woccupied:
                    break
            else:
                break
    return attack


#attack of black Pawn
def attack_bPawn1(n):
    attack = []
    position = bPawn1(n)
    woccupied = white_occupied(n)
    boccupied = black_occupied(n)
    x = position[0]
    y = position[1]
    state = game_state_black[n][0][0]
    if state == "Pawn":
        if y > 1:
            newpos = (x, y - 1)
            if not (newpos in woccupied) and not (newpos in boccupied):
                attack.append(newpos)
        if y > 1:
            if 9 - x > 1:
                newpos = (x + 1, y - 1)
                if newpos in woccupied and not (newpos in boccupied):
                    attack.append(newpos)
        if y > 1:
            if x > 1:
                newpos = (x - 1, y - 1)
                if newpos in woccupied and not (newpos in boccupied):
                    attack.append(newpos)
        if y == 7:
            newpos = (x, y - 2)
            new2pos = (x, y - 1)
            if not (newpos in woccupied or newpos in boccupied or new2pos in woccupied or new2pos in boccupied):
                attack.append(newpos)
    if state == "Queen":
        # move left down
        for i in range(1, 7):
            if x > i:
                if y > i:
                    newpos = (x - i, y - i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
                    # move right up
        for i in range(1, 7):
            if 9 - x > i:
                if 9 - y > i:
                    newpos = (x + i, y + i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
                    # move right down
        for i in range(1, 7):
            if y > i:
                if 9 - x > i:
                    newpos = (x + i, y - i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
        # move left up
        for i in range(1, 7):
            if 9 - y > i:
                if x > i:
                    newpos = (x - i, y + i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
        # move left
        for i in range(1, 7):
            if x > i:
                newpos = (x - i, y)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
                # move right
        for i in range(1, 7):
            if 9 - x > i:
                newpos = (x + i, y)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
                # move down
        for i in range(1, 7):
            if y > i:
                newpos = (x, y - i)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
        # move up
        for i in range(1, 7):
            if 9 - y > i:
                newpos = (x, y + i)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
    if state == "Knight":
        if x - 2 > 0:
            if y - 1 > 0:
                newpos = (x - 2, y - 1)
                if not (newpos in boccupied):
                    attack.append(newpos)
            if y + 1 < 9:
                newpos = (x - 2, y + 1)
                if not (newpos in boccupied):
                    attack.append(newpos)
        if x + 2 < 9:
            if y - 1 > 0:
                newpos = (x + 2, y - 1)
                if not (newpos in boccupied):
                    attack.append(newpos)
            if y + 1 < 9:
                newpos = (x + 2, y + 1)
                if not (newpos in boccupied):
                    attack.append(newpos)
        if x - 1 > 0:
            if y - 2 > 0:
                newpos = (x - 1, y - 2)
                if not (newpos in boccupied):
                    attack.append(newpos)
            if y + 2 < 9:
                newpos = (x - 1, y + 2)
                if not (newpos in boccupied):
                    attack.append(newpos)
        if x + 1 < 9:
            if y - 2 > 0:
                newpos = (x + 1, y - 2)
                if not (newpos in boccupied):
                    attack.append(newpos)
            if y + 2 < 9:
                newpos = (x + 1, y + 2)
                if not (newpos in boccupied):
                    attack.append(newpos)
    if state == "Rook":
        # move left
        for i in range(1, 7):
            if x > i:
                newpos = (x - i, y)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move right
        for i in range(1, 7):
            if 9 - x > i:
                newpos = (x + i, y)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
                # move down
        for i in range(1, 7):
            if y > i:
                newpos = (x, y - i)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
        # move up
        for i in range(1, 7):
            if 9 - y > i:
                newpos = (x, y + i)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
    if state == "Bishop":
        # move left down
        for i in range(1, 7):
            if x > i:
                if y > i:
                    newpos = (x - i, y - i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
                    # move right up
        for i in range(1, 7):
            if 9 - x > i:
                if 9 - y > i:
                    newpos = (x + i, y + i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
                    # move right down
        for i in range(1, 7):
            if y > i:
                if 9 - x > i:
                    newpos = (x + i, y - i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
        # move left up
        for i in range(1, 7):
            if 9 - y > i:
                if x > i:
                    newpos = (x - i, y + i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
    return attack


#attack of black Pawn
def attack_bPawn2(n):
    attack = []
    position = bPawn2(n)
    woccupied = white_occupied(n)
    boccupied = black_occupied(n)
    x = position[0]
    y = position[1]
    state = game_state_black[n][1][0]
    if state == "Pawn":
        if y > 1:
            newpos = (x, y - 1)
            if not (newpos in woccupied) and not (newpos in boccupied):
                attack.append(newpos)
        if y > 1:
            if 9 - x > 1:
                newpos = (x + 1, y - 1)
                if newpos in woccupied and not (newpos in boccupied):
                    attack.append(newpos)
        if y > 1:
            if x > 1:
                newpos = (x - 1, y - 1)
                if newpos in woccupied and not (newpos in boccupied):
                    attack.append(newpos)
        if y == 7:
            newpos = (x, y - 2)
            new2pos = (x, y - 1)
            if not (newpos in woccupied or newpos in boccupied or new2pos in woccupied or new2pos in boccupied):
                attack.append(newpos)
    if state == "Queen":
        # move left down
        for i in range(1, 7):
            if x > i:
                if y > i:
                    newpos = (x - i, y - i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
                    # move right up
        for i in range(1, 7):
            if 9 - x > i:
                if 9 - y > i:
                    newpos = (x + i, y + i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
                    # move right down
        for i in range(1, 7):
            if y > i:
                if 9 - x > i:
                    newpos = (x + i, y - i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
        # move left up
        for i in range(1, 7):
            if 9 - y > i:
                if x > i:
                    newpos = (x - i, y + i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
        # move left
        for i in range(1, 7):
            if x > i:
                newpos = (x - i, y)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
                # move right
        for i in range(1, 7):
            if 9 - x > i:
                newpos = (x + i, y)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
                # move down
        for i in range(1, 7):
            if y > i:
                newpos = (x, y - i)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
        # move up
        for i in range(1, 7):
            if 9 - y > i:
                newpos = (x, y + i)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
    if state == "Knight":
        if x - 2 > 0:
            if y - 1 > 0:
                newpos = (x - 2, y - 1)
                if not (newpos in boccupied):
                    attack.append(newpos)
            if y + 1 < 9:
                newpos = (x - 2, y + 1)
                if not (newpos in boccupied):
                    attack.append(newpos)
        if x + 2 < 9:
            if y - 1 > 0:
                newpos = (x + 2, y - 1)
                if not (newpos in boccupied):
                    attack.append(newpos)
            if y + 1 < 9:
                newpos = (x + 2, y + 1)
                if not (newpos in boccupied):
                    attack.append(newpos)
        if x - 1 > 0:
            if y - 2 > 0:
                newpos = (x - 1, y - 2)
                if not (newpos in boccupied):
                    attack.append(newpos)
            if y + 2 < 9:
                newpos = (x - 1, y + 2)
                if not (newpos in boccupied):
                    attack.append(newpos)
        if x + 1 < 9:
            if y - 2 > 0:
                newpos = (x + 1, y - 2)
                if not (newpos in boccupied):
                    attack.append(newpos)
            if y + 2 < 9:
                newpos = (x + 1, y + 2)
                if not (newpos in boccupied):
                    attack.append(newpos)
    if state == "Rook":
        # move left
        for i in range(1, 7):
            if x > i:
                newpos = (x - i, y)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move right
        for i in range(1, 7):
            if 9 - x > i:
                newpos = (x + i, y)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
                # move down
        for i in range(1, 7):
            if y > i:
                newpos = (x, y - i)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
        # move up
        for i in range(1, 7):
            if 9 - y > i:
                newpos = (x, y + i)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
    if state == "Bishop":
        # move left down
        for i in range(1, 7):
            if x > i:
                if y > i:
                    newpos = (x - i, y - i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
                    # move right up
        for i in range(1, 7):
            if 9 - x > i:
                if 9 - y > i:
                    newpos = (x + i, y + i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
                    # move right down
        for i in range(1, 7):
            if y > i:
                if 9 - x > i:
                    newpos = (x + i, y - i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
        # move left up
        for i in range(1, 7):
            if 9 - y > i:
                if x > i:
                    newpos = (x - i, y + i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
    return attack

#attack of black Pawn
def attack_bPawn3(n):
    attack = []
    position = bPawn3(n)
    woccupied = white_occupied(n)
    boccupied = black_occupied(n)
    x = position[0]
    y = position[1]
    state = game_state_black[n][2][0]
    if state == "Pawn":
        if y > 1:
            newpos = (x, y - 1)
            if not (newpos in woccupied) and not (newpos in boccupied):
                attack.append(newpos)
        if y > 1:
            if 9 - x > 1:
                newpos = (x + 1, y - 1)
                if newpos in woccupied and not (newpos in boccupied):
                    attack.append(newpos)
        if y > 1:
            if x > 1:
                newpos = (x - 1, y - 1)
                if newpos in woccupied and not (newpos in boccupied):
                    attack.append(newpos)
        if y == 7:
            newpos = (x, y - 2)
            new2pos = (x, y - 1)
            if not (newpos in woccupied or newpos in boccupied or new2pos in woccupied or new2pos in boccupied):
                attack.append(newpos)
    if state == "Queen":
        # move left down
        for i in range(1, 7):
            if x > i:
                if y > i:
                    newpos = (x - i, y - i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
                    # move right up
        for i in range(1, 7):
            if 9 - x > i:
                if 9 - y > i:
                    newpos = (x + i, y + i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
                    # move right down
        for i in range(1, 7):
            if y > i:
                if 9 - x > i:
                    newpos = (x + i, y - i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
        # move left up
        for i in range(1, 7):
            if 9 - y > i:
                if x > i:
                    newpos = (x - i, y + i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
        # move left
        for i in range(1, 7):
            if x > i:
                newpos = (x - i, y)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
                # move right
        for i in range(1, 7):
            if 9 - x > i:
                newpos = (x + i, y)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
                # move down
        for i in range(1, 7):
            if y > i:
                newpos = (x, y - i)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
        # move up
        for i in range(1, 7):
            if 9 - y > i:
                newpos = (x, y + i)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
    if state == "Knight":
        if x - 2 > 0:
            if y - 1 > 0:
                newpos = (x - 2, y - 1)
                if not (newpos in boccupied):
                    attack.append(newpos)
            if y + 1 < 9:
                newpos = (x - 2, y + 1)
                if not (newpos in boccupied):
                    attack.append(newpos)
        if x + 2 < 9:
            if y - 1 > 0:
                newpos = (x + 2, y - 1)
                if not (newpos in boccupied):
                    attack.append(newpos)
            if y + 1 < 9:
                newpos = (x + 2, y + 1)
                if not (newpos in boccupied):
                    attack.append(newpos)
        if x - 1 > 0:
            if y - 2 > 0:
                newpos = (x - 1, y - 2)
                if not (newpos in boccupied):
                    attack.append(newpos)
            if y + 2 < 9:
                newpos = (x - 1, y + 2)
                if not (newpos in boccupied):
                    attack.append(newpos)
        if x + 1 < 9:
            if y - 2 > 0:
                newpos = (x + 1, y - 2)
                if not (newpos in boccupied):
                    attack.append(newpos)
            if y + 2 < 9:
                newpos = (x + 1, y + 2)
                if not (newpos in boccupied):
                    attack.append(newpos)
    if state == "Rook":
        # move left
        for i in range(1, 7):
            if x > i:
                newpos = (x - i, y)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move right
        for i in range(1, 7):
            if 9 - x > i:
                newpos = (x + i, y)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
                # move down
        for i in range(1, 7):
            if y > i:
                newpos = (x, y - i)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
        # move up
        for i in range(1, 7):
            if 9 - y > i:
                newpos = (x, y + i)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
    if state == "Bishop":
        # move left down
        for i in range(1, 7):
            if x > i:
                if y > i:
                    newpos = (x - i, y - i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
                    # move right up
        for i in range(1, 7):
            if 9 - x > i:
                if 9 - y > i:
                    newpos = (x + i, y + i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
                    # move right down
        for i in range(1, 7):
            if y > i:
                if 9 - x > i:
                    newpos = (x + i, y - i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
        # move left up
        for i in range(1, 7):
            if 9 - y > i:
                if x > i:
                    newpos = (x - i, y + i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
    return attack

#attack of black Pawn
def attack_bPawn4(n):
    attack = []
    position = bPawn4(n)
    woccupied = white_occupied(n)
    boccupied = black_occupied(n)
    x = position[0]
    y = position[1]
    state = game_state_black[n][3][0]
    if state == "Pawn":
        if y > 1:
            newpos = (x, y - 1)
            if not (newpos in woccupied) and not (newpos in boccupied):
                attack.append(newpos)
        if y > 1:
            if 9 - x > 1:
                newpos = (x + 1, y - 1)
                if newpos in woccupied and not (newpos in boccupied):
                    attack.append(newpos)
        if y > 1:
            if x > 1:
                newpos = (x - 1, y - 1)
                if newpos in woccupied and not (newpos in boccupied):
                    attack.append(newpos)
        if y == 7:
            newpos = (x, y - 2)
            new2pos = (x, y - 1)
            if not (newpos in woccupied or newpos in boccupied or new2pos in woccupied or new2pos in boccupied):
                attack.append(newpos)
    if state == "Queen":
        # move left down
        for i in range(1, 7):
            if x > i:
                if y > i:
                    newpos = (x - i, y - i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
                    # move right up
        for i in range(1, 7):
            if 9 - x > i:
                if 9 - y > i:
                    newpos = (x + i, y + i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
                    # move right down
        for i in range(1, 7):
            if y > i:
                if 9 - x > i:
                    newpos = (x + i, y - i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
        # move left up
        for i in range(1, 7):
            if 9 - y > i:
                if x > i:
                    newpos = (x - i, y + i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
        # move left
        for i in range(1, 7):
            if x > i:
                newpos = (x - i, y)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
                # move right
        for i in range(1, 7):
            if 9 - x > i:
                newpos = (x + i, y)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
                # move down
        for i in range(1, 7):
            if y > i:
                newpos = (x, y - i)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
        # move up
        for i in range(1, 7):
            if 9 - y > i:
                newpos = (x, y + i)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
    if state == "Knight":
        if x - 2 > 0:
            if y - 1 > 0:
                newpos = (x - 2, y - 1)
                if not (newpos in boccupied):
                    attack.append(newpos)
            if y + 1 < 9:
                newpos = (x - 2, y + 1)
                if not (newpos in boccupied):
                    attack.append(newpos)
        if x + 2 < 9:
            if y - 1 > 0:
                newpos = (x + 2, y - 1)
                if not (newpos in boccupied):
                    attack.append(newpos)
            if y + 1 < 9:
                newpos = (x + 2, y + 1)
                if not (newpos in boccupied):
                    attack.append(newpos)
        if x - 1 > 0:
            if y - 2 > 0:
                newpos = (x - 1, y - 2)
                if not (newpos in boccupied):
                    attack.append(newpos)
            if y + 2 < 9:
                newpos = (x - 1, y + 2)
                if not (newpos in boccupied):
                    attack.append(newpos)
        if x + 1 < 9:
            if y - 2 > 0:
                newpos = (x + 1, y - 2)
                if not (newpos in boccupied):
                    attack.append(newpos)
            if y + 2 < 9:
                newpos = (x + 1, y + 2)
                if not (newpos in boccupied):
                    attack.append(newpos)
    if state == "Rook":
        # move left
        for i in range(1, 7):
            if x > i:
                newpos = (x - i, y)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move right
        for i in range(1, 7):
            if 9 - x > i:
                newpos = (x + i, y)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
                # move down
        for i in range(1, 7):
            if y > i:
                newpos = (x, y - i)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
        # move up
        for i in range(1, 7):
            if 9 - y > i:
                newpos = (x, y + i)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
    if state == "Bishop":
        # move left down
        for i in range(1, 7):
            if x > i:
                if y > i:
                    newpos = (x - i, y - i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
                    # move right up
        for i in range(1, 7):
            if 9 - x > i:
                if 9 - y > i:
                    newpos = (x + i, y + i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
                    # move right down
        for i in range(1, 7):
            if y > i:
                if 9 - x > i:
                    newpos = (x + i, y - i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
        # move left up
        for i in range(1, 7):
            if 9 - y > i:
                if x > i:
                    newpos = (x - i, y + i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
    return attack

#attack of black Pawn
def attack_bPawn5(n):
    attack = []
    position = bPawn5(n)
    woccupied = white_occupied(n)
    boccupied = black_occupied(n)
    x = position[0]
    y = position[1]
    state = game_state_black[n][4][0]
    if state == "Pawn":
        if y > 1:
            newpos = (x, y - 1)
            if not (newpos in woccupied) and not (newpos in boccupied):
                attack.append(newpos)
        if y > 1:
            if 9 - x > 1:
                newpos = (x + 1, y - 1)
                if newpos in woccupied and not (newpos in boccupied):
                    attack.append(newpos)
        if y > 1:
            if x > 1:
                newpos = (x - 1, y - 1)
                if newpos in woccupied and not (newpos in boccupied):
                    attack.append(newpos)
        if y == 7:
            newpos = (x, y - 2)
            new2pos = (x, y - 1)
            if not (newpos in woccupied or newpos in boccupied or new2pos in woccupied or new2pos in boccupied):
                attack.append(newpos)
    if state == "Queen":
        # move left down
        for i in range(1, 7):
            if x > i:
                if y > i:
                    newpos = (x - i, y - i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
                    # move right up
        for i in range(1, 7):
            if 9 - x > i:
                if 9 - y > i:
                    newpos = (x + i, y + i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
                    # move right down
        for i in range(1, 7):
            if y > i:
                if 9 - x > i:
                    newpos = (x + i, y - i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
        # move left up
        for i in range(1, 7):
            if 9 - y > i:
                if x > i:
                    newpos = (x - i, y + i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
        # move left
        for i in range(1, 7):
            if x > i:
                newpos = (x - i, y)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
                # move right
        for i in range(1, 7):
            if 9 - x > i:
                newpos = (x + i, y)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
                # move down
        for i in range(1, 7):
            if y > i:
                newpos = (x, y - i)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
        # move up
        for i in range(1, 7):
            if 9 - y > i:
                newpos = (x, y + i)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
    if state == "Knight":
        if x - 2 > 0:
            if y - 1 > 0:
                newpos = (x - 2, y - 1)
                if not (newpos in boccupied):
                    attack.append(newpos)
            if y + 1 < 9:
                newpos = (x - 2, y + 1)
                if not (newpos in boccupied):
                    attack.append(newpos)
        if x + 2 < 9:
            if y - 1 > 0:
                newpos = (x + 2, y - 1)
                if not (newpos in boccupied):
                    attack.append(newpos)
            if y + 1 < 9:
                newpos = (x + 2, y + 1)
                if not (newpos in boccupied):
                    attack.append(newpos)
        if x - 1 > 0:
            if y - 2 > 0:
                newpos = (x - 1, y - 2)
                if not (newpos in boccupied):
                    attack.append(newpos)
            if y + 2 < 9:
                newpos = (x - 1, y + 2)
                if not (newpos in boccupied):
                    attack.append(newpos)
        if x + 1 < 9:
            if y - 2 > 0:
                newpos = (x + 1, y - 2)
                if not (newpos in boccupied):
                    attack.append(newpos)
            if y + 2 < 9:
                newpos = (x + 1, y + 2)
                if not (newpos in boccupied):
                    attack.append(newpos)
    if state == "Rook":
        # move left
        for i in range(1, 7):
            if x > i:
                newpos = (x - i, y)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move right
        for i in range(1, 7):
            if 9 - x > i:
                newpos = (x + i, y)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
                # move down
        for i in range(1, 7):
            if y > i:
                newpos = (x, y - i)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
        # move up
        for i in range(1, 7):
            if 9 - y > i:
                newpos = (x, y + i)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
    if state == "Bishop":
        # move left down
        for i in range(1, 7):
            if x > i:
                if y > i:
                    newpos = (x - i, y - i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
                    # move right up
        for i in range(1, 7):
            if 9 - x > i:
                if 9 - y > i:
                    newpos = (x + i, y + i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
                    # move right down
        for i in range(1, 7):
            if y > i:
                if 9 - x > i:
                    newpos = (x + i, y - i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
        # move left up
        for i in range(1, 7):
            if 9 - y > i:
                if x > i:
                    newpos = (x - i, y + i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
    return attack

#attack of black Pawn
def attack_bPawn6(n):
    attack = []
    position = bPawn6(n)
    woccupied = white_occupied(n)
    boccupied = black_occupied(n)
    x = position[0]
    y = position[1]
    state = game_state_black[n][5][0]
    if state == "Pawn":
        if y > 1:
            newpos = (x, y - 1)
            if not (newpos in woccupied) and not (newpos in boccupied):
                attack.append(newpos)
        if y > 1:
            if 9 - x > 1:
                newpos = (x + 1, y - 1)
                if newpos in woccupied and not (newpos in boccupied):
                    attack.append(newpos)
        if y > 1:
            if x > 1:
                newpos = (x - 1, y - 1)
                if newpos in woccupied and not (newpos in boccupied):
                    attack.append(newpos)
        if y == 7:
            newpos = (x, y - 2)
            new2pos = (x, y - 1)
            if not (newpos in woccupied or newpos in boccupied or new2pos in woccupied or new2pos in boccupied):
                attack.append(newpos)
    if state == "Queen":
        # move left down
        for i in range(1, 7):
            if x > i:
                if y > i:
                    newpos = (x - i, y - i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
                    # move right up
        for i in range(1, 7):
            if 9 - x > i:
                if 9 - y > i:
                    newpos = (x + i, y + i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
                    # move right down
        for i in range(1, 7):
            if y > i:
                if 9 - x > i:
                    newpos = (x + i, y - i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
        # move left up
        for i in range(1, 7):
            if 9 - y > i:
                if x > i:
                    newpos = (x - i, y + i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
        # move left
        for i in range(1, 7):
            if x > i:
                newpos = (x - i, y)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
                # move right
        for i in range(1, 7):
            if 9 - x > i:
                newpos = (x + i, y)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
                # move down
        for i in range(1, 7):
            if y > i:
                newpos = (x, y - i)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
        # move up
        for i in range(1, 7):
            if 9 - y > i:
                newpos = (x, y + i)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
    if state == "Knight":
        if x - 2 > 0:
            if y - 1 > 0:
                newpos = (x - 2, y - 1)
                if not (newpos in boccupied):
                    attack.append(newpos)
            if y + 1 < 9:
                newpos = (x - 2, y + 1)
                if not (newpos in boccupied):
                    attack.append(newpos)
        if x + 2 < 9:
            if y - 1 > 0:
                newpos = (x + 2, y - 1)
                if not (newpos in boccupied):
                    attack.append(newpos)
            if y + 1 < 9:
                newpos = (x + 2, y + 1)
                if not (newpos in boccupied):
                    attack.append(newpos)
        if x - 1 > 0:
            if y - 2 > 0:
                newpos = (x - 1, y - 2)
                if not (newpos in boccupied):
                    attack.append(newpos)
            if y + 2 < 9:
                newpos = (x - 1, y + 2)
                if not (newpos in boccupied):
                    attack.append(newpos)
        if x + 1 < 9:
            if y - 2 > 0:
                newpos = (x + 1, y - 2)
                if not (newpos in boccupied):
                    attack.append(newpos)
            if y + 2 < 9:
                newpos = (x + 1, y + 2)
                if not (newpos in boccupied):
                    attack.append(newpos)
    if state == "Rook":
        # move left
        for i in range(1, 7):
            if x > i:
                newpos = (x - i, y)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move right
        for i in range(1, 7):
            if 9 - x > i:
                newpos = (x + i, y)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
                # move down
        for i in range(1, 7):
            if y > i:
                newpos = (x, y - i)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
        # move up
        for i in range(1, 7):
            if 9 - y > i:
                newpos = (x, y + i)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
    if state == "Bishop":
        # move left down
        for i in range(1, 7):
            if x > i:
                if y > i:
                    newpos = (x - i, y - i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
                    # move right up
        for i in range(1, 7):
            if 9 - x > i:
                if 9 - y > i:
                    newpos = (x + i, y + i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
                    # move right down
        for i in range(1, 7):
            if y > i:
                if 9 - x > i:
                    newpos = (x + i, y - i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
        # move left up
        for i in range(1, 7):
            if 9 - y > i:
                if x > i:
                    newpos = (x - i, y + i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
    return attack


#attack of black Pawn
def attack_bPawn7(n):
    attack = []
    position = bPawn7(n)
    woccupied = white_occupied(n)
    boccupied = black_occupied(n)
    x = position[0]
    y = position[1]
    state = game_state_black[n][6][0]
    if state == "Pawn":
        if y > 1:
            newpos = (x, y - 1)
            if not (newpos in woccupied) and not (newpos in boccupied):
                attack.append(newpos)
        if y > 1:
            if 9 - x > 1:
                newpos = (x + 1, y - 1)
                if newpos in woccupied and not (newpos in boccupied):
                    attack.append(newpos)
        if y > 1:
            if x > 1:
                newpos = (x - 1, y - 1)
                if newpos in woccupied and not (newpos in boccupied):
                    attack.append(newpos)
        if y == 7:
            newpos = (x, y - 2)
            new2pos = (x, y - 1)
            if not (newpos in woccupied or newpos in boccupied or new2pos in woccupied or new2pos in boccupied):
                attack.append(newpos)
    if state == "Queen":
        # move left down
        for i in range(1, 7):
            if x > i:
                if y > i:
                    newpos = (x - i, y - i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
                    # move right up
        for i in range(1, 7):
            if 9 - x > i:
                if 9 - y > i:
                    newpos = (x + i, y + i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
                    # move right down
        for i in range(1, 7):
            if y > i:
                if 9 - x > i:
                    newpos = (x + i, y - i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
        # move left up
        for i in range(1, 7):
            if 9 - y > i:
                if x > i:
                    newpos = (x - i, y + i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
        # move left
        for i in range(1, 7):
            if x > i:
                newpos = (x - i, y)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
                # move right
        for i in range(1, 7):
            if 9 - x > i:
                newpos = (x + i, y)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
                # move down
        for i in range(1, 7):
            if y > i:
                newpos = (x, y - i)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
        # move up
        for i in range(1, 7):
            if 9 - y > i:
                newpos = (x, y + i)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
    if state == "Knight":
        if x - 2 > 0:
            if y - 1 > 0:
                newpos = (x - 2, y - 1)
                if not (newpos in boccupied):
                    attack.append(newpos)
            if y + 1 < 9:
                newpos = (x - 2, y + 1)
                if not (newpos in boccupied):
                    attack.append(newpos)
        if x + 2 < 9:
            if y - 1 > 0:
                newpos = (x + 2, y - 1)
                if not (newpos in boccupied):
                    attack.append(newpos)
            if y + 1 < 9:
                newpos = (x + 2, y + 1)
                if not (newpos in boccupied):
                    attack.append(newpos)
        if x - 1 > 0:
            if y - 2 > 0:
                newpos = (x - 1, y - 2)
                if not (newpos in boccupied):
                    attack.append(newpos)
            if y + 2 < 9:
                newpos = (x - 1, y + 2)
                if not (newpos in boccupied):
                    attack.append(newpos)
        if x + 1 < 9:
            if y - 2 > 0:
                newpos = (x + 1, y - 2)
                if not (newpos in boccupied):
                    attack.append(newpos)
            if y + 2 < 9:
                newpos = (x + 1, y + 2)
                if not (newpos in boccupied):
                    attack.append(newpos)
    if state == "Rook":
        # move left
        for i in range(1, 7):
            if x > i:
                newpos = (x - i, y)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move right
        for i in range(1, 7):
            if 9 - x > i:
                newpos = (x + i, y)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
                # move down
        for i in range(1, 7):
            if y > i:
                newpos = (x, y - i)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
        # move up
        for i in range(1, 7):
            if 9 - y > i:
                newpos = (x, y + i)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
    if state == "Bishop":
        # move left down
        for i in range(1, 7):
            if x > i:
                if y > i:
                    newpos = (x - i, y - i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
                    # move right up
        for i in range(1, 7):
            if 9 - x > i:
                if 9 - y > i:
                    newpos = (x + i, y + i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
                    # move right down
        for i in range(1, 7):
            if y > i:
                if 9 - x > i:
                    newpos = (x + i, y - i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
        # move left up
        for i in range(1, 7):
            if 9 - y > i:
                if x > i:
                    newpos = (x - i, y + i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
    return attack





#attack of black Pawn
def attack_bPawn8(n):
    attack = []
    position = bPawn8(n)
    woccupied = white_occupied(n)
    boccupied = black_occupied(n)
    x = position[0]
    y = position[1]
    state = game_state_black[n][7][0]
    if state == "Pawn":
        if y > 1:
            newpos = (x, y - 1)
            if not (newpos in woccupied) and not(newpos in boccupied):
                attack.append(newpos)
        if y > 1:
            if 9 - x > 1:
                newpos = (x + 1, y - 1)
                if newpos in woccupied and not(newpos in boccupied):
                    attack.append(newpos)
        if y > 1:
            if x > 1:
                newpos = (x - 1, y - 1)
                if newpos in woccupied and not(newpos in boccupied):
                    attack.append(newpos)
        if y == 7:
            newpos = (x, y - 2)
            new2pos = (x, y - 1)
            if not (newpos in woccupied or newpos in boccupied or new2pos in woccupied or new2pos in boccupied):
                attack.append(newpos)
    if state == "Queen":
        # move left down
        for i in range(1, 7):
            if x > i:
                if y > i:
                    newpos = (x - i, y - i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
                    # move right up
        for i in range(1, 7):
            if 9 - x > i:
                if 9 - y > i:
                    newpos = (x + i, y + i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
                    # move right down
        for i in range(1, 7):
            if y > i:
                if 9 - x > i:
                    newpos = (x + i, y - i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
        # move left up
        for i in range(1, 7):
            if 9 - y > i:
                if x > i:
                    newpos = (x - i, y + i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
        # move left
        for i in range(1, 7):
            if x > i:
                newpos = (x - i, y)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
                # move right
        for i in range(1, 7):
            if 9 - x > i:
                newpos = (x + i, y)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
                # move down
        for i in range(1, 7):
            if y > i:
                newpos = (x, y - i)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
        # move up
        for i in range(1, 7):
            if 9 - y > i:
                newpos = (x, y + i)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
    if state == "Knight":
        if x - 2 > 0:
            if y - 1 > 0:
                newpos = (x - 2, y - 1)
                if not (newpos in boccupied):
                    attack.append(newpos)
            if y + 1 < 9:
                newpos = (x - 2, y + 1)
                if not (newpos in boccupied):
                    attack.append(newpos)
        if x + 2 < 9:
            if y - 1 > 0:
                newpos = (x + 2, y - 1)
                if not (newpos in boccupied):
                    attack.append(newpos)
            if y + 1 < 9:
                newpos = (x + 2, y + 1)
                if not (newpos in boccupied):
                    attack.append(newpos)
        if x - 1 > 0:
            if y - 2 > 0:
                newpos = (x - 1, y - 2)
                if not (newpos in boccupied):
                    attack.append(newpos)
            if y + 2 < 9:
                newpos = (x - 1, y + 2)
                if not (newpos in boccupied):
                    attack.append(newpos)
        if x + 1 < 9:
            if y - 2 > 0:
                newpos = (x + 1, y - 2)
                if not (newpos in boccupied):
                    attack.append(newpos)
            if y + 2 < 9:
                newpos = (x + 1, y + 2)
                if not (newpos in boccupied):
                    attack.append(newpos)
    if state == "Rook":
        # move left
        for i in range(1, 7):
            if x > i:
                newpos = (x - i, y)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in boccupied:
                        break
                else:
                    break
                # move right
        for i in range(1, 7):
            if 9 - x > i:
                newpos = (x + i, y)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
                # move down
        for i in range(1, 7):
            if y > i:
                newpos = (x, y - i)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
        # move up
        for i in range(1, 7):
            if 9 - y > i:
                newpos = (x, y + i)
                if not (newpos in boccupied):
                    attack.append(newpos)
                    if newpos in woccupied:
                        break
                else:
                    break
    if state == "Bishop":
        #move left down
        for i in range(1, 7):
            if x > i:
                if y > i:
                    newpos = (x - i, y - i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
                    # move right up
        for i in range(1, 7):
            if 9 - x > i:
                if 9 - y > i:
                    newpos = (x + i, y + i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
                    # move right down
        for i in range(1, 7):
            if y > i:
                if 9 - x > i:
                    newpos = (x + i, y - i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
        # move left up
        for i in range(1, 7):
            if 9 - y > i:
                if x > i:
                    newpos = (x - i, y + i)
                    if not (newpos in boccupied):
                        attack.append(newpos)
                        if newpos in woccupied:
                            break
                    else:
                        break
    return attack







def game_start_white():
    return [[("Pawn", (1,2)),
             ("Pawn", (2,2)),
             ("Pawn", (3,2)),
             ("Pawn", (4,2)),
             ("Pawn", (5,2)),
             ("Pawn", (6,2)),
             ("Pawn", (7,2)),
             ("Pawn", (8,2)),
             ("Rook", (1,1)),
             ("Knight", (2,1)),
             ("Bishop", (3,1)),
             ("Queen", (4,1)),
             ("King", (5,1)),
             ("Bishop", (6,1)),
             ("Knight", (7,1)),
             ("Rook", (8,1))]]
def game_start_black():
    return [[("Pawn", (1,7)),
             ("Pawn", (2,7)),
             ("Pawn", (3,7)),
             ("Pawn", (4,7)),
             ("Pawn", (5,7)),
             ("Pawn", (6,7)),
             ("Pawn", (7,7)),
             ("Pawn", (8,7)),
             ("Rook", (1,8)),
             ("Knight", (2,8)),
             ("Bishop", (3,8)),
             ("Queen", (4,8)),
             ("King", (5,8)),
             ("Bishop", (6,8)),
             ("Knight", (7,8)),
             ("Rook", (8,8))]]

nextturncheck_white = "false"
nextturncheck_black = "false"





#allocate names to positions of white figures
def wPawn1(n):
    return game_state_white[n][0][1]
def wPawn2(n):
    return game_state_white[n][1][1]
def wPawn3(n):
    return game_state_white[n][2][1]
def wPawn4(n):
    return game_state_white[n][3][1]
def wPawn5(n):
    return game_state_white[n][4][1]
def wPawn6(n):
    return game_state_white[n][5][1]
def wPawn7(n):
    return game_state_white[n][6][1]
def wPawn8(n):
    return game_state_white[n][7][1]
def wRook1(n):
    return game_state_white[n][8][1]
def wKnight1(n):
    return game_state_white[n][9][1]
def wBishop1(n):
    return game_state_white[n][10][1]
def wQueen(n):
    return game_state_white[n][11][1]
def wKing(n):
    return game_state_white[n][12][1]
def wBishop2(n):
    return game_state_white[n][13][1]
def wKnight2(n):
    return game_state_white[n][14][1]
def wRook2(n):
    return game_state_white[n][15][1]

#allocate names to positions of black figures
def bPawn1(n):
    return game_state_black[n][0][1]
def bPawn2(n):
    return game_state_black[n][1][1]
def bPawn3(n):
    return game_state_black[n][2][1]
def bPawn4(n):
    return game_state_black[n][3][1]
def bPawn5(n):
    return game_state_black[n][4][1]
def bPawn6(n):
    return game_state_black[n][5][1]
def bPawn7(n):
    return game_state_black[n][6][1]
def bPawn8(n):
    return game_state_black[n][7][1]
def bRook1(n):
    return game_state_black[n][8][1]
def bKnight1(n):
    return game_state_black[n][9][1]
def bBishop1(n):
    return game_state_black[n][10][1]
def bQueen(n):
    return game_state_black[n][11][1]
def bKing(n):
    return game_state_black[n][12][1]
def bBishop2(n):
    return game_state_black[n][13][1]
def bKnight2(n):
    return game_state_black[n][14][1]
def bRook2(n):
    return game_state_black[n][15][1]

#define list of occupied places
def white_occupied(n):
    return [wPawn1(n),
     wPawn2(n),
     wPawn3(n),
     wPawn4(n),
     wPawn5(n),
     wPawn6(n),
     wPawn7(n),
     wPawn8(n),
     wRook1(n),
     wKnight1(n),
     wBishop1(n),
     wQueen(n),
     wKing(n),
     wBishop2(n),
     wKnight2(n),
     wRook2(n)]

def black_occupied(n):
    return [bPawn1(n),
            bPawn2(n),
            bPawn3(n),
            bPawn4(n),
            bPawn5(n),
            bPawn6(n),
            bPawn7(n),
            bPawn8(n),
            bRook1(n),
            bKnight1(n),
            bBishop1(n),
            bQueen(n),
            bKing(n),
            bBishop2(n),
            bKnight2(n),
            bRook2(n)]
k = 0






def total_attacks_white(n):
    x = attack_wPawn1(n) + attack_wPawn2(n) + attack_wPawn3(n) +attack_wPawn4(n) +attack_wPawn5(n) + attack_wPawn6(n) + attack_wPawn7(n) +attack_wPawn8(n) +attack_wKing(n) +attack_wQueen(n) +attack_wKnight1(n) +attack_wKnight2(n) +attack_wRook1(n) +attack_wRook2(n) +attack_wBishop1(n) +attack_wBishop2(n)

    return x
def total_attacks_black(n):
    x = attack_bPawn1(n) + attack_bPawn2(n) + attack_bPawn3(n) +attack_bPawn4(n) +attack_bPawn5(n) + attack_bPawn6(n) + attack_bPawn7(n) +attack_bPawn8(n) +attack_bKing(n) +attack_bQueen(n) +attack_bKnight1(n) +attack_bKnight2(n) +attack_bRook1(n) +attack_bRook2(n) +attack_bBishop1(n) +attack_bBishop2(n)

    return x



def black_remove(square, n):
    x = square[0]
    y = square[1]
    if square in black_occupied(n):
        if square == bPawn1(n):
            bpawn_state_change(n, 0, "Pawn", (100, 100))
        if square == bPawn2(n):
            bpawn_state_change(n, 1, "Pawn", (100, 100))
        if square == bPawn3(n):
            bpawn_state_change(n, 2, "Pawn", (100, 100))
        if square == bPawn4(n):
            bpawn_state_change(n, 3, "Pawn", (100, 100))
        if square == bPawn5(n):
            bpawn_state_change(n, 4, "Pawn", (100, 100))
        if square == bPawn6(n):
            bpawn_state_change(n, 5, "Pawn", (100, 100))
        if square == bPawn7(n):
            bpawn_state_change(n, 6, "Pawn", (100, 100))
        if square == bPawn8(n):
            bpawn_state_change(n, 7, "Pawn", (100, 100))
        if square == bRook1(n):
            bpawn_state_change(n, 8, "Pawn", (100, 100))
        if square == bKnight1(n):
            bpawn_state_change(n, 9, "Pawn", (100, 100))
        if square == bBishop1(n):
            bpawn_state_change(n, 10, "Pawn", (100, 100))
        if square == bQueen(n):
            bpawn_state_change(n, 11, "Pawn", (100, 100))
        if square == bKing(n):
            bpawn_state_change(n, 12, "Pawn", (100, 100))
        if square == bBishop2(n):
            bpawn_state_change(n, 13, "Pawn", (100, 100))
        if square == bKnight2(n):
            bpawn_state_change(n, 14, "Pawn", (100, 100))
        if square == bRook2(n):
            bpawn_state_change(n, 15, "Pawn", (100, 100))



def white_remove(square, n):
    x = square[0]
    y = square[1]
    if square in white_occupied(n):
        if square == wPawn1(n):
            wpawn_state_change(n, 0, "Pawn", (100, 100))
        if square == wPawn2(n):
            wpawn_state_change(n, 1, "Pawn", (100, 100))
        if square == wPawn3(n):
            wpawn_state_change(n, 2, "Pawn", (100, 100))
        if square == wPawn4(n):
            wpawn_state_change(n, 3, "Pawn", (100, 100))
        if square == wPawn5(n):
            wpawn_state_change(n, 4, "Pawn", (100, 100))
        if square == wPawn6(n):
            wpawn_state_change(n, 5, "Pawn", (100, 100))
        if square == wPawn7(n):
            wpawn_state_change(n, 6, "Pawn", (100, 100))
        if square == wPawn8(n):
            wpawn_state_change(n, 7, "Pawn", (100, 100))
        if square == wRook1(n):
            wpawn_state_change(n, 8, "Pawn", (100, 100))
        if square == wKnight1(n):
            wpawn_state_change(n, 9, "Pawn", (100, 100))
        if square == wBishop1(n):
            wpawn_state_change(n, 10, "Pawn", (100, 100))
        if square == wQueen(n):
            wpawn_state_change(n, 11, "Pawn", (100, 100))
        if square == wKing(n):
            wpawn_state_change(n, 12, "Pawn", (100, 100))
        if square == wBishop2(n):
            wpawn_state_change(n, 13, "Pawn", (100, 100))
        if square == wKnight2(n):
            wpawn_state_change(n, 14, "Pawn", (100, 100))
        if square == wRook2(n):
            wpawn_state_change(n, 15, "Pawn", (100, 100))


def wpawn_state_change(n, number, newstate, square):
    game_state_white[n][number] = (newstate, square)

def bpawn_state_change(n, number, newstate, square):
    game_state_black[n][number] = (newstate, square)


def white_standard_move():
    global new_white_state, new_brook1move, new_brook2move, new_wrook1move, new_wrook2move, newbrook1move, newbrook2move
    if checkstate == "true":
        if position in black_occupied(n):
            black_remove(position, n)
        if bKing(n) in total_attacks_white(n):
            if not (wKing(n) in total_attacks_black(n)):

                new_white_state.append((game_state_white[n], game_state_black[n]))
                newbrook1move.append(brook1move[n])
                newbrook2move.append(brook2move[n])
                newwrook1move.append(wrook1move[n])
                newwrook2move.append(wrook2move[n])

    if checkstate == "false":
        if position in black_occupied(n):
            black_remove(position, n)
        if not (bKing(n) in total_attacks_white(n)):
            if not (wKing(n) in total_attacks_black(n)):

                new_white_state.append((game_state_white[n], game_state_black[n]))
                newbrook1move.append(brook1move[n])
                newbrook2move.append(brook2move[n])
                newwrook1move.append(wrook1move[n])
                newwrook2move.append(wrook2move[n])


def black_standard_move():
    global new_black_state, new_brook1move, new_brook2move, new_wrook1move, new_wrook2move, newbrook1move, newbrook2move
    if checkstate == "true":
        if position in white_occupied(n):
            white_remove(position, n)
        if wKing(n) in total_attacks_black(n):
            if not (bKing(n) in total_attacks_white(n)):

                new_black_state.append((game_state_black[n], game_state_white[n]))
                newbrook1move.append(brook1move[n])
                newbrook2move.append(brook2move[n])
                newwrook1move.append(wrook1move[n])
                newwrook2move.append(wrook2move[n])
    if checkstate == "false":
        if position in white_occupied(n):
            white_remove(position, n)
        if not (wKing(n) in total_attacks_black(n)):
            if not (bKing(n) in total_attacks_white(n)):

                new_black_state.append((game_state_black[n], game_state_white[n]))
                newbrook1move.append(brook1move[n])
                newbrook2move.append(brook2move[n])
                newwrook1move.append(wrook1move[n])
                newwrook2move.append(wrook2move[n])












#starting position in game - to place in initialise game
game_state_white = game_start_white()
game_state_black = game_start_black()
wskip = 0
bskip = 0
wrook1move = [0]
wrook2move = [0]
brook1move = [0]
brook2move = [0]
game = []
game_state = [game_state_white, game_state_black, wrook1move, wrook2move, brook1move, brook2move]

def make_move_white(white_move, game_state):

    global wskip, bskip, wrook1move, brook1move
    global wrook2move, brook2move
    global game_state_white, game_state_black
    global checkstate
    global position
    global new_white_state, newbrook1move, newbrook2move
    global newwrook1move, newwrook2move, newblack_state
    global n

    new_white_state = []  # pair of (whitestate, blackstate)
    newbrook1move = []
    newbrook2move = []
    newwrook1move = []
    newwrook2move = []
    new_white_state = []  # pair of (whitestate, blackstate)
    new_black_state = []
    statenumber = len(game_state_white)
    game_state_white = game_state[0]
    game_state_black = game_state[1]
    wrook1move = game_state[2]
    wrook2move = game_state[3]
    brook1move = game_state[4]
    brook2move = game_state[5]
    total_game_state = []
    statenumber = len(game_state_white)
    new_white_state = []


    if white_move == "castle king":
        for n in range(statenumber):
            if wrook2move[n] == 0 and not ((6, 1) in total_attacks_black(n)) and not (
                    (7, 1) in total_attacks_black(n)) and not ((6, 1) in black_occupied(n)) and not (
                    (7, 1) in black_occupied(n)) and not ((7, 1) in white_occupied(n)) and not (
                    (6, 1) in white_occupied(n)):
                x = []
                for o in game_state_white: x.append(o)
                wpawn_state_change(n, 12, "King", (7, 1))
                wpawn_state_change(n, 15, "Rook", (6, 1))
                new_white_state.append((game_state_white[n], game_state_black[n]))
                newbrook1move.append(brook1move[n])
                newbrook2move.append(brook2move[n])
                newwrook1move.append(1)
                newwrook2move.append(1)
                game_state_white = x
    if white_move == "castle queen":
        for n in range(statenumber):
            if wrook1move[n] == 0 and not ((2, 1) in total_attacks_black(n)) and not (
                    (3, 1) in total_attacks_black(n)) and not ((2, 1) in black_occupied(n)) and not (
                    (3, 1) in black_occupied(n)) and not ((2, 1) in white_occupied(n)) and not (
                    (3, 1) in white_occupied(n)) and not (
                    (4, 1) in white_occupied(n)) and not (
                    (4, 1) in black_occupied(n)) and not (
                    (4, 1) in total_attacks_black(n)):
                x = []
                for o in game_state_white: x.append(o)
                wpawn_state_change(n, 12, "King", (3, 1))
                wpawn_state_change(n, 8, "Rook", (4, 1))
                newbrook1move.append(brook1move[n])
                newbrook2move.append(brook2move[n])
                newwrook1move.append(1)
                newwrook2move.append(1)
                game_state_white = x
    if white_move != "castle king" and white_move != "castle queen":
        if white_move[0] == "x":
            kill = "true"
            if white_move[1] == "a":
                x = 1
            if white_move[1] == "b":
                x = 2
            if white_move[1] == "c":
                x = 3
            if white_move[1] == "d":
                x = 4
            if white_move[1] == "e":
                x = 5
            if white_move[1] == "f":
                x = 6
            if white_move[1] == "g":
                x = 7
            if white_move[1] == "h":
                x = 8
            y = int(white_move[2])
            if len(white_move) > 4:
                checkstate = "true"
            else:
                checkstate = "false"
        else:
            kill = "false"
            if white_move[0] == "a":
                x = 1
            if white_move[0] == "b":
                x = 2
            if white_move[0] == "c":
                x = 3
            if white_move[0] == "d":
                x = 4
            if white_move[0] == "e":
                x = 5
            if white_move[0] == "f":
                x = 6
            if white_move[0] == "g":
                x = 7
            if white_move[0] == "h":
                x = 8
            y = int(white_move[1])
        checkstate = "false"
        if len(white_move) > 4:
            checkstate = "true"
        position = (x, y)  # NOT X Y!!!
        a = x
        b = y
        for n in range(statenumber):
            whitestate = game_state_white
            blackstate = game_state_black
            if (position in black_occupied(n) and kill == "true") or (
                    not (position in black_occupied(n)) and kill == "false"):
                if position in total_attacks_white(n):

                    if position in attack_wPawn1(n):
                        x = game_state_white[n].copy()
                        y = game_state_black[n].copy()
                        state = game_state_white[n][0][0]
                        wpawn_state_change(n, 0, state, position)
                        white_standard_move()

                        if game_state_white[n][0][1][1] == 8:
                            if game_state_white[n][0][0] == "Pawn":
                                new_pawn_state = input("What should the Pawn become (Rook, Knight, Bishop, Queen): ")
                                if len(new_pawn_state) > 1:
                                    x = game_state_white[n]
                                    wpawn_state_change(n, 0, new_pawn_state, position)
                                    white_standard_move()
                        game_state_white[n] = x
                        game_state_black[n] = y
                    if position in attack_wPawn2(n):
                        x = game_state_white[n].copy()
                        y = game_state_black[n].copy()
                        state = game_state_white[n][1][0]
                        wpawn_state_change(n, 1, state, position)
                        white_standard_move()
                        if game_state_white[n][1][1][1] == 8:
                            if game_state_white[n][1][0] == "Pawn":
                                new_pawn_state = input("What should the Pawn become (Rook, Knight, Bishop, Queen): ")
                                if len(new_pawn_state) > 1:
                                    x = game_state_white[n]
                                    wpawn_state_change(n, 1, new_pawn_state, position)
                                    white_standard_move()
                        game_state_white[n] = x
                        game_state_black[n] = y
                    if position in attack_wPawn3(n):
                        y = game_state_black[n].copy()
                        x = game_state_white[n].copy()
                        state = game_state_white[n][2][0]
                        wpawn_state_change(n, 2, state, position)
                        white_standard_move()

                        if game_state_white[n][2][1][1] == 8:
                            if game_state_white[n][2][0] == "Pawn":
                                new_pawn_state = input("What should the Pawn become (Rook, Knight, Bishop, Queen): ")
                                if len(new_pawn_state) > 1:
                                    x = game_state_white[n]
                                    wpawn_state_change(n, 2, new_pawn_state, position)
                                    white_standard_move()
                        game_state_white[n] = x
                        game_state_black[n] = y
                    if position in attack_wPawn4(n):
                        y = game_state_black[n].copy()
                        x = game_state_white[n].copy()
                        state = game_state_white[n][3][0]
                        wpawn_state_change(n, 3, state, position)
                        white_standard_move()

                        if game_state_white[n][3][1][1] == 8:
                            if game_state_white[n][3][0] == "Pawn":
                                new_pawn_state = input("What should the Pawn become (Rook, Knight, Bishop, Queen): ")
                                if len(new_pawn_state) > 1:
                                    x = game_state_white[n]
                                    wpawn_state_change(n, 3, new_pawn_state, position)
                                    white_standard_move()
                        game_state_white[n] = x
                        game_state_black[n] = y
                    if position in attack_wPawn5(n):
                        x = game_state_white[n].copy()
                        y = game_state_black[n].copy()
                        state = game_state_white[n][4][0]
                        wpawn_state_change(n, 4, state, position)
                        white_standard_move()

                        if game_state_white[n][4][1][1] == 8:
                            if game_state_white[n][4][0] == "Pawn":
                                new_pawn_state = input("What should the Pawn become (Rook, Knight, Bishop, Queen): ")
                                if len(new_pawn_state) > 1:
                                    x = game_state_white[n]
                                    wpawn_state_change(n, 4, new_pawn_state, position)
                                    white_standard_move()
                        game_state_white[n] = x
                        game_state_black[n] = y
                    if position in attack_wPawn6(n):
                        x = game_state_white[n].copy()
                        y = game_state_black[n].copy()
                        state = game_state_white[n][5][0]
                        wpawn_state_change(n, 5, state, position)
                        white_standard_move()

                        if game_state_white[n][5][1][1] == 8:
                            if game_state_white[n][5][0] == "Pawn":
                                new_pawn_state = input("What should the Pawn become (Rook, Knight, Bishop, Queen): ")
                                if len(new_pawn_state) > 1:
                                    x = game_state_white[n]
                                    wpawn_state_change(n, 5, new_pawn_state, position)
                                    white_standard_move()
                        game_state_white[n] = x
                        game_state_black[n] = y
                    if position in attack_wPawn7(n):
                        x = game_state_white[n].copy()
                        y = game_state_black[n].copy()
                        state = game_state_white[n][6][0]
                        wpawn_state_change(n, 6, state, position)
                        white_standard_move()

                        if game_state_white[n][6][1][1] == 8:
                            if game_state_white[n][6][0] == "Pawn":
                                new_pawn_state = input("What should the Pawn become (Rook, Knight, Bishop, Queen): ")
                                if len(new_pawn_state) > 1:
                                    x = game_state_white[n]
                                    wpawn_state_change(n, 6, new_pawn_state, position)
                                    white_standard_move()
                        game_state_white[n] = x
                        game_state_black[n] = y
                    if position in attack_wPawn8(n):
                        x = game_state_white[n].copy()
                        y = game_state_black[n].copy()
                        state = game_state_white[n][7][0]
                        wpawn_state_change(n, 7, state, position)
                        white_standard_move()

                        if game_state_white[n][7][1][1] == 8:
                            if game_state_white[n][7][0] == "Pawn":
                                new_pawn_state = input("What should the Pawn become (Rook, Knight, Bishop, Queen): ")
                                if len(new_pawn_state) > 1:
                                    x = game_state_white[n]
                                    wpawn_state_change(n, 7, new_pawn_state, position)
                                    white_standard_move()
                        game_state_white[n] = x
                        game_state_black[n] = y
                    if position in attack_wRook1(n):
                        x = game_state_white[n].copy()
                        y = game_state_black[n].copy()
                        wpawn_state_change(n, 8, "Rook", position)
                        if checkstate == "true":
                            if position in black_occupied(n):
                                black_remove(position, n)
                            if bKing(n) in total_attacks_white(n):

                                if not (wKing(n) in total_attacks_black(n)):
                                    new_white_state.append((game_state_white[n], game_state_black[n]))
                                    newbrook1move.append(brook1move[n])
                                    newbrook2move.append(brook2move[n])
                                    newwrook1move.append(1)
                                    newwrook2move.append(wrook2move[n])
                        if checkstate == "false":
                            if position in black_occupied(n):
                                black_remove(position, n)
                            if not (bKing(n) in total_attacks_white(n)):

                                if not (wKing(n) in total_attacks_black(n)):
                                    new_white_state.append((game_state_white[n], game_state_black[n]))
                                    newbrook1move.append(brook1move[n])
                                    newbrook2move.append(brook2move[n])
                                    newwrook1move.append(1)
                                    newwrook2move.append(wrook2move[n])
                        game_state_white[n] = x
                        game_state_black[n] = y
                    if position in attack_wKnight1(n):
                        y = game_state_black[n].copy()
                        x = game_state_white[n].copy()
                        wpawn_state_change(n, 9, "Knight", position)
                        white_standard_move()
                        game_state_white[n] = x
                        game_state_black[n] = y
                    if position in attack_wBishop1(n):
                        x = game_state_white[n].copy()
                        y = game_state_black[n].copy()
                        wpawn_state_change(n, 10, "Bishop", position)
                        white_standard_move()
                        game_state_white[n] = x
                        game_state_black[n] = y
                    if position in attack_wQueen(n):
                        x = game_state_white[n].copy()
                        y = game_state_black[n].copy()
                        wpawn_state_change(n, 11, "Queen", position)
                        white_standard_move()
                        game_state_white[n] = x
                        game_state_black[n] = y
                    if position in attack_wKing(n):
                        x = game_state_white[n].copy()
                        y = game_state_black[n].copy()
                        wpawn_state_change(n, 12, "King", position)
                        if checkstate == "true":
                            if position in black_occupied(n):
                                black_remove(position, n)
                            if bKing(n) in total_attacks_white(n):
                                if not (wKing(n) in total_attacks_black(n)):
                                    new_white_state.append((game_state_white[n], game_state_black[n]))

                                    newbrook1move.append(brook1move[n])
                                    newbrook2move.append(brook2move[n])

                                    newwrook1move.append(1)
                                    newwrook2move.append(1)
                        if checkstate == "false":
                            if position in black_occupied(n):
                                black_remove(position, n)
                            if not (bKing(n) in total_attacks_white(n)):
                                if not (wKing(n) in total_attacks_black(n)):
                                    new_white_state.append((game_state_white[n], game_state_black[n]))
                                    newbrook1move.append(brook1move[n])
                                    newbrook2move.append(brook2move[n])
                                    newwrook1move.append(1)
                                    newwrook2move.append(1)
                        game_state_white[n] = x
                        game_state_black[n] = y
                    if position in attack_wBishop2(n):
                        y = game_state_black[n].copy()
                        x = game_state_white[n].copy()
                        wpawn_state_change(n, 13, "Bishop", position)
                        white_standard_move()
                        game_state_white[n] = x
                        game_state_black[n] = y
                    if position in attack_wKnight2(n):
                        x = game_state_white[n].copy()
                        y = game_state_black[n].copy()
                        wpawn_state_change(n, 14, "Knight", position)
                        white_standard_move()
                        game_state_white[n] = x
                        game_state_black[n] = y
                    if position in attack_wRook2(n):
                        y = game_state_black[n].copy()
                        x = game_state_white[n].copy()
                        wpawn_state_change(n, 15, "Rook", position)
                        if checkstate == "true":
                            if position in black_occupied(n):
                                black_remove(position, n)
                            if bKing(n) in total_attacks_white(n):
                                if not (wKing(n) in total_attacks_black(n)):
                                    new_white_state.append((game_state_white[n], game_state_black[n]))
                                    new_black_state.append((game_state_black[n], game_state_white[n]))
                                    newbrook1move.append(brook1move[n])
                                    newbrook2move.append(brook2move[n])
                                    newwrook1move.append(wrook1move[n])
                                    newwrook2move.append(1)
                        if checkstate == "false":
                            if position in black_occupied(n):
                                black_remove(position, n)
                            if not (wKing(n) in total_attacks_black(n)):
                                if not (bKing(n) in total_attacks_white(n)):
                                    new_white_state.append((game_state_white[n], game_state_black[n]))
                                    new_black_state.append((game_state_black[n], game_state_white[n]))
                                    newbrook1move.append(brook1move[n])
                                    newbrook2move.append(brook2move[n])
                                    newwrook1move.append(wrook1move[n])
                                    newwrook2move.append(1)
                        game_state_white[n] = x
                        game_state_black[n] = y

    new_white_state = set(tuple(tuple(q) for q in t) for t in new_white_state)
    new_white_state = list(list(list(q) for q in t) for t in new_white_state)

    if len(new_white_state) == 0:
        print("Turn impossible")
        bskip = 1
        return(game_state)
    else:
        game.append(white_move)
        bskip = 0
        brook1move = newbrook1move
        brook2move = newbrook2move
        wrook1move = newwrook1move
        wrook2move = newwrook2move
        game_state_white = []
        game_state_black = []
        game_state = []
        for r in new_white_state:
            game_state_white.append(r[0])
            game_state_black.append(r[1])
        game_state.append(game_state_white)
        game_state.append(game_state_black)
        game_state.append(wrook1move)
        game_state.append(wrook2move)
        game_state.append(brook1move)
        game_state.append(brook2move)
        return game_state




def make_move_black(black_move, game_state):

    global wskip, bskip, wrook1move, brook1move
    global wrook2move, brook2move
    global game_state_white, game_state_black
    global checkstate
    global position
    global new_black_state, newbrook1move, newbrook2move
    global newwrook1move, newwrook2move, newblack_state
    global n

    newbrook1move = []
    newbrook2move = []
    newwrook1move = []
    newwrook2move = []
    new_white_state = []  # pair of (whitestate, blackstate)
    new_black_state = []
    statenumber = len(game_state_white)
    game_state_white = game_state[0]
    game_state_black = game_state[1]
    wrook1move = game_state[2]
    wrook2move = game_state[3]
    brook1move = game_state[4]
    brook2move = game_state[5]
    statenumber = len(game_state_black)
    new_white_state = []
    if black_move == "castle king":
        for n in range(statenumber):
            if brook2move[n] == 0 and not ((6, 8) in total_attacks_white(n)) and not (
                    (7, 8) in total_attacks_white(n)) and not ((6, 8) in black_occupied(n)) and not (
                    (7, 8) in black_occupied(n)) and not ((7, 8) in white_occupied(n)) and not (
                    (6, 8) in white_occupied(n)):
                x = []
                for o in game_state_black: x.append(o)
                bpawn_state_change(n, 12, "King", (7, 8))
                bpawn_state_change(n, 15, "Rook", (6, 8))
                new_black_state.append((game_state_black[n], game_state_white[n]))
                newbrook1move.append(1)
                newbrook2move.append(1)
                newwrook1move.append(wrook1move[n])
                newwrook2move.append(wrook2move[n])
                game_state_black = x
    if black_move == "castle queen":
        for n in range(statenumber):
            if brook1move[n] == 0 and not ((2, 8) in total_attacks_white(n)) and not (
                    (3, 8) in total_attacks_white(n)) and not ((2, 8) in black_occupied(n)) and not (
                    (3, 8) in black_occupied(n)) and not ((2, 8) in white_occupied(n)) and not (
                    (3, 8) in white_occupied(n)) and not (
                    (4, 8) in white_occupied(n)) and not (
                    (4, 8) in black_occupied(n)) and not (
                    (4, 8) in total_attacks_white(n)):
                x = []
                for o in game_state_white: x.append(o)
                bpawn_state_change(n, 12, "King", (3, 8))
                bpawn_state_change(n, 8, "Rook", (4, 8))
                new_black_state.append((game_state_black[n], game_state_white[n]))
                newbrook1move.append(1)
                newbrook2move.append(1)
                newwrook1move.append(wrook1move[n])
                newwrook2move.append(wrook2move[n])
                game_state_white = x
    if black_move != "castle king" and black_move != "castle queen":
        if black_move[0] == "x":
            kill = "true"
            if black_move[1] == "a":
                x = 1
            if black_move[1] == "b":
                x = 2
            if black_move[1] == "c":
                x = 3
            if black_move[1] == "d":
                x = 4
            if black_move[1] == "e":
                x = 5
            if black_move[1] == "f":
                x = 6
            if black_move[1] == "g":
                x = 7
            if black_move[1] == "h":
                x = 8
            y = int(black_move[2])
            if len(black_move) > 4:
                checkstate = "true"
            else:
                checkstate = "false"
        else:
            kill = "false"
            if black_move[0] == "a":
                x = 1
            if black_move[0] == "b":
                x = 2
            if black_move[0] == "c":
                x = 3
            if black_move[0] == "d":
                x = 4
            if black_move[0] == "e":
                x = 5
            if black_move[0] == "f":
                x = 6
            if black_move[0] == "g":
                x = 7
            if black_move[0] == "h":
                x = 8
            y = int(black_move[1])
        checkstate = "false"
        if len(black_move) > 4:
            checkstate = "true"
        position = (x, y)  # NOT X Y!!!
        a = x
        b = y
        for n in range(statenumber):

            blackstate = game_state_black
            whitestate = game_state_white
            if (position in white_occupied(n) and kill == "true") or (
                    not (position in white_occupied(n)) and kill == "false"):
                if position in total_attacks_black(n):

                    if position in attack_bPawn1(n):
                        x = game_state_black[n].copy()
                        y = game_state_white[n].copy()
                        state = game_state_black[n][0][0]
                        bpawn_state_change(n, 0, state, position)
                        black_standard_move()

                        if game_state_black[n][0][1][1] == 8:
                            if game_state_black[n][0][0] == "Pawn":
                                new_pawn_state = input("What should the Pawn become (Rook, Knight, Bishop, Queen): ")
                                if len(new_pawn_state) > 1:
                                    x = game_state_black[n]
                                    bpawn_state_change(n, 0, new_pawn_state, position)
                                    black_standard_move()
                        game_state_black[n] = x
                        game_state_white[n] = y
                    if position in attack_bPawn2(n):
                        x = game_state_black[n].copy()
                        y = game_state_white[n].copy()
                        state = game_state_black[n][1][0]
                        bpawn_state_change(n, 1, state, position)
                        black_standard_move()
                        if game_state_black[n][1][1][1] == 8:
                            if game_state_black[n][1][0] == "Pawn":
                                new_pawn_state = input("What should the Pawn become (Rook, Knight, Bishop, Queen): ")
                                if len(new_pawn_state) > 1:
                                    x = game_state_black[n]
                                    bpawn_state_change(n, 1, new_pawn_state, position)
                                    black_standard_move()
                        game_state_black[n] = x
                        game_state_white[n] = y
                    if position in attack_bPawn3(n):
                        x = game_state_black[n].copy()
                        y = game_state_white[n].copy()
                        state = game_state_black[n][2][0]
                        bpawn_state_change(n, 2, state, position)
                        black_standard_move()

                        if game_state_black[n][2][1][1] == 8:
                            if game_state_black[n][2][0] == "Pawn":
                                new_pawn_state = input("What should the Pawn become (Rook, Knight, Bishop, Queen): ")
                                if len(new_pawn_state) > 1:
                                    x = game_state_black[n]
                                    bpawn_state_change(n, 2, new_pawn_state, position)
                                    black_standard_move()
                        game_state_black[n] = x
                        game_state_white[n] = y
                    if position in attack_bPawn4(n):
                        x = game_state_black[n].copy()
                        y = game_state_white[n].copy()
                        state = game_state_black[n][3][0]
                        bpawn_state_change(n, 3, state, position)
                        black_standard_move()

                        if game_state_black[n][3][1][1] == 8:
                            if game_state_black[n][3][0] == "Pawn":
                                new_pawn_state = input("What should the Pawn become (Rook, Knight, Bishop, Queen): ")
                                if len(new_pawn_state) > 1:
                                    x = game_state_black[n]
                                    bpawn_state_change(n, 3, new_pawn_state, position)
                                    black_standard_move()
                        game_state_black[n] = x
                        game_state_white[n] = y
                    if position in attack_bPawn5(n):
                        x = game_state_black[n].copy()
                        y = game_state_white[n].copy()
                        state = game_state_black[n][4][0]
                        bpawn_state_change(n, 4, state, position)
                        black_standard_move()

                        if game_state_black[n][4][1][1] == 8:
                            if game_state_black[n][4][0] == "Pawn":
                                new_pawn_state = input("What should the Pawn become (Rook, Knight, Bishop, Queen): ")
                                if len(new_pawn_state) > 1:
                                    x = game_state_white[n]
                                    bpawn_state_change(n, 4, new_pawn_state, position)
                                    black_standard_move()
                        game_state_black[n] = x
                        game_state_white[n] = y
                    if position in attack_bPawn6(n):
                        x = game_state_black[n].copy()
                        y = game_state_white[n].copy()
                        state = game_state_black[n][5][0]
                        bpawn_state_change(n, 5, state, position)
                        black_standard_move()

                        if game_state_black[n][5][1][1] == 8:
                            if game_state_black[n][5][0] == "Pawn":
                                new_pawn_state = input("What should the Pawn become (Rook, Knight, Bishop, Queen): ")
                                if len(new_pawn_state) > 1:
                                    x = game_state_white[n]
                                    bpawn_state_change(n, 5, new_pawn_state, position)
                                    black_standard_move()
                        game_state_black[n] = x
                        game_state_white[n] = y
                    if position in attack_bPawn7(n):
                        x = game_state_black[n].copy()
                        y = game_state_white[n].copy()
                        state = game_state_black[n][6][0]
                        bpawn_state_change(n, 6, state, position)
                        black_standard_move()

                        if game_state_black[n][6][1][1] == 8:
                            if game_state_black[n][6][0] == "Pawn":
                                new_pawn_state = input("What should the Pawn become (Rook, Knight, Bishop, Queen): ")
                                if len(new_pawn_state) > 1:
                                    x = game_state_white[n]
                                    bpawn_state_change(n, 6, new_pawn_state, position)
                                    black_standard_move()
                        game_state_black[n] = x
                        game_state_white[n] = y
                    if position in attack_bPawn8(n):
                        x = game_state_black[n].copy()
                        y = game_state_white[n].copy()
                        state = game_state_black[n][7][0]
                        bpawn_state_change(n, 7, state, position)
                        black_standard_move()

                        if game_state_black[n][7][1][1] == 8:
                            if game_state_black[n][7][0] == "Pawn":
                                new_pawn_state = input("What should the Pawn become (Rook, Knight, Bishop, Queen): ")
                                if len(new_pawn_state) > 1:
                                    x = game_state_black[n]
                                    bpawn_state_change(n, 7, new_pawn_state, position)
                                    black_standard_move()
                        game_state_black[n] = x
                        game_state_white[n] = y
                    if position in attack_bRook1(n):
                        x = game_state_black[n].copy()
                        y = game_state_white[n].copy()
                        bpawn_state_change(n, 8, "Rook", position)
                        if checkstate == "true":
                            if position in white_occupied(n):
                                white_remove(position, n)
                            if not (bKing(n) in total_attacks_white(n)):
                                if wKing(n) in total_attacks_black(n):
                                    new_black_state.append((game_state_black[n], game_state_white[n]))

                                    newbrook1move.append(1)
                                    newbrook2move.append(brook2move[n])

                                    newwrook1move.append(wrook1move[n])
                                    newwrook2move.append(wrook2move[n])

                        if checkstate == "false":
                            if position in white_occupied(n):
                                white_remove(position, n)
                            if not (bKing(n) in total_attacks_white(n)):
                                if not (wKing(n) in total_attacks_black(n)):
                                    new_black_state.append((game_state_black[n], game_state_white[n]))

                                    newbrook1move.append(1)
                                    newbrook2move.append(brook2move[n])

                                    newwrook1move.append(wrook1move[n])
                                    newwrook2move.append(wrook2move[n])

                        game_state_black[n] = x
                        game_state_white[n] = y
                    if position in attack_bKnight1(n):
                        x = game_state_black[n].copy()
                        y = game_state_white[n].copy()
                        bpawn_state_change(n, 9, "Knight", position)
                        black_standard_move()
                        game_state_black[n] = x
                        game_state_white[n] = y
                    if position in attack_bBishop1(n):
                        x = game_state_black[n].copy()
                        y = game_state_white[n].copy()
                        bpawn_state_change(n, 10, "Bishop", position)
                        black_standard_move()
                        game_state_black[n] = x
                        game_state_white[n] = y
                    if position in attack_bQueen(n):
                        x = game_state_black[n].copy()
                        y = game_state_white[n].copy()
                        bpawn_state_change(n, 11, "Queen", position)
                        black_standard_move()
                        game_state_black[n] = x
                        game_state_white[n] = y
                    if position in attack_bKing(n):
                        x = game_state_black[n].copy()
                        y = game_state_white[n].copy()
                        bpawn_state_change(n, 12, "King", position)
                        if checkstate == "true":
                            if position in white_occupied(n):
                                white_remove(position, n)
                            if not (bKing(n) in total_attacks_white(n)):
                                if wKing(n) in total_attacks_black(n):
                                    new_black_state.append((game_state_black[n], game_state_white[n]))

                                    newbrook1move.append(1)
                                    newbrook2move.append(1)

                                    newwrook1move.append(wrook1move[n])
                                    newwrook2move.append(wrook2move[n])

                        if checkstate == "false":
                            if position in white_occupied(n):
                                white_remove(position, n)
                            if not (bKing(n) in total_attacks_white(n)):
                                if not (wKing(n) in total_attacks_black(n)):
                                    new_black_state.append((game_state_black[n], game_state_white[n]))

                                    newbrook1move.append(1)
                                    newbrook2move.append(1)

                                    newwrook1move.append(wrook1move[n])
                                    newwrook2move.append(wrook2move[n])

                        game_state_black[n] = x
                        game_state_white[n] = y

                    if position in attack_bBishop2(n):
                        x = game_state_black[n].copy()
                        y = game_state_white[n].copy()
                        bpawn_state_change(n, 13, "Bishop", position)
                        black_standard_move()
                        game_state_black[n] = x
                        game_state_white[n] = y
                    if position in attack_bKnight2(n):
                        x = game_state_black[n].copy()
                        y = game_state_white[n].copy()
                        bpawn_state_change(n, 14, "Knight", position)
                        black_standard_move()
                        game_state_black[n] = x
                        game_state_white[n] = y
                    if position in attack_bRook2(n):
                        x = game_state_black[n].copy()
                        y = game_state_white[n].copy()
                        bpawn_state_change(n, 15, "Rook", position)
                        if checkstate == "true":
                            if position in white_occupied(n):
                                white_remove(position, n)
                            if not (bKing(n) in total_attacks_white(n)):
                                if wKing(n) in total_attacks_black(n):
                                    new_black_state.append((game_state_black[n], game_state_white[n]))

                                    newbrook1move.append(brook1move[n])
                                    newbrook2move.append(1)

                                    newwrook1move.append(wrook1move[n])
                                    newwrook2move.append(wrook2move[n])

                        if checkstate == "false":
                            if position in white_occupied(n):
                                white_remove(position, n)
                            if not (wKing(n) in total_attacks_black(n)):
                                if not (bKing(n) in total_attacks_white(n)):
                                    new_black_state.append((game_state_black[n], game_state_white[n]))

                                    newbrook1move.append(brook1move[n])
                                    newbrook2move.append(1)

                                    newwrook1move.append(wrook1move[n])
                                    newwrook2move.append(wrook2move[n])

                        game_state_black[n] = x
                        game_state_white[n] = y
    new_black_state = set(tuple(tuple(q) for q in t) for t in new_black_state)
    new_black_state = list(list(list(q) for q in t) for t in new_black_state)

    if len(new_black_state) == 0:
        print("Turn impossible")
        wskip = 1
        return(game_state)
    else:
        game_state = []
        game.append(black_move)
        wskip = 0
        brook1move = newbrook1move
        brook2move = newbrook2move
        wrook1move = newwrook1move
        wrook2move = newwrook2move
        game_state_white = []
        game_state_black = []
        for r in new_black_state:
            game_state_white.append(r[1])
            game_state_black.append(r[0])
        game_state.append(game_state_white)
        game_state.append(game_state_black)
        game_state.append(wrook1move)
        game_state.append(wrook2move)
        game_state.append(brook1move)
        game_state.append(brook2move)
        return game_state




def column(x):
    if x == 1:
        return "a"
    if x == 2:
        return "b"
    if x == 3:
        return "c"
    if x == 4:
        return "d"
    if x == 5:
        return "e"
    if x == 6:
        return "f"
    if x == 7:
        return "g"
    if x == 8:
        return "h"


for turn in range (6000):
  if wskip == 0:
      statenumber = len(game_state_white)
      print("The number of possible states is: " + str(statenumber))
      print("Make a move, White: ")
      total_game_state = []
      for n in range(statenumber):
          total_game_state.append([game_state_white[n], game_state_black[n]])
      starte_viewer_mit_positionen(total_game_state)
      white_move = input( )

      game_state = make_move_white(white_move, game_state)





  if bskip == 0:
      statenumber = len(game_state_black)
      print("The number of possible states is: " + str(statenumber))
      print("Make a move, Black: ")
      total_game_state = []
      for n in range(statenumber):
          total_game_state.append([game_state_white[n], game_state_black[n]])
      starte_viewer_mit_positionen(total_game_state)
      black_move = input( )

      game_state = make_move_black(black_move, game_state)



print(game)

