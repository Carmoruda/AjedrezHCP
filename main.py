import os
import re
import sys
import serial
import chess
import stockfish
import datetime
import requests

nombreBlancas = ""
nombreNegras = ""
board = chess.Board()
TOKEN = "TU_TOKEN"
chat_id = "TU_CHAT_ID"

def MandarMensaje(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={mensaje}"
    requests.get(url).json()

def PiezaCasilla(casilla):
    pieza = board.piece_at(chess.parse_square(casilla))

    if (str(pieza).upper() == "P"):
        return "el peón"
    elif (str(pieza).upper() == "R"):
        return "la torre"
    elif (str(pieza).upper() == "N"):
        return "el caballo"
    elif (str(pieza).upper() == "B"):
        return "el alfil"
    elif (str(pieza).upper() == "Q"):
        return "la dama"
    elif (str(pieza).upper() == "K"):
        return "el rey"

def InputBotones():

    movimientoLegal = False

    botonNumero = ""
    botonLetra = ""

    while movimientoLegal == False:
        contador = 0

        for contador in range(2):
            if contador == 0:
                print("\n\t Introduzca la letra de la casilla de la pieza.")
                botonLetra = RecogerInputBoton().split("/")[0]
                print("\t * Letra:" + botonLetra + "\n")
            else:
                print("\t Introduzca el numero de la casilla de la pieza.")
                botonNumero = RecogerInputBoton().split("/")[1]
                botonNumero = int(botonNumero)
                print("\t * Número:" + str(botonNumero) + "\n")
            contador += 1

        posActual = (botonLetra + str(botonNumero)).lower()
        pieza = PiezaCasilla(posActual)


        contador = 0

        for contador in range(2):
            if contador == 0:
                print("\t Introduzca la letra de la casilla a la que quiere mover.")
                botonLetra = RecogerInputBoton().split("/")[0]
                print("\t * Letra:" + botonLetra + "\n")
            else:
                print("\t Introduzca el número de la casilla a la que quiere mover.")
                botonNumero = RecogerInputBoton().split("/")[1]
                botonNumero = int(botonNumero)
                print("\t * Número:" + str(botonNumero) + "\n")
            contador += 1

        posMover = (botonLetra + str(botonNumero)).lower()

        movimientoLegal = chess.Move.from_uci(posActual + posMover) in board.legal_moves

        if movimientoLegal:
            board.push_san(posActual + posMover)

            if board.turn == False:
                mensaje = "\tBlancas (" + nombreBlancas + ") ha movido " + pieza + " de " + posActual + " a " + posMover + "."
                MandarMensaje(mensaje)
            else:
                mensaje = "\tNegras (" + nombreNegras + ") ha movido " + pieza + " de " + posActual + " a " + posMover + "."
                MandarMensaje(mensaje)

            return mensaje
        else:
            print("\n\t   Error! El movimiento realizado no es legal.\n\n")

def RecogerInputBoton():
    for i in range(50):
        line = ser.readline()  # read a byte
        if line:
            string = line.decode()  # convert the byte string to a unicode string
            # num = int(string) # convert the unicode string to an int
            return string


def NuevaPartida():
    global nombreBlancas
    global nombreNegras
    global ser

    ser = serial.Serial('COM8', 9800, timeout=1)

    clear()
    print(("-" * 30) + " NUEVA PARTIDA " + ("-" * 30))
    nombreBlancas = input("\n\t* Nombre jugador blancas: ")
    nombreNegras = input("\n\t* Nombre jugador negras: ")

    input("\n\t Pulse enter para continuar.")

    MandarMensaje("Nueva partida creada:\n\t * Jugador blancas: " + nombreBlancas + "\n\t * Jugador negras: " + nombreNegras)
    stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    Partida()

def NuevaPartidaBot():
    global nombreBlancas
    global nombreNegras
    global ser

    ser = serial.Serial('COM8', 9800, timeout=1)

    clear()
    print(("-" * 30) + " NUEVA PARTIDA " + ("-" * 30))

    print("   Seleccione una de las siguientes opciones:\n\t1   Jugar con blancas.\n\t2   Jugar con negras.\n")
    accionMenu = input("\n  Introduzca su elección:\n  ===> ")

    clear()
    print(("-" * 30) + " NUEVA PARTIDA " + ("-" * 30))

    if (accionMenu == "1"):
        nombreBlancas = input("\n\t * Nombre jugador blancas: ")
        nombreNegras = "Stockfish"
        print("\n\t * Nombre jugador negras: Stockfish")
        input("\n\tPulse enter para continuar.")

        stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

        MandarMensaje("Nueva partida creada:\n\t * Jugador blancas: " + nombreBlancas + "\n\t * Jugador negras: " + nombreNegras)

        clear()
        PartidaBotBlancas()


    elif (accionMenu == "2"):
        nombreBlancas = "Stockfish"
        print("\n\t * Nombre jugador blancas: Stockfish")
        nombreNegras = input("\n\t * Nombre jugador negras: ")

        input("\n\tPulse enter para continuar.")

        stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

        MandarMensaje("Nueva partida creada:\n\t * Jugador blancas: " + nombreBlancas + "\n\t * Jugador negras: " + nombreNegras)

        clear()
        PartidaBotNegras()

def ComprobarFin():
    if board.is_checkmate():
        if board.turn:
            print("\nPartida finalizada! Jaque mate de las negras.\n")
            MandarMensaje("Partida finalizada! Jaque mate de las negras.")
        else:
            print("\nPartida finalilzada! Jaque mate de las blancas.\n")
            MandarMensaje("Partida finalizada! Jaque mate de las blancas.")
    elif board.is_stalemate():
        if board.turn:
            print("\nPartida finalizada! Rey ahogado por parte de las negras.\n")
            MandarMensaje("Partida finalizada!  Rey ahogado por parte de las negras.")
        else:
            print("\nPartida finalilzada! Rey ahogado por parte de las blancas.\n")
            MandarMensaje("Partida finalizada!  Rey ahogado por parte de las blancas.")

def PartidaBotBlancas():

    contador = 0
    jugadas = []
    while (board.is_checkmate() == False and board.is_stalemate() == False):

        turno = ("-" * 30) + " TURNO DE "
        if (contador % 2 == 0):
            turno += nombreBlancas.upper() + " "
        else:
            turno += nombreNegras.upper() + " "

        clear()
        print(turno + ("-" * 30) + "\n")

        if (contador % 2 == 0):
            jugada = InputBotones()
            print(jugada + "\n")
            jugada = jugada.split()
            jugadas.append(jugada[7] + jugada[9].replace(".", ""))
            pieza = PiezaCasilla(jugada[9].replace(".", ""))

        else:
            stockfish.set_position(jugadas)
            siguiente = stockfish.get_best_move()
            jugadas.append(siguiente)

            board.push_san(siguiente)
            siguiente = re.findall('..?', siguiente)

            pieza = PiezaCasilla(siguiente[1])

            if board.turn == False:
                mensaje = "Blancas (" + nombreBlancas + ") ha movido " + pieza + " de " + siguiente[0] + " a " + siguiente[1] + "."
                MandarMensaje(mensaje)
            else:
                mensaje = "Negras (" + nombreNegras + ") ha movido " + pieza + " de " + siguiente[0] + " a " + siguiente[1] + "."
                MandarMensaje(mensaje)

            print("\t" + mensaje + "\n\n")

        stockfish.set_position(jugadas)
        print(stockfish.get_board_visual())

        contador += 1

        ComprobarFin()

        input("\t Pulse enter para continuar.")

def PartidaBotNegras():

    contador = 0
    jugadas = []
    while (board.is_checkmate() == False and board.is_stalemate() == False):

        turno = ("-" * 30) + " TURNO DE "
        if (contador % 2 == 0):
            turno += nombreBlancas.upper() + " "
        else:
            turno += nombreNegras.upper() + " "

        clear()
        print(turno + ("-" * 30) + "\n")

        if (contador % 2 == 0):
            stockfish.set_position(jugadas)
            siguiente = stockfish.get_best_move()
            jugadas.append(siguiente)

            board.push_san(siguiente)
            siguiente = re.findall('..?', siguiente)

            pieza = PiezaCasilla(siguiente[1])

            if board.turn == False:
                mensaje = "Blancas (" + nombreBlancas + ") ha movido " + pieza + " de " + siguiente[0] + " a " + siguiente[1] + "."
                MandarMensaje(mensaje)
            else:
                mensaje = "Negras (" + nombreNegras + ") ha movido " + pieza + " de " + siguiente[0] + " a " + siguiente[1] + "."
                MandarMensaje(mensaje)

            print("\t" + mensaje + "\n\n")
        else:
            jugada = InputBotones()
            print(jugada + "\n")
            jugada = jugada.split(" ")
            pieza = PiezaCasilla(jugada[9].replace(".", ""))
            jugadas.append(jugada[7] + jugada[9].replace(".", ""))

        stockfish.set_position(jugadas)
        print(stockfish.get_board_visual())

        contador += 1

        ComprobarFin()

        input("s\t Pulse enter para continuar.")

def Partida():
    contador = 0

    while (board.is_checkmate() == False and board.is_stalemate() == False):

        turno = ("-" * 30) + " TURNO DE "
        if (contador % 2 == 0):
            turno += nombreBlancas.upper() + " "
        else:
            turno += nombreNegras.upper() + " "

        clear()
        print(turno + ("-" * 30) + "\n")

        print(InputBotones() + "\n")

        print(board)

        ComprobarFin()

        input("\n\tPulse enter para continuar.")
        contador += 1



def NuevaSesion():
    clear()
    ahora = datetime.datetime.now()

    bienvenidaJuego = ("-" * 50) + " AJEDREZ " + ("-" * 50) + "\n\n"
    bienvenidaJuego += "\t * Día: " + ahora.strftime("%d/%m/%Y") + "\n"
    bienvenidaJuego += "\t * Hora: " + ahora.strftime("%H:%M") + "\n"
    print(bienvenidaJuego)


def Menu():
    accionMenu = ''

    while True:
        NuevaSesion()

        print("   Seleccione una de las siguientes opciones:\n\t1   Nueva partida 1vs1.\n\t2   Nueva partida 1vsbot.\n\t3   Salir")
        accionMenu = input("\n  Introduzca su elección:\n  ===> ")

        if (accionMenu == "1"):
            NuevaPartida()
        elif (accionMenu == "2"):
            NuevaPartidaBot()
        elif (accionMenu == "3"):
            sys.exit()
        else:
            accionMenu = "\n  Error! Los valores introducidos deben ser 1 o 2.\n"

clear = lambda: os.system('cls')

if __name__ == "__main__":
    stockfish = stockfish.Stockfish(path="stockfish.exe")
    Menu()



"""
ser = serial.Serial('COM8', 9800, timeout=1)
time.sleep(2)

for i in range(50):
    line = ser.readline()   # read a byte
    if line:
        string = line.decode()  # convert the byte string to a unicode string
        #num = int(string) # convert the unicode string to an int
        print(string)

ser.close()
"""