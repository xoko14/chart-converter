import os, sys

from xml.etree import ElementTree as ET

from numpy import number

from convert import convert

import json

import urllib.request as urlr

from xml.dom import minidom

def main():
    opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
    args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]
    
    songs = []

    for rootf, subdirectories, files in os.walk("./source/music"):
        i = 0
        for subdirectory in subdirectories:
            folder = os.path.join(rootf, subdirectory)
            with open(os.path.join(folder, "Music.xml"), encoding="utf-8") as file:
                xml = file.read()
            root = ET.fromstring(xml)

            songname = root.find("Name").findtext("str")
            artistname = root.find("ArtistName").findtext("str")

            if "-t" in opts:
                if songname.lower().find(args[0].lower()) != -1:
                    print(str(i)+") "+root.findtext("dataName"))
                    print("\t"+songname)
                    print("\t"+artistname)
                    songs.append(root.findtext("dataName"))
                    i+=1
            elif "-a" in opts:
                if artistname.lower().find(args[0].lower()) != -1:
                    print(str(i)+") "+root.findtext("dataName"))
                    print("\t"+songname)
                    print("\t"+artistname)
                    songs.append(root.findtext("dataName"))
                    i+=1
                    
    
    if "-o" in opts:
        finished = False
        while not finished:
            selection = input(">")
            try:
                selection = int(selection)
            except:
                print("Please, input a number")
                continue
            
            if selection < len(songs):
                finished = True
            else:
                print("Please input a valid number")
        
        songfolder = songs[selection]
        
        folder = os.path.join("./source/music", songfolder)
        
        charter_e = convert(os.path.join(folder, f"{songfolder[5:]}_00.ogkr"), os.path.join(args[1], f"{songfolder}/song_e.chart"))
        charter_n = convert(os.path.join(folder, f"{songfolder[5:]}_01.ogkr"), os.path.join(args[1], f"{songfolder}/song_n.chart"))
        charter_h = convert(os.path.join(folder, f"{songfolder[5:]}_02.ogkr"), os.path.join(args[1], f"{songfolder}/song_h.chart"))


        with open(os.path.join(folder, "Music.xml"), encoding="utf-8") as file:
            xml = file.read()
        
        sxml = ET.fromstring(xml)
            
        song_name = sxml.find("Name").findtext("str")
        song_artist = sxml.find("ArtistName").findtext("str")
        song_sortname = sxml.findtext("NameForSort")
        
        chartroot = ET.Element("chart")
        
        ET.SubElement(chartroot, "title").text = song_name
        ET.SubElement(chartroot, "artist").text = song_artist
        ET.SubElement(chartroot, "easy", file="song_e.chart", charter=charter_e, difficulty="Easy")
        ET.SubElement(chartroot, "normal", file="song_n.chart", charter=charter_n, difficulty="Normal")
        ET.SubElement(chartroot, "hard", file="song_h.chart", charter=charter_h, difficulty="Hard")
        ET.SubElement(chartroot, "music", file="song.wav")
        ET.SubElement(chartroot, "jacket", file="jacket.png", artist="unknown")
        
        tree = ET.ElementTree(chartroot)
        
        if not os.path.isdir(args[1]): os.mkdir(args[1])
        if not os.path.isdir(os.path.join(args[1], songfolder)): os.mkdir(os.path.join(args[1], songfolder))
        xmlstr = minidom.parseString(ET.tostring(chartroot)).toprettyxml(indent="    ")
        with open(os.path.join(args[1], f"{songfolder}/song.xml"), "w", encoding="utf-8") as f:
            f.write(xmlstr)
        # tree.write(os.path.join(args[1], f"{songfolder}/song.xml"), encoding="utf-8")
        
        os.system(f".\\vgmstream\\test.exe -o {os.path.join(args[1], f'{songfolder}/song.wav')} .\\source\\musicsource\\musicsource{songfolder[5:]}\\music{songfolder[5:]}.awb")
        
        with open("./source/data/music.json", encoding="utf-8") as file:
                songsinfo = json.loads(file.read())

        for songinfo in songsinfo:
            if songinfo["title_sort"] == song_sortname:
                song_image = songinfo["image_url"]
        
        print(song_image)
        # shutil.copyfile(os.path.join("./source/jacket/", song_image), os.path.join(args[1], f'{songfolder}/song.jpg'))
        urlr.urlretrieve("https://ongeki-net.com/ongeki-mobile/img/music/"+song_image, os.path.join(args[1], f'{songfolder}/jacket.png'))
        
        
                
if __name__ == "__main__":
    main()