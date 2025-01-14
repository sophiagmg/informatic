import tkinter as tk
import snake_ta6 as sn

app = tk.Tk()  # Erzeugt ein neues "GUI"-Objekt vom Typ Tk
app.geometry('465x560')  # Definiert die Abmaße des Hauptfensters
app.resizable(0, 0)  # Sperrt die Abmaße des Hauptfensters
app.title('Snake')  # Schreibt einen Title in die Statuszeile
game = sn.Game(app, 435, 435)  # Erzeugt ein neues Objekt des Typs Game

tk.mainloop()  # Zeigt das GUI auf dem Bildschirm an