#import the speech recognizer and pyfirmata libraries
import pyfirmata as pf
import speech_recognition as sr
import time

def listen(recognizer, microphone):
    #listen to mic
    with microphone as source:
            print("Setting up mic... stay silent for 1 second.")
            recognizer.adjust_for_ambient_noise(source)
            print("Say your command.")
            audio = recognizer.listen(source)
            print("Transcribing...")
    
    #setting up a dict for the information received
    response = {
        "text": None,
        "error": None,
        "success": True
        }

    #check for errors
    try:
        response["text"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Speech unrecognized"
    
    return response

#the main code that will be run
if __name__ == "__main__":

    #setting up the serial connection to the arduino
    board = pf.Arduino('COM3')
    it = pf.util.Iterator(board)
    it.start()

    #setting up the pins
    pin11 = board.get_pin('d:11:o')
    pin13 = board.get_pin('d:13:o')

    #creating a recognizer object
    r = sr.Recognizer()

    #creating a mic object for input
    m = sr.Microphone()

    #run this program forever (will change later)
    while True:
        while True:
            #get info from mic
            command = listen(r, m)
            #if the command has been transcribed, stop listening
            if command["text"]:
                break
            #if the api didn't work, stop listening
            if not command["success"]:
                break
            print("Could you repeat your command, please?")
        
        #check if there were errors
        if command["error"]:
            #print the error message
            print("ERROR: {}".format(command["error"]))

            #if the speech was unrecognized, restart program
            if ("Speech unrecognized" == command["error"]):
                continue
            #If the API isn't working, stop the program
            else:
                break

        #print what was said
        print("You said: {}".format(command["text"]))

        #check what command was said
        if "close" in command["text"].lower():
            print("Closing door...")
            #motor will turn counterclockwise
            pin13.write(1)
            pin11.write(1)
            time.sleep(5)
            pin11.write(0)
            print("Door closed.")
        elif "open" in command["text"].lower():
            print("Open door...")
            #motor will turn clockwise
            pin13.write(0)
            pin11.write(1)
            time.sleep(5)
            pin11.write(0)
        elif "exit" in command["text"].lower():
            print("Exiting program... Say hi to Rabab for me.")
            break