from PyQt5.QtWidgets import QWidget, QPushButton, QApplication,QTextEdit
from PyQt5.QtWidgets import QSlider, QLabel, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt
from os import path
from pathlib import Path
from urllib.parse import unquote
import sys
import vlc
import time

class Window(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
                
##### --------------------------------------------------------------------------------
#
#    Control Buttons
#
##### --------------------------------------------------------------------------------
        
        playbutton = QPushButton(self)
        playpixmap = QPixmap('play.png')
        playicon = QIcon(playpixmap)
        playbutton.setIcon(playicon)
        playbutton.setFixedSize(30,30)
        playbutton.move(40,10)
        playbutton.clicked.connect(self.playTrack)               

        pausebutton = QPushButton(self)
        pausepixmap = QPixmap('pause.png')
        pauseicon = QIcon(pausepixmap)
        pausebutton.setIcon(pauseicon)
        pausebutton.setFixedSize(30,30)
        pausebutton.move(75,10)
        pausebutton.clicked.connect(self.pauseTrack)

        stopbutton = QPushButton(self)
        stoppixmap = QPixmap('stop.png')
        stopicon = QIcon(stoppixmap)
        stopbutton.setIcon(stopicon)
        stopbutton.setFixedSize(30,30)
        stopbutton.move(110,10)
        stopbutton.clicked.connect(self.stopTrack)

        nextbutton = QPushButton(self)
        nextpixmap = QPixmap('nextTrack.png')
        nexticon = QIcon(nextpixmap)
        nextbutton.setIcon(nexticon)
        nextbutton.setFixedSize(30,30)
        nextbutton.move(75,50)
        nextbutton.clicked.connect(self.nextTrack)

        lastbutton = QPushButton(self)
        lastpixmap = QPixmap('lastTrack.png')
        lasticon = QIcon(lastpixmap)
        lastbutton.setIcon(lasticon)
        lastbutton.setFixedSize(30,30)
        lastbutton.move(40,50)
        lastbutton.clicked.connect(self.lastTrack)
                        
        filebutton = QPushButton('File',self)
        filebutton.clicked.connect(self.pickFile)
        filebutton.move(150,15)
                    
##### --------------------------------------------------------------------------------
#
#    Volume Slider
#
##### --------------------------------------------------------------------------------
         
        volumeslider = QSlider(Qt.Vertical,self)
        volumeslider.setFocusPolicy(Qt.NoFocus)
        volumeslider.setGeometry(15,10,10,100)
        volumeslider.setTickInterval(10)
        volumeslider.setValue(70)
        volumeslider.setTickPosition(3)
        volumeslider.valueChanged[int].connect(self.changeVolume)
        volumelabel = QLabel(self)
        volumelabel.setText('Vol')
        volumelabel.move(10,120)
                            
##### --------------------------------------------------------------------------------
#
#    Track Label
#
##### --------------------------------------------------------------------------------
         
        self.tracklabel = QLabel(self)
        self.tracklabel.setText(self.filename)
        self.tracklabel.move(40,210)
        
        self.playlistBox = QTextEdit(self)
        self.playlistBox.setGeometry(40,90,185,100)       
                    
##### --------------------------------------------------------------------------------
#
#   Main Window
#
##### --------------------------------------------------------------------------------
       
        self.setGeometry(300,300,240,250)
        self.setWindowIcon(QIcon('ninja.png'))
        self.setWindowTitle('Ninja MP3')
        self.show()
        
##### --------------------------------------------------------------------------------
#
#    Button Logic
#
##### --------------------------------------------------------------------------------      
    
    def playTrack(self):
        if self.playlist == []:
            return
        self.track.play() 
        newTrack = unquote(self.track.get_media_player().get_media().get_mrl())                      
        newLabel = Path(newTrack).name 
        self.tracklabel.setText(newLabel)
        self.tracklabel.adjustSize()
        self.rewind = False
       
    def pauseTrack(self):
        self.track.pause()
        
    def stopTrack(self):
        self.track.stop()
        
    def nextTrack(self):
        if self.playlist == []:
            return

        self.track.next()
        newTrack = unquote(self.track.get_media_player().get_media().get_mrl())           
        newLabel = Path(newTrack).name
        self.tracklabel.setText(newLabel)
        self.tracklabel.adjustSize()
        self.rewind = False 

    def lastTrack(self):
        if self.playlist == []:
            return
        
        if self.rewind == False:
            self.track.previous()
            self.track.pause()            
            time.sleep(0.3)
            self.track.next()
            self.track.play()
            newTrack = unquote(self.track.get_media_player().get_media().get_mrl())          
            newLabel = Path(newTrack).name
            self.tracklabel.setText(newLabel)
            self.tracklabel.adjustSize()                    
            self.rewind = True

        else:
            self.track.previous()
            newTrack = unquote(self.track.get_media_player().get_media().get_mrl())           
            newLabel = Path(newTrack).name
            self.tracklabel.setText(newLabel)
            self.tracklabel.adjustSize()                       
            self.rewind = False

##### --------------------------------------------------------------------------------
#
#    File Actions
#
##### --------------------------------------------------------------------------------
         
    def pickFile(self):
        
        picked, filters = QFileDialog.getOpenFileName(self, 'Open File', filter='mp3(*.mp3)')
        for i in range(len(self.playlist)):
            if picked == self.playlist[i]:
                errorDialog = QMessageBox()
                errorDialog.setIcon(QMessageBox.Critical)
                errorDialog.setText('Please pick a unique track.')
                errorDialog.setWindowTitle('Error')
                errorDialog.exec_()
                return
        
        if path.isfile(picked):

            self.playlist.append(picked)
            self.track_list = self.instance.media_list_new(self.playlist)
            self.track.set_media_list(self.track_list) 
            self.populatePlaylist()
        
        filters = filters 
        
    def populatePlaylist(self):
        self.playlistBox.clear()
        for i in range(len(self.playlist)) :
            trackName = Path(self.playlist[i]).name
            self.playlistBox.setCurrentFont(QFont('Arial',8))
            self.playlistBox.insertPlainText(trackName+'\n')                           
  
    def changeVolume(self,value):
        if self.playlist == []:
            return
        
        mp = self.track.get_media_player()
        mp.audio_set_volume(value)
        
class AudioPlayer(Window):
                            
##### --------------------------------------------------------------------------------
#
#    General setup 
#
##### --------------------------------------------------------------------------------
         
    instance = vlc.Instance()
    track = instance.media_list_player_new()
    track.set_playback_mode(vlc.PlaybackMode.loop)
    playlist = []
    filename = ''
    track_list = instance.media_list_new(playlist)
    track.set_media_list(track_list)
    rewind = False
    
    def __init__(self):
        super().__init__()

def main():
    app = QApplication(sys.argv)
    ap = AudioPlayer()
    ap = ap
    sys.exit(app.exec_())   
    
if __name__ == '__main__':
    main()           