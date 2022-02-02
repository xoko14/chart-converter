import sys

def stype(type):
    return type[0]+type[1]

def main():
    file1 = open(sys.argv[1], 'r', encoding='utf-8')
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
                chart+="!Lane\n"
                
            elif "[NOTES]" in line:
                current = "notes"
                chart+="!Note\n"
                
            elif "[FLICK]" in line:
                current = "flick"
                chart+="!Flick\n"
                
            elif "[BELL]" in line:
                current = "bell"
                chart+="!Bell\n"
                
            elif "[BULLET]" in line:
                current = "bullet"
                chart+="!Bullet\n"
                
            else:
                lline = line.split()
                
                # Lane section conversion
                if current == "lane":
                    if stype(lline[0]) == "WL":
                        chart+=f"WL {lline[2]} {lline[3]} {lline[4]}\n"
                    elif stype(lline[0]) == "WR":
                        chart+=f"WR {lline[2]} {lline[3]} {lline[4]}\n"
                    
                    elif stype(lline[0]) == "LL":
                        chart+=f"LL {lline[2]} {lline[3]} {lline[4]}\n"
                    elif stype(lline[0]) == "LC":
                        chart+=f"LC {lline[2]} {lline[3]} {lline[4]}\n"
                    elif stype(lline[0]) == "LR":
                        chart+=f"LR {lline[2]} {lline[3]} {lline[4]}\n"
                
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
                    if lline[0] == "CFK":
                        chart+=f"CF {lline[1]} {lline[2]} {lline[3]} {lline[4]}\n"
                        
                #Bell section conversion
                elif current == "bell":
                    if lline[0] == "BEL":
                        chart+=f"BE {lline[1]} {lline[2]} {lline[3]}\n"
                        
                #Bullet section conversion
                elif current == "bullet":
                    if lline[0] == "BLT":
                        chart+=f"BU {lline[2]} {lline[3]} {lline[4]}\n"
                    
    print("\n"+chart)
                
    
if __name__ == "__main__":
    main()