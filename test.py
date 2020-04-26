import stewart
import threading
import time

# Create the environment object
env = stewart.environment()

def code():
    ''' Your main code here
    ''' 
    # This function send the angles to servo motors
    angles = [90,90,90,90,90,90]
    env.step(angles, 0.1, 100)

# Create the threading for main code running
code_thread = threading.Thread(name = 'Code', target = code)
code_thread.setDaemon(True)
code_thread.start()
# Call for show plot on environment, it has to be at the end of the code
env.showPlot()
