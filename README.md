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



# System Sequence Diagram Description
```mermaid
sequenceDiagram
    participant User
    participant Speech_Recognition_Node as Speech Recognition Node
    participant Camera
    participant Face_Recognition_Service as Face Recognition Service
    participant TTS_Service as TTS Service

    User->>Speech_Recognition_Node: Voice input
    alt command is "unlock"
        Speech_Recognition_Node->>Camera: Record 2s video
        Camera->>Face_Recognition_Service: Send 5 frames
        alt recognition fails
            Face_Recognition_Service->>TTS_Service: Announce failure
        else recognition succeeds
            Face_Recognition_Service->>TTS_Service: Welcome user
        end
    else command is "start recording"
        Speech_Recognition_Node->>TTS_Service: Ask for user's name
        User->>Speech_Recognition_Node: Respond with name
        Speech_Recognition_Node->>Camera: Record 2s video
        Camera->>Face_Recognition_Service: Send 5 frames for enrollment
        Face_Recognition_Service->>TTS_Service: Announce outcome
    end

