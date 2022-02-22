import sys

def stype(type):
    return type[0]+type[1]

def convert(source, target):
    file1 = open(source, 'r', encoding='utf-8')
    lines = file1.readlines()
    current = ""
    chart = ""
    
    for i, line in enumerate(lines):
        sys.stdout.write(f"\rreading line {i+1}")
        sys.stdout.flush()
        
        if(len(line)<2):
            continue
        
        if not line[0]+line[1] == "//":
            
            # Check section
            if "[LANE]" in line:
                current = "lane"
                chart+="\n!Lane\n"
                
            elif "[NOTES]" in line:
                current = "notes"
                chart+="\n!Note\n"
                
            elif "[FLICK]" in line:
                current = "flick"
                chart+="\n!Flick\n"
                
            elif "[BELL]" in line:
                current = "bell"
                chart+="\n!Bell\n"
                
            elif "[BULLET]" in line:
                current = "bullet"
                chart+="\n!Bullet\n"
                
            elif "[COMPOSITION]" in line:
                current = "metrics"
                chart+="\n!Metrics\n"
                chart+=f"BM 0 0 {bpm}\n"
                chart+=f"ME 0 0 {met[0]} {met[1]}\n"
                
            elif "[B_PALETTE]" in line:
                current = "bpattern"
                chart+="\n!Bullet pattern\n"
                
            else:
                lline = line.split()
                
                # Lane section conversion
                if current == "lane":
                    if stype(lline[0]) == "WL":
                        chart+=f"WL {lline[2]} {lline[3]} {lline[4]} {lline[0][2]}\n"
                    elif stype(lline[0]) == "WR":
                        chart+=f"WR {lline[2]} {lline[3]} {lline[4]} {lline[0][2]}\n"
                    
                    elif stype(lline[0]) == "LL":
                        chart+=f"LL {lline[2]} {lline[3]} {lline[4]} {lline[0][2]}\n"
                    elif stype(lline[0]) == "LC":
                        chart+=f"LC {lline[2]} {lline[3]} {lline[4]} {lline[0][2]}\n"
                    elif stype(lline[0]) == "LR":
                        chart+=f"LR {lline[2]} {lline[3]} {lline[4]} {lline[0][2]}\n"
                
                # Note section conversion
                elif current == "notes":
                    if lline[0] == "TAP":
                        chart+=f"NT {lline[2]} {lline[3]} {lline[4]}\n"
                    elif lline[0] == "CTP":
                        chart+=f"CT {lline[2]} {lline[3]} {lline[4]}\n"
                    
                    elif lline[0] == "HLD":
                        chart+=f"NH {lline[2]} {lline[3]} {lline[4]} {lline[6]} {lline[7]} {lline[8]}\n"
                    elif lline[0] == "CHD":
                        chart+=f"CH {lline[2]} {lline[3]} {lline[4]} {lline[6]} {lline[7]} {lline[8]}\n"
                
                # Flick section conversion
                elif current == "flick":
                    if lline[0] == "FLK":
                        chart+=f"NF {lline[1]} {lline[2]} {lline[3]} {lline[4]}\n"
                    elif lline[0] == "CFK":
                        chart+=f"CF {lline[1]} {lline[2]} {lline[3]} {lline[4]}\n"
                        
                #Bell section conversion
                elif current == "bell":
                    if lline[0] == "BEL":
                        chart+=f"BE {lline[1]} {lline[2]} {lline[3]}\n"
                        
                #Bullet section conversion
                elif current == "bullet":
                    if lline[0] == "BLT":
                        chart+=f"BU {lline[2]} {lline[3]} {lline[4]} {lline[1]}\n"
                
                #Metrics section conversion
                elif current == "metrics":
                    if lline[0] == "BPM":
                        chart+=f"BM {lline[1]} {lline[2]} {lline[3]}\n"
                    if lline[0] == "MET":
                        chart+=f"ME {lline[1]} {lline[2]} {lline[3]} {lline[4]}\n"
                
                elif current == "bpattern":
                    if lline[0] == "BPL":
                        chart+=f"BP {lline[1]} {lline[2]} {lline[3]} {lline[4]} {lline[5]}\n"
                
                
                else:
                    if lline[0] == "BPM_DEF":
                        bpm = lline[1]
                    elif lline[0] == "MET_DEF":
                        met = lline[1:3]
                    elif lline[0] == "CREATOR":
                        charter = lline[1]
                    
    f = open(target, "w")
    f.write(chart)
    f.close()
    return charter