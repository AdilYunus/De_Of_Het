import requests #import module requests
from bs4 import BeautifulSoup #import module BeautifulSoup
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
import sys


class Welklidwoord(QtWidgets.QDialog):

    def __init__(self):
        super(Welklidwoord, self).__init__()
        uic.loadUi('Gui/lidwoord.ui', self)
        #hidden frame -A
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        #-display country in dropdown1 -A
        self.website = "https://www.welklidwoord.nl/" # webside
        #-----------------------------
        self.search.clicked.connect(self.search_words)
        self.search.setAutoDefault(True)
        self.show()
        self.quit.clicked.connect(self.close)

    def search_words(self):
        woord = self.searchBox.text()
        if woord=="":
            self.dehet.setText("sorry,")
            self.woord.setText(f"{woord} niet gevonden")
        else:
            self.scrape(woord)
        
    def scrape(self,woord):
        url = self.website + woord       #de url van de woord die je heb gezocht
        get_url = requests.get(url)   #VStuur een get-verzoek naar de url en geef de waarde aan get_url
        get_text = get_url.text # de waarde van get_url.text geef aan get_text
        soup = BeautifulSoup(get_text, "html.parser")
        lidwoord = soup.find('span').text #Gebruik de soepmodule om de waarde van span te vinden en geef deze waarde aan lidwoord
        if lidwoord.lower() == "de of het": #Als lidwoord in kleine letters gelijk is aan 'de of het',drukt het volgende
            self.dehet.setText("sorry,")
            self.woord.setText(f"{woord} niet gevonden")

        else: #Anders drukt het volgende
            self.dehet.setText(lidwoord)
            # woord=woord.title()
            self.woord.setText(woord)
    #windows moving without frame---A
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.ismoving = True
            self.start_point = e.globalPos()
            self.window_point = self.frameGeometry().topLeft()
    def mouseMoveEvent(self, e):
        if self.ismoving:
            relpos = e.globalPos() - self.start_point
            self.move(self.window_point + relpos) 
    def mouseReleaseEvent(self, e):
        self.ismoving = False


if __name__ == "__main__":
    app =  QtWidgets.QApplication(sys.argv)
    window = Welklidwoord()
    app.exec_()
