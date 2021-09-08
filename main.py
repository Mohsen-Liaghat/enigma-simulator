

def dict_join ( d1 : dict , d2: dict  ) -> dict :
    for i in d2 :
        assert i not in d1 , "you cant join the same items"
        d1 [ i ] = d2 [ i ]
    return d1

class Rotor : 
    def __init__(self , string  ) :
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        self.__translator = dict( zip(alphabet , string ) )

    
    def decode ( self , chr ) : 
        for key  in self.__translator :
            if self.__translator[key] == chr :
                return key 
        raise 
    
    def code ( self , chr ) :
        return self.__translator [ chr ]

class Enigma :
    def __init__(self , selected_rotors , chr_order , arg ) :
        self.__alphabet = "abcdefghijklmnopqrstuvwxyz"
        self.rotors_angle = tuple( self.__alphabet.find( i ) for i in chr_order )
        assert all ( i in self.__alphabet for i in chr_order) , "chr_order must be a string from alphabets and len() == 3"
        self.__reflector = Rotor( self.__alphabet [ -1 : -27 : -1 ] )
        self.__counter = 0
        self.__plogboard = dict_join (arg , { arg[i] : i for i in arg})
        with open ( "rotors.txt" , "r" ) as f :
            l = tuple(f.read().split('\n'))
            self.__rotors = tuple ( Rotor(l [ i ]) for i in selected_rotors )
   
    def rotates_rotors (self) :
        self.__counter += 1 

    def __code ( self , word ) :
        res = []
        for i in word :
            if i in self.__plogboard :
                tmp = self.__plogboard[ i ]
            else:
                tmp = i
            tmp = self.__rotors[0].code( tmp ) 
            tmp = self.__alphabet [( self.__alphabet.find( tmp ) + self.rotors_angle[0] + self.__counter ) % 26 ]
            tmp = self.__rotors[1].code(tmp)
            tmp = self.__alphabet [( self.__alphabet.find( tmp ) + self.rotors_angle[1] + self.__counter // 26 ) % 26 ]
            tmp = self.__rotors[2].code(tmp)
            tmp = self.__alphabet [( self.__alphabet.find( tmp ) + self.rotors_angle[2] + self.__counter // (26 * 26) ) % 26 ]
            tmp = self.__reflector.code(tmp)
            #reverce
            tmp = self.__alphabet [ ( self.__alphabet.find( tmp ) - self.rotors_angle[2] - self.__counter // (26 * 26) ) % 26 ]
            tmp = self.__rotors[2].decode( tmp )
            tmp = self.__alphabet [ ( self.__alphabet.find( tmp ) - self.rotors_angle[1] - self.__counter // (26) ) % 26 ]
            tmp = self.__rotors[1].decode( tmp )
            tmp = self.__alphabet [ ( self.__alphabet.find( tmp ) - self.rotors_angle[0] - self.__counter ) % 26 ]
            tmp = self.__rotors[0].decode( tmp )
            self.rotates_rotors()
            if tmp in self.__plogboard : 
                tmp = self.__plogboard [ tmp ]
            res.append(tmp)

        return "".join(res)

    def reload (self) :
        self.__counter = 0
    
    def code ( self , text ) :
        words = text.split() 
        res = ""
        for i in words :
            res += self.__code( i ) + " "
        return res

selected_rotors = tuple( map( int , input("enter the rotors number respectively : " ).split() ))
rotors_angle = input("set the rotors without space : ")[ : 3 ]
plogboard = {}
try :
    t1 , t2 = input("enput a plog into plogboard ( seprate two plog of the wire by space ) : ").split()
    for i in range ( 12 ):
        plogboard [ t1 ] = t2
        t1 , t2 = input("enput a plog into plogboard ( seprate two plog of the wire by space ) : ").split()

except :
    my_machine = Enigma( selected_rotors , rotors_angle , plogboard )
    print( "The enigma machine is ready : ")
    while True :
        text = input().strip().lower()
        if text == "" :
            break
        cipher = my_machine.code(text)
        print(cipher)
        my_machine.reload()
        #print(my_machine.code(cipher))
        print()
        my_machine.reload()