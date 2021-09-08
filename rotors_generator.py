import random

alphabet = "abcdefghijklmnopqrstuvwxyz"

rotors = [ list(alphabet) for _ in range (5) ]

for i in rotors :
    random.shuffle(i)

with open( "rotors.txt" , "w" , encoding= "ascii") as f :
    for i in rotors :
        f.write ( "".join(i) + '\n' )