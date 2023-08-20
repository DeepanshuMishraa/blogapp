import speech_recognition as sr
import requests

# initialize the speech recognizer
r = sr.Recognizer()

# use the default microphone as the audio source
with sr.Microphone() as source:
    # listen for speech input
    print("Speak now...")
    audio = r.listen(source)

    # use Google Speech Recognition to convert speech to text
    try:
        transcript = r.recognize_google(audio)
        print("You said: " + transcript)

        # send the transcript to the server for processing
        url = "http://localhost:5000/voice-control"
        headers = {"Content-Type": "application/json"}
        data = {"transcript": transcript}
        response = requests.post(url, headers=headers, json=data)

        # handle the server response
        if response.status_code == 200:
            response_data = response.json()
            action = response_data["action"]
            if action == "shutdown":
                # shutdown the computer
                shutdown()
            elif action == "volume-up":
                # increase the volume
                volume_up()
            elif action == "volume-down":
                # decrease the volume
                volume_down()
            else:
                print("Unknown action: " + action)
        else:
            print("Error processing voice input")

    except sr.UnknownValueError:
        print("Sorry, I could not understand your speech")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

# function to shutdown the computer
def shutdown():
    # send an HTTP request to the server to shutdown the computer
    url = "http://localhost:5000/shutdown"
    requests.post(url)

# function to increase the volume
def volume_up():
    # send an HTTP request to the server to increase the volume
    url = "http://localhost:5000/volume-up"
    requests.post(url)

# function to decrease the volume
def volume_down():
    # send an HTTP request to the server to decrease the volume
    url = "http://localhost:5000/volume-down"
    requests.post(url)
