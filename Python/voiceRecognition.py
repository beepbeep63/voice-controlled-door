#import the peech rocognizer library
import speech_recognition as sr

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
        if "open" in command["text"].lower():
            print("Opening door...")
            #insert motor code here using pyfirmata
        elif "close" in command["text"].lower():
            print("Closing door...")
            #insert motor code here
        elif "exit" in command["text"].lower():
            print("Exiting program... Say hi to Rabab for me.")
            break