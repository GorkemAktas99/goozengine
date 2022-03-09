# Gooz Engine for Micropython<hr/>

This engine was designed by Görkem Aktaş for Gooz Project to run on MicroPython. Designed for Gooz OS, this engine acts as the main layer of the operating system.

## How It Works<hr/>

MicroPython runs files over main.py. So this engine took the starting point as main.py. If desired, main.py can be changed and GoozEngine and EngineTemplate classes, which are the main parts of the engine, can be used.

## main.py<hr/>
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
## Gooz Engine<hr/>
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

## Engine Template<hr/>
The Engine Template is dynamically designed and designed in such a way that it can be easily shaped for general purposes and does not complicate the code development work with the growth of the project.<br/>
The class has its own error handling. The purpose here is to prevent the operating system from crashing no matter what and to communicate the errors to the user in an understandable way.<br/>
### Engine Template Class
```python
class EngineTemplate():
    _filesystem_list = ["ls","pwd","cd","rm","rmdir","cat","clear","echo"]
    _wifi_list = ["wifi"]
    _engine_commands = ["shutdown","reset"]

    def __init__(self,cmds):

        if "$" in cmds[0]:
            exec("import etc.env.env_manager as env")
            exec("env.write({})".format(self.exec_formatter(cmds)))
        
        elif self.check_env_var(cmds):
            for i in self.check_env_var(cmds):
                cmds = self.env_var_parser(cmds,i)
                self.registry(cmds)
        else:
            self.registry(cmds)
```
Here is the constructor method for the Engine Template. The system first checks if there is an environment variable record. As can be seen, the operations are not carried out directly by means of an import, but by dynamically shaped file calls. There is a registry function for the functions to be called and their parameters.
### Registry Process
```python
    def registry(self,cmds):
        try:
            if cmds[0] in self._filesystem_list:
                exec("import dev.filesystem.core as fsos")
                exec("fsos.run({})".format(self.exec_formatter(cmds)))
            elif cmds[0] in self._engine_commands:
                exec("EngineTemplate.{}()".format(cmds[0],self.exec_formatter(cmds)))
            elif cmds[0] in self._wifi_list:
                exec("import dev.wifi.core as wfos")
                exec("wfos.run({})".format(self.exec_formatter(cmds)))
            elif cmds[0] == "env":
                exec("import etc.env.env_manager as env")
                exec("env.show()")
            elif cmds[0] == "conf":
                exec("import etc.config.core as cfos")
                exec("cfos.run({})".format(self.exec_formatter(cmds)))
            else:
                exec("import app."+cmds[0]+".main as command")
                exec("command.run({})".format(self.exec_formatter(cmds)))
        except Exception as ex:
            LOG.error(ex)
            EngineErrors.command_not_found()
```
If a base operation is to be developed regarding the engine, it must be registered in the registry function. Otherwise, packages should be located in the app folder, such as package development. The important thing in these packages is to create a folder with the name of the package. Then there should be a main.py file in the package and a run function should be defined in this file that will take the "cmds" parameters.
### Static Method : Exec Formatter
```python
    @staticmethod
    def exec_formatter_api(cmds):
        cmd_temp = "["
        for i in range(len(cmds)-1):
            cmd_temp += "'{}',".format(cmds[i])
        cmd_temp += "'{}'".format(cmds[len(cmds)-1])
        cmd_temp += "]"
        return cmd_temp
```
Some problems occur when the parameters are passed from a static variable to a dynamic structure in string format. An "Exec Formatter" is used in the Engine Template to prevent them. This formatter can also be called from other files as a static method. When you want to send a list parameter to the exec function, which you usually need to send the "cmds" parameters, you can use this method.
### Static Method : Parameter Parser
```python
    @staticmethod
    def parameter_parser(cmds):
        parameter_blueprints = {}
        for i in range(len(cmds)):
            if "--" in cmds[i]:
                parameter_blueprints[cmds[i]] = cmds[i+1]
        return parameter_blueprints
```
Some parameters may be needed from the written command arguments. For example, in a wifi operation, you may want to transmit data such as ssid and password from the terminal as parameters. In these cases, you can separate the parameters in your commands and turn them into a blueprint, thanks to the parameter parser. Blueprints are readable json format files. They are stored as key-value pairs. So it can be accessed from within the scripts. For example, a parameter like --name hello will be sent to you with blueprint["--name"] accessibility.

