import re
import sys
import serial
import argparse
from time import sleep
    
noteno = 0
songno = 0

parser = argparse.ArgumentParser(description="Read music data (note_number note_dureation) from stdin and play on roomba at specified port.")
parser.add_argument('-p', '--port', default='/dev/ttyUSB0', help='Serial port (default: /dev/ttyUSB0)')
parser.add_argument('-b', '--baud', default='115200', help='Serial speed (default: 115200')
args = parser.parse_args()

ser = serial.Serial(args.port, args.baud)

out = []

print("Enter notes in format 'note_number note_dureation'. Send an empty line to finish data.")
for line in sys.stdin:
    line = line.strip()

    # Ignore all empty lines at the start
    if not len(out) > 1 and not line:
        #print("No data entered.")
        continue

    # If an empty line is found after a line with data, stop reading
    if line == "":
        break
    
    lnotes = re.split(r'\s+', line)
    if not lnotes or len(lnotes) < 2:
        #print("Invalid input: " + line)
        continue
    nlen = int(lnotes[0])
    nnote = int(lnotes[1])
    out.append([nnote,nlen])


data = (128,131)
ser.write(data)
print(data)

while(noteno < len(out)):
    notelen = len(out) - noteno
    if notelen > 0:
        if notelen >= 16:
            notelen = 16
        data = (140,songno,notelen)
        ser.write(data)
        print(data)
        clnote = 0
        sleeptime = 0.1
        while clnote < notelen:
            n = out[noteno + clnote]
            data = (n[0], n[1])
            sleeptime += (1/64*n[1])
            print(data)
            ser.write(data)
            clnote = clnote + 1
        noteno = noteno + notelen
        sleep(0.1)
        data = (141,songno)
        print(data)
        ser.write(data)
        songno = songno + 1
        if songno > 3:
            songno = 0

        sleep(sleeptime)
