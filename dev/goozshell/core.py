from engine.engine_template import EngineTemplate
from engine.gooz_engine import GoozEngine
from wifuxlogger import WifuxLogger as LOG

def run(cmds): 
    f = open(cmds[1],"r")
    commands = f.readlines()
    for i in range(len(commands)):
        if "\r\n" in commands[i]:
            commands[i] = commands[i][:-2]
    for command in commands:
        cmd_array = GoozEngine.parser(command)
        EngineTemplate(cmd_array)
    
