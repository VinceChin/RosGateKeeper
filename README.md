# RosGateKeeper
a group project for ros gatekeeper

# Reuquirements
please run the command
pip install requirements.txt

sudo apt-get install mpg123 

and other packages it requires

# How to use
## Unlock
Just say unlock to the robot

## Record Your Face
1. Say “Start recording” to the robot
2. The robot will ask you "What is your name?"
3. Then reply the robot with "My name is XXXX". The sentence must start with "My name is"



## System Sequence Diagram Description

This sequence outlines the interactions within the My_Ros_Gatekeeper system, including speech recognition, video recording, face recognition, and text-to-speech responses.

1. **User Interaction with Speech Recognition Node**:
   - The user provides a voice input.
   - The speech recognition node determines if the keyword is "unlock" or "start recording".

2. **Process for 'Unlock' Command**:
   - If the keyword is "unlock":
     - The camera records a 2-second video and selects 5 random frames.
     - These frames are sent to the face recognition service.
     - The face recognition service processes the images and determines the outcome.
       - If recognition fails, the TTS service announces a failure to unlock.
       - If recognition succeeds, the server returns the user's name, and the TTS service welcomes the user home.

3. **Process for 'Start Recording' Command**:
   - If the keyword is "start recording":
     - The TTS service asks the user for their name.
     - The user responds with their name.
     - The camera then records another 2-second video, selecting 5 frames to send to the face recognition service for enrollment.
     - The TTS service announces the outcome of the face recording process.

This sequence diagram provides a clear overview of how the My_Ros_Gatekeeper system processes voice commands and interacts with the user for face recognition and feedback.

