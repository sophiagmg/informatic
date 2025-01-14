# Siehe Kommentare vom Arbeitsblatt

import tkinter as tk
import random
import time
from tkinter import messagebox

LAENGE_SCHLANGE = 2
START_POS_X = 155
START_POS_Y = 155

class Game(tk.Frame):

    def __init__(self, master, breite, hoehe):

        super(Game, self).__init__(master)
        self.master = master
        self.breite = breite
        self.hoehe = hoehe

        # Die folgenden Zeilen erzeugen das Spielfeld
        self.spielfeld = tk.Canvas(self.master, bg='black', bd=5, relief='sunken')
        self.spielfeld.place(x=15, y=10, height=self.hoehe, width=self.breite)

        # Die folgenden Zeilen erzeugen das Frame für alle Labels, Buttons und das Scale
        self.frame = tk.Frame(bg='grey')
        self.frame.place(x=19, y=450, height=95, width=self.breite-10)

        # Die folgenden Zeilen erzeugen die Labels
        self.label_punkte = tk.Label(self.frame, bg='white', anchor='w', text='Punkte:', font=('arial', 12, 'bold'))
        self.label_punkte.place(x=5, y=5, height=25, width=80)

        self.rekord = tk.Label(self.frame, bg='white', anchor='w', text='Rekord:', font=('arial', 12, 'bold'))
        self.rekord.place(x=5, y=35, height=25, width=80)

        self.spielzeit = tk.Label(self.frame, bg='white', anchor='w', text='Spielzeit:', font=('arial', 12, 'bold'))
        self.spielzeit.place(x=5, y=65, height=25, width=80)

        self.punktestand = tk.Label(self.frame, bg='white', relief='sunken', text='0', font=('arial', 12, 'normal'))
        self.punktestand.place(x=100, y=5, height=25, width=50)

        self.rekordstand = tk.Label(self.frame, bg='white', relief='sunken', text='0', font=('arial', 12, 'normal'))
        self.rekordstand.place(x=100, y=35, height=25, width=50)

        self.spielzeitstand = tk.Label(self.frame, bg='white', relief='sunken', text='0', font=('arial', 12, 'normal'))
        self.spielzeitstand.place(x=100, y=65, height=25, width=50)

        self.geschwindigkeitsanzeige = tk.Label(self.frame, bg='white', text='Geschwindigkeit:', font=('arial', 12, 'bold'))
        self.geschwindigkeitsanzeige.place(x=165, y=3, height=25, width=150)

        # Die folgenden Zeilen erzeugen ein Scale um die Geschwindigkeit einzustellen
        self.geschwindigkeit = tk.IntVar(None, 1)
        self.geschwindigkeit_regler = tk.Scale(self.frame, orient='horizontal', variable=self.geschwindigkeit,
                                               from_=420, to=20, sliderlength=10, tickinterval=100, bg='white',
                                               troughcolor='red', resolution=10,width=10, relief='sunken',
                                               font=('arial', 10, 'normal'))
        self.geschwindigkeit_regler.place(x=165, y=32, width=150, height=60)

        # Die folgenden Zeilen erzeugen die Buttons
        self.start = tk.Button(self.frame, bg='grey', relief='raised', text='START', font=('arial', 12, 'bold'))
        self.start.place(x=335, y=15, height=25, width=75)
        self.start.config(command=self.starte_spiel)    # Das Spiel wird gestartet

        self.ende = tk.Button(self.frame, bg='grey', relief='raised', text='ENDE', font=('arial', 12, 'bold'))
        self.ende.place(x=335, y=58, height=25, width=75)
        self.ende.config(command=self.master.destroy)
        # Die Zeile konfiguriert den Button, damit das Programm zu Ende geht, wenn er gedrückt wird


        self.neues_spiel = True  # überprüft ob das Spiel läuft

        self.schlange = []  # leere Liste wird erstellt

        # die Bilder werden eingeführt
        self.kopf_img = tk.PhotoImage(file='images/kopf.png')

        self.koerper_img = tk.PhotoImage(file='images/koerper.png')

        self.futter_img = tk.PhotoImage(file='images/futter.png')

        # die Labels für Kopf und Futter werden erstellt
        self.kopf = tk.Label(self.spielfeld, bg='black', image=self.kopf_img)

        self.futter = tk.Label(self.spielfeld, bg='black', image=self.futter_img)
        self.futter.lower(self.kopf)

        self.neu = True  # variable neu wird auf true gesetzt

        self.highscore = 0

        self.start_zeit = None

        self.belohnung_x = 0
        self.belohnung_y = 0

        self.wiederholen = True

        self.x_richtung = 1
        # Die Richtung in die die Schlange sich bewegt wird bestimmt
        self.y_richtung = 0
        self.punkte = 0     # Der Punktestand wird auf 0 gesetzt
        self.starten = False    # Die Variabel starten wird auf Falsch gesetzt

        self.game_over = False

        self.erzeuge_schlange()     # die Schlange wird einmalig aufgerufen
        self.tasten_funktionen()    # Die Methode der Tasten wird aufgerufen
        self.erzeuge_belohnung()
        self.aktualisiere()


    def erzeuge_schlange(self):  # neue Methode für die Schlange

        if self.neues_spiel == True:  # wenn das Spiel läuft, dann wird das Programm abgespielt
            self.schlange.append(self.kopf)  # ruft den Kopf der Schlange auf
            self.schlange[0].place(x=START_POS_X, y=START_POS_Y, height=25, width=25)

            for i in range(LAENGE_SCHLANGE):    # Eine Schleife für den Körperteil wird erstellt
                koerperteil = tk.Label(self.spielfeld, bg='black', image=self.koerper_img)
                # Der Variable Körperteil wird ein Bild zugewiesen
                self.schlange.append(koerperteil)
                koerperteil.place(x=START_POS_X - (i+1) * 25, y=START_POS_Y, height=25, width=25)
                # Der Ort des nächsten Körperteil der Schlange wird bestimmt
            self.neues_spiel = False


    # die methoden links, rechts, oben und unten werden erstellt
    def links(self, event):
        if self.neu == True:
            if self.x_richtung != 1:
                self.x_richtung = -1
                self.y_richtung = 0
        self.neu = False

    def rechts(self, event):
        if self.neu == True:
            if self.x_richtung != -1:
                self.x_richtung = 1
                self.y_richtung = 0
        self.neu = False

    def hoch(self, event):
        if self.neu == True:
            if self.y_richtung != -1:
                self.x_richtung = 0
                self.y_richtung = 1
        self.neu = False

    def runter(self, event):
        if self.neu == True:
            if self.y_richtung != 1:
                self.x_richtung = 0
                self.y_richtung = -1
        self.neu = False


    # die tastenfunktion wird aktiviert
    def tasten_funktionen(self):
        self.master.bind('<Left>', self.links)
        self.master.bind('<Right>', self.rechts)
        self.master.bind('<Up>', self.hoch)
        self.master.bind('<Down>', self.runter)


    # das Spiel wird gestartet
    def starte_spiel(self):
        self.starten = True
        self.start_zeit = time.time()  # Startzeit setzen


    # die Bewegung der Schlange wird definiert
    def bewege_schlange(self):
        # Die Variablen für den Ort des Kopfes werden erstellt
        kopf_x = self.schlange[0].winfo_x()
        kopf_y = self.schlange[0].winfo_y()


        self.game_over = self.pruefe_kollision()  # Setze Game-Over Status, falls Kollision
        if self.game_over:
            messagebox.showinfo("Game over", f"Du hast {self.punkte} Punkte erreicht!")
            self.starten = False  # Stoppe das Spiel

        # Berechnung der neuen Position des Kopfes
        if self.x_richtung == 1:
            x = kopf_x + 25
            y = kopf_y
        elif self.x_richtung == -1:
            x = kopf_x - 25
            y = kopf_y
        elif self.y_richtung == 1:
            x = kopf_x
            y = kopf_y - 25
        elif self.y_richtung == -1:
            x = kopf_x
            y = kopf_y + 25

        # Bewegt die restlichen Körperteile (von hinten nach vorne)
        for koerper in self.schlange:
            koerper.place(x=x, y=y, height=25, width=25)
            x = koerper.winfo_x()
            y = koerper.winfo_y()


    # Methode zum Erzeugen einer Belohnung (Futter)
    # Methode zum Erzeugen einer Belohnung (Futter)
    def erzeuge_belohnung(self):
        self.wiederholen = True  # Flag, um sicherzustellen, dass die Belohnung nicht auf der Schlange erscheint

        if self.punkte == 0:  # Wenn der Punktestand 0 ist, wird die Belohnung an einer festen Position erzeugt
            self.belohnung_x = START_POS_X + 150  # X-Position der Belohnung
            self.belohnung_y = START_POS_Y  # Y-Position der Belohnung
        else:
            while self.wiederholen:  # Solange wiederholen, bis die Belohnung nicht auf der Schlange erscheint
                # Belohnung wird an zufälliger Position innerhalb des Spielfelds erzeugt
                self.belohnung_x = random.choice(range(5, self.breite - 5, 25))  # Zufällige X-Position
                self.belohnung_y = random.choice(range(5, self.hoehe - 5, 25))  # Zufällige Y-Position
                self.wiederholen = False  # Setze das Wiederholen auf False, falls die Position okay ist

                # Überprüfen, ob die Belohnung auf einem Körperteil der Schlange liegt
                for koerperteil in self.schlange[1:]:  # Überprüft nur den Körper, nicht den Kopf
                    if koerperteil.winfo_x() == self.belohnung_x and koerperteil.winfo_y() == self.belohnung_y:
                        self.wiederholen = True  # Wenn die Belohnung auf einem Körperteil liegt, wiederhole die Position
                        break  # Brich die Schleife ab, um eine neue Position zu berechnen

        # Setzt die Belohnung auf das Spielfeld
        self.futter.place(x=self.belohnung_x, y=self.belohnung_y, width=25, height=25)

    # Methode zum Prüfen, ob die Schlange die Belohnung gefressen hat
    def pruefe_belohnung(self):
        x = self.schlange[0].winfo_x()  # X-Position des Kopfes der Schlange
        y = self.schlange[0].winfo_y()  # Y-Position des Kopfes der Schlange

        if x == self.belohnung_x and y == self.belohnung_y:  # Wenn der Kopf der Schlange die Belohnung erreicht
            self.punkte += 1  # Erhöht den Punktestand
            self.punktestand.config(text=str(self.punkte))  # Aktualisiert die Punktanzeige

            if self.punkte > self.highscore:
                self.highscore = self.punkte  # Aktualisiere den Rekord
                self.rekordstand.config(text=str(self.highscore))  # Aktualisiere das Rekord-Label

            self.erzeuge_belohnung()  # Erzeugt eine neue Belohnung

            # Fügt ein neues Körperteil zur Schlange hinzu
            neues_teil = tk.Label(self.spielfeld, bg='black', image=self.koerper_img)
            self.schlange.append(neues_teil)  # Das neue Körperteil wird an die Schlange angehängt

    def pruefe_kollision(self):

        # Prüft, ob der Kopf der Schlange mit einer Wand kollidiert
        kopf_x = self.schlange[0].winfo_x()
        kopf_y = self.schlange[0].winfo_y()

        # Wandkollisionen (je nach Spielfeldgröße)
        if kopf_x < 0 or kopf_x >= self.breite - 25 or kopf_y < 0 or kopf_y >= self.hoehe - 25:
            return True

        # Kollision mit dem eigenen Körper
        for koerperteil in self.schlange[1:]:
            if kopf_x == koerperteil.winfo_x() and kopf_y == koerperteil.winfo_y():
                return True

        return False

    def loesche_schlange(self):
        for koerper in self.schlange[1:]:  # Iteriere durch alle Teile der Schlange
            koerper.destroy()  # Zerstöre jedes Teil
        self.schlange.clear()  # Lösche alle Elemente in der Schlange-Liste

    def initialisiere(self):
        # Löscht alle bisherigen Schlange-Teile und setzt alle wichtigen Spielparameter zurück
        self.loesche_schlange()  # Löscht alle Teile der Schlange von der Anzeige

        self.neu = True  # Setzt die Variable neu auf True, um zu signalisieren, dass die Schlange neu initialisiert wird

        # Setzt die Position der Belohnung (Futter) auf 0 (wird später neu platziert)
        self.belohnung_x = 0
        self.belohnung_y = 0

        # Setzt die Bewegungsrichtung der Schlange auf 0 (keine Bewegung zu Beginn)
        self.x_richtung = 0
        self.y_richtung = 0

        # Setzt den Punktestand auf 0 und aktualisiert das Punktestand-Label
        self.punkte = 0
        self.punktestand.config(text='0')

        # Setzt die Spielzeit auf 0 und aktualisiert das Spielzeit-Label
        self.start_zeit = 0
        self.spielzeitstand.config(text='0')

        # Setzt den Spielzustand so, dass das Spiel nicht gestartet ist und das Spiel noch nicht vorbei ist
        self.starten = False
        self.game_over = False

        # Markiert, dass ein neues Spiel begonnen wird
        self.neues_spiel = True

        # Leert die Schlange, da wir ein neues Spiel starten
        self.schlange = []

        # Setzt die Bewegungsrichtung der Schlange auf "nach rechts"
        self.x_richtung = 1
        self.y_richtung = 0

        # Erzeugt die Schlange und das Futter neu
        self.erzeuge_schlange()  # Erzeugt die Schlange
        self.erzeuge_belohnung()  # Erzeugt die Belohnung (Futter)

        # Markiert, dass das neue Spiel initialisiert wurde
        self.neues_spiel = False

    # Methode zum Aktualisieren des Spiels
    def aktualisiere(self):
        # Diese Methode wird alle 500ms aufgerufen, um das Spiel weiter laufen zu lassen
        if self.starten:  # Überprüft, ob das Spiel gerade läuft
            self.bewege_schlange()  # Bewegt die Schlange basierend auf der aktuellen Richtung
            self.pruefe_belohnung()  # Überprüft, ob die Schlange die Belohnung gefressen hat
            self.pruefe_kollision()  # Überprüft, ob die Schlange mit etwas kollidiert ist (Wand oder Körper)

            if self.start_zeit != None:  # Wenn das Spiel gestartet ist
                verstrichene_zeit = time.time() - self.start_zeit  # Berechnet die verstrichene Zeit seit dem Spielstart
                self.spielzeitstand.config(
                    text=f"{int(verstrichene_zeit)}")  # Aktualisiert die Spielzeit-Anzeige in Sekunden

        if self.game_over:  # Wenn das Spiel vorbei ist (Kollision oder anderes Spielende)
            self.initialisiere()  # Initialisiert das Spiel (setzt alles zurück)
            self.game_over = False  # Setzt den Spielstatus auf "nicht mehr vorbei"

        self.neu = True  # Setzt neu auf True, um anzuzeigen, dass das Spiel aktualisiert wurde

        # Ruft die Methode `aktualisiere` alle `self.geschwindigkeit.get()` Millisekunden wieder auf, um das Spiel fortzusetzen
        self.after(self.geschwindigkeit.get(), self.aktualisiere)  # Warten auf den nächsten Update-Zyklus
