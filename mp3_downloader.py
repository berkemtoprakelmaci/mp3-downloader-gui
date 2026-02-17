# Copyright (C) 2026 Berkem Toprak Elmacı
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.

import yt_dlp
import os
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PySide6.QtCore import QThread, Signal

# relative path finder in exe
def resource_path(relative_path):
    """ PyInstaller ile oluşturulan exe için dosya yolunu bulur """
    try:
        # PyInstaller temp generator, path is in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class DownloadWorker(QThread):
    finished = Signal(str)

    def __init__(self, url, is_playlist):
        super().__init__()
        self.url = url
        self.is_playlist = is_playlist

    def run(self):
        indirilecek_konum = os.path.join(os.path.expanduser("~"), "Downloads")
        
        # dynamic FFmpeg path
        ffmpeg_yolu = resource_path("ffmpeg.exe") 
        
        ayarlar = {
            'noplaylist': not self.is_playlist,
            'format': 'bestaudio/best',
            'outtmpl': f'{indirilecek_konum}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'ffmpeg_location': os.path.dirname(ffmpeg_yolu), 
        }

        try:
            with yt_dlp.YoutubeDL(ayarlar) as ydl:
                ydl.download([self.url])
            self.finished.emit("✅ İndirme Tamamlandı!")
        except Exception as e:
            self.finished.emit(f"❌ Hata: {str(e)}")

class Pencere(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("mp3 download")
        self.resize(400, 150)

        layout = QVBoxLayout()

        self.etiket = QLabel("URL")
        layout.addWidget(self.etiket)

        self.input_kutusu = QLineEdit()
        self.input_kutusu.setPlaceholderText("")
        layout.addWidget(self.input_kutusu)

        self.buton_tek = QPushButton("Download")
        self.buton_liste = QPushButton("List Download")
        self.buton_tek.clicked.connect(lambda: self.baslat_indir(False))
        self.buton_liste.clicked.connect(lambda: self.baslat_indir(True))
        layout.addWidget(self.buton_tek)
        layout.addWidget(self.buton_liste)

        self.setLayout(layout)

    def baslat_indir(self, is_playlist):
        url = self.input_kutusu.text()
        if not url:
            self.etiket.setText("")
            return

        self.etiket.setText("İndiriliyor...")
        self.buton_tek.setEnabled(False) 
        self.buton_liste.setEnabled(False)

        self.worker = DownloadWorker(url, is_playlist)
        self.worker.finished.connect(self.indirme_bitti)
        self.worker.start()

    def indirme_bitti(self, mesaj):
        self.etiket.setText(mesaj)
        self.buton_tek.setEnabled(True)
        self.buton_liste.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = Pencere()
    pencere.show()
    sys.exit(app.exec())
