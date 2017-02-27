import string

# LEER ESTO
#
# manual:
# http://users.telenet.be/d.rijmenants/Enigma%20Sim%20Manual.pdf
# sobre todo el apartado 3. Technical details of the Enigma Machine
# y The Rotor Stepping Mechanism
#
# simulador:
# https://people.physik.hu-berlin.de/~palloks/js/enigma/enigma-u_v20_en.html
#


class Rotor:
    def __init__(self, name, start, rotoratright=None):
        if name == 1: # Rotor tipo I
            self.type = name
            self.d_wiring = dict(zip(string.ascii_lowercase, "ekmflgdqvzntowyhxuspaibrcj")) # mapeado de las conexiones internas
            self.r_wiring = dict(zip("ekmflgdqvzntowyhxuspaibrcj", string.ascii_lowercase)) # mapeado inverso
            self.position = start
            self.turnover = "q" # from q to r
            self.rotated = False
            self.rightrotor = rotoratright # el rotor que tiene a su derecha, si no tiene None
        elif name == 2: # Rotor tipo II
            self.type = name
            self.d_wiring = dict(zip(string.ascii_lowercase, "ajdksiruxblhwtmcqgznpyfvoe"))
            self.r_wiring = dict(zip("ajdksiruxblhwtmcqgznpyfvoe", string.ascii_lowercase))
            self.position = start
            self.turnover = "e" # from e to f
            self.rotated = False
            self.rightrotor = rotoratright
        elif name == 3: # Rotor tipo III
            self.type = name
            self.d_wiring = dict(zip(string.ascii_lowercase, "bdfhjlcprtxvznyeiwgakmusqo"))
            self.r_wiring = dict(zip("bdfhjlcprtxvznyeiwgakmusqo", string.ascii_lowercase))
            self.position = start
            self.turnover = "v" # from v to w
            self.rotated = False
            self.rightrotor = rotoratright            

    def __str__(self):
        return "Rotor type {}, pos = {}".format(self.type, self.position)
            

    def rotate(self):
        if(self.rightrotor != None and self.position == self.turnover): #!!
            #print("wooo, giro doble")
            #print("rotor {} rotated from {} to ".format(self.type, self.position), end="")
            self.position = chr((ord(self.position)-ord("a")+1)%len(string.ascii_lowercase) + ord("a"))
            self.rotated = True
            #print(self.position)
            return
        else:
            self.rotated = False
            
        if(self.rightrotor == None):
            # si a su derecha no hay ningun rotor, va a girar cada vez que se cifre una letra
            #print("rotor {} rotated from {} to ".format(self.type, self.position), end="")
            self.position = chr((ord(self.position)-ord("a")+1)%len(string.ascii_lowercase) + ord("a"))
            self.rotated = True
            #print(self.position)
        elif(self.rightrotor.position == chr(ord(self.rightrotor.turnover)+1) and self.rightrotor.rotated):
            # si a su derecha hay un rotor, este rotor va a girar cuando el rotor de la derecha
            # haga una vuelta (cuando su posicion sea igual a su valor de 'turnover'
            #print("rotor {} rotated from {} to ".format(self.type, self.position), end="")
            self.position = chr((ord(self.position)-ord("a")+1)%len(string.ascii_lowercase) + ord("a"))
            self.rotated = True
            #print(self.position)
        else:
            self.rotated = False
            

    def d_encrypt(self, char): # cifrado directo, derecha a izquierda (antes de pasar por el espejo)
        self.rotate()
        char = chr((ord(char)-ord("a")+ord(self.position)-ord("a"))%len(string.ascii_lowercase) + ord("a"))
        char = self.d_wiring.get(char)
        char = chr((ord(char)-ord("a")-ord(self.position)+ord("a"))%len(string.ascii_lowercase) + ord("a"))
        return char

    def r_encrypt(self, char): # cifrado inverso, para cuando ya se ha pasado por el espejo
        char = chr((ord(char)-ord("a")+ord(self.position)-ord("a"))%len(string.ascii_lowercase) + ord("a"))
        char = self.r_wiring.get(char)
        char = chr((ord(char)-ord("a")-ord(self.position)+ord("a"))%len(string.ascii_lowercase) + ord("a"))
        return char        


class Enigma:
# Este Enigma NO TIENE el 'plugboard', tambien habria que añadirlo
# tambien habrira que añadir metodos para resetear la máquina, o ponerlo
# en la configuracion que quieras...
    def __init__(self):
        self.r1 = Rotor(1, "a", None)
        self.r2 = Rotor(2, "a", self.r1)
        self.r3 = Rotor(3, "a", self.r2)
        self.reflector = dict(zip(string.ascii_lowercase, "yruhqsldpxngokmiebfzcwvjat"))
    def encrypt(self, s):
        # en vez de hacer un print, habria que guardarlo en un string y al final return...
        for c in s:
            if c not in string.ascii_lowercase:
                print(c, end="")
                continue
            c = self.r1.d_encrypt(c)
            c = self.r2.d_encrypt(c)
            c = self.r3.d_encrypt(c)

            c = self.reflector.get(c)

            c = self.r3.r_encrypt(c)
            c = self.r2.r_encrypt(c)
            c = self.r1.r_encrypt(c)

            print(c, end="")
            #print("{}[{}{}{}]".format(c, self.r3.position, self.r2.position, self.r1.position), end="")
        print("")
        
# uso
e = Enigma()
e.encrypt("aaaaa aaaaa aaaaa aaaaa")

