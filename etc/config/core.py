from engine.engine_template import EngineTemplate
from engine.gooz_engine import GoozEngine
from wifuxlogger import WifuxLogger as LOG

def run(cmds):
    exec("{}({})".format(cmds[1],EngineTemplate.exec_formatter_api(cmds)))

def load():
    LOG.debug("Configure Values")
    try:
        f = open("/etc/config/configures.txt","r")
        configures = f.readlines()
        f.close()
        for i in range(len(configures)):
            if "\r\n" in configures[i]:
                configures[i] = configures[i][:-2]
        for i in range(len(configures)):
            configures[i] = GoozEngine.parser(configures[i])
        configure_blueprint = {}
        for i in configures:
            configure_blueprint[i[0]] = i[2]
        LOG.info("System has been configured")
        return configure_blueprint
    except Exception as ex:
        LOG.error("Configured variables cannot be taken")
        LOG.error(ex)

def change(cmds):
    try:
        f = open("/etc/config/configures.txt","r")
        configures = f.readlines()
        f.close()
        LOG.debug("Process has been started and variables has been taken")
        for i in range(len(configures)):
            if "\r\n" in configures[i]:
                configures[i] = configures[i][:-2]
        for i in range(len(configures)):
            configures[i] = GoozEngine.parser(configures[i])
        for i in range(len(configures)):
            if cmds[2] in configures[i][0]:
                configures[i][2] = cmds[3]
        new_confs = []
        for i in range(len(configures)):
            new_confs.append(configures[i][0] + " " + configures[i][1] + " " + configures[i][2] + "\r\n")
        f = open("/etc/config/configures.txt","w")
        for i in new_confs:
            f.write(i)
        f.close()
        LOG.info("Configuration has been changed successfully")
    except Exception as ex:
        LOG.error("Configures can not be changed")
        LOG.error(ex)
    
