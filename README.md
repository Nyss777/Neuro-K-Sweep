## Neuro-K-Sweep

Simple program to remove old version of songs from the Neuro Karaoke Archive, written in python and packaged with pyinstaller.

### Instructions for use

* The program expects a file name 'config.txt' right alongside the executable. If you place it in the wrong place the program will 
complain about it and tell you the place it expects to find it.

* The first line specifies the path where the songs are and the seconds line specifies the place where outdated songs will be moved to.

* The songs path names are assumed to follow from the Google Drive so they are preserved, for example:

* With the outdated songs folder location being "C://destination/" , the file "DISC 2/008. DECO_27, PinocchioP - God-ish (Neuro.v2).mp3"
would be moved to "C://destination/DISC 2/008. DECO_27, PinocchioP - God-ish (Neuro.v2).mp3" and not "C://destination/008. DECO_27, PinocchioP - God-ish (Neuro.v2).mp3"

* The program may not catch all the repeats on the first try, so it's better to run until no new songs are removed.

* If the program complains about "Failed to load album cover config" you can ignore it, it's not important.

* If when moving a song to the outdated songs folder, the songs is already present there, then the song will be deleted to avoid dupes.
