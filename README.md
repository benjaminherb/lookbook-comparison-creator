# LOOKBOOK COMPARISON CREATOR
## StuPro Studiotechnik 2022

Python/FFmpeg Tool um aus dem Lookbook Datensatz Vergleichsvideos/übersichten zu erstellen. Es werden jeweils die Einstellungen mit Arbeitsblende ausgegeben (in 1080p/h264).

## Installation

### Benötigte Programme
Für das Tool wird [Python3](https://www.python.org/downloads/) und [FFmpeg](https://ffmpeg.org/download.html) benötigt.

* Windows: Doppelklick / "Öffnen mit -> Python" oder im Terminal "python3.exe LookbookComparisonCreator.py" 
* MacOS: "Öffnen mit -> Python Launcher" oder im Terminal "python3 LookbookComparisonCreator.py"
* Linux:  "Run as Program" oder im Terminal "python LookbookComparisonCreator.py"

## Nutzung
**FFmpeg:** Pfad zur FFmpeg binary. Sofern es bereits im System installiert und zur PATH variablen hinzugefügt (also im Terminal über ffmpeg oder ffmpeg.exe aufrufbar) ist kann auch das verwendet werden.
**Source:** Pfad zu den Source Clips
**Keys:** Auswahl der gewünschten Clips mit durch Kommas separierten Eigenschaften (aus den Dateinnamen der Source Clips)
Entweder/Oder Eigenschaften können durch ein '|' getrennt angegeben werden (zB. Orbiter|Robe) und auszuschließende Eigenschaften durch ein '-' (zB. -Frost)

Beispiele:
* Key,Close,Orbiter -> Alle Nahaufnahmen vom Orbiter
* Key,Wide,Mini Mix|Maxi Mix,1D -> Alle Totalen mit Mini Mix oder Maxi Mix mit Diffusion
* Key,Wide,Robe|Orbiter,°,-Frost -> Alle harten (eg 15°,30°) Aufsätze vom Orbiter/Robe ohne Frost




