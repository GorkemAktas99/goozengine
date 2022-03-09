# Gooz Engine for Micropython

This engine was designed by Görkem Aktaş for Gooz Project to run on MicroPython. Designed for Gooz OS, this engine acts as the main layer of the operating system.

## How It Works

MicroPython runs files over main.py. So this engine took the starting point as main.py. If desired, main.py can be changed and GoozEngine and EngineTemplate classes, which are the main parts of the engine, can be used.

## main.py
```python
from engine.gooz_engine import GoozEngine
from wifuxlogger import WifuxLogger as LOG
from etc.config.core import load

def login(username,password):
    usr = input("Username -> ")
    pswd = input("Password -> ")
    if password == pswd and username == usr:
        LOG.info("Welcome {}".format(username))
        return True
    else:
        LOG.error("Access Denied")
        return False
try:
    confs = load()
    loginFlag = login(confs["username"],confs["password"])

except Exception as ex:
    LOG.error("Necessary config variables cannot be taken")
    LOG.error("Probably system doesn't have a username or password value")
    LOG.error(ex)

while loginFlag:
    command = input("-> ")
    GoozEngine.run(command)
```
There are several libraries based on this file and its derivatives. Algorithms have been tried to be implemented with static and dynamic methods in these libraries. A configuration operation is provided at the first boot. The goal here is to allow developers to pre-configure pre-defined configurations to improve the user experience. If desired, the configurations here can be improved and differentiated.
```python
from etc.config.core import load
```
The process here is running the "load" function from the /etc/config/core file. Thus, all configuration definitions in /etc/config/configures.txt are injected into the system at system startup.
```python
from engine.gooz_engine import GoozEngine
from wifuxlogger import WifuxLogger as LOG
```
The steps here allow the motor to be called statically. Thus, there is no need to create an engine object. The LOG library used in the writing of the Wifux project is used here as well.
## Gooz Engine
Gooz Engine, which is built on EngineTemplate, allows the writing of different engines thanks to this template.
```python
from engine.engine_template import EngineTemplate

class GoozEngine():
    @staticmethod
    def run(commands):
        command_str = ""
        command_array = []
        str_flag = 0
        for i in commands:
            if i == "\"":
                if str_flag == 0:
                    str_flag = 1
                elif str_flag == 1:
                    str_flag = 0
            elif i == " " and str_flag == 0:
                command_array.append(command_str)
                command_str = ""
            else:
                command_str += i
        command_array.append(command_str)
        command_str = ""
        EngineTemplate(command_array)
    
    @staticmethod
    def parser(commands):
        command_str = ""
        command_array = []
        str_flag = 0
        for i in commands:
            if i == "\"":
                if str_flag == 0:
                    str_flag = 1
                elif str_flag == 1:
                    str_flag = 0
            elif i == " " and str_flag == 0:
                command_array.append(command_str)
                command_str = ""
            else:
                command_str += i
        command_array.append(command_str)
        command_str = ""
        return command_array
```
As you can see, this library has 2 static methods. The purpose of these is to realize the parcel process. The most important purpose of Gooz Engine is to properly convert incoming commands into list objects. If needed, new special character definitions can be added and the command argument system can be improved thanks to the changes to be made in the methods in the Gooz Engine class.

## Engine Template


