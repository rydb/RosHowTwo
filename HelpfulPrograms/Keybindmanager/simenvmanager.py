#This is the script im using for managing launching all the nodes!
#Having 3 different terminals open at once to launch nodes is annoying
#and the lack of standardized ros2 keybinds is doublely so!

#So I made my own!

#This script requires sudo to run due to needing access to to keyboard inputs 
#outside the terminal for workflow keybinds!

#Put this in the root of your ROS2 project in order to use it

#Due to using linux commands, this is linux exclusive

#Keybinds:
    #e + 1 = reload urdfpublisher + rviz2
    
import keyboard  # using module keyboard
from multiprocessing import Process, Queue
import multiprocessing
import time
from os import environ
import os
import sys
from subprocess import Popen, PIPE
import subprocess
from pipes import quote
from pprint import pprint
import signal

#TODO
    #1. Ensure that this script is not vunerable to shell injections due to its use of "shell=True"

    #2. Document what the sourcing script below does 

#No clue how this works, got it from https://stackoverflow.com/questions/7040592/calling-the-source-command-from-subprocess-popen.
#It sources the os.system commands so the ROS2 commands properly work so IDC!
if "--child" in sys.argv: # executed in the child environment
    pprint(dict(os.environ))
else:
    python, script = quote(sys.executable), quote(sys.argv[0])
    os.execl("/bin/bash", "/bin/bash", "-c",
        "source install/setup.bash; %s %s --child" % (python, script))

#Entry point
if __name__ == '__main__':
    
    #change executed command here to suit your needs
    rvizExecute = "ros2 run rviz2 rviz2 -d rviz/NewUrdf.rviz"
    urdfExecute = 'ros2 launch urdfpublisher launch.py'
    
    #Initializes Rviz2 and urdf2 nodes in subprocesses
    proRviz2 = subprocess.Popen(rvizExecute, stdout=subprocess.PIPE, 
                       shell=True, preexec_fn=os.setsid) 
    proUrdf = subprocess.Popen(urdfExecute, stdout=subprocess.PIPE, 
                       shell=True, preexec_fn=os.setsid) 

    #Manages keybinds of running nodes
    while(True):
        #kills urdf publisher then rviz2, then starts them both. They do not update during runtime so inorder to get the
        #vscode urdf model dynamic update look they need to both be restarted
        if keyboard.is_pressed('ctrl + e + 1'):
            print("restarting urdfpublisher")
            os.killpg(os.getpgid(proUrdf.pid), signal.SIGTERM)
            time.sleep(1)
            proUrdf = subprocess.Popen(urdfExecute, stdout=subprocess.PIPE, 
                shell=True, preexec_fn=os.setsid)
            
            print("restarting rviz2")
            os.killpg(os.getpgid(proRviz2.pid), signal.SIGTERM)
            time.sleep(1)
            proRviz2 = subprocess.Popen(rvizExecute, stdout=subprocess.PIPE, 
                    shell=True, preexec_fn=os.setsid)
            time.sleep(2)

