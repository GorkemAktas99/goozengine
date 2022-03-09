from engine.engine_template import EngineTemplate
from wifuxlogger import WifuxLogger as LOG
from urequests import get as restget
from ujson import loads as jloads
from os import mkdir

def run(cmds):
    LOG.debug("Exec")
    exec("{}({})".format(cmds[1],EngineTemplate.exec_formatter_api(cmds)))

def install(cmds):
    LOG.debug("Install")
    #pkg install webgooz
    if ":" in cmds[2]:
        new = cmds[2].split(":")
    else:
        response = jloads(restget("https://raw.githubusercontent.com/gooz-project/gooz_packages/main/"+cmds[2]+"/default.json").text)
        mkdir("/app/" + response["name"])
        