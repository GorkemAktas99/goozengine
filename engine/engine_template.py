import sys
import machine
import os
from wifuxlogger import WifuxLogger as LOG
from time import sleep as delay

class EngineErrors:
    @staticmethod
    def command_not_found():
        LOG.error("There is no command")

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
            elif cmds[0] == "pkg":
                exec("import dev.packager.core as package")
                exec("package.run({})".format(self.exec_formatter(cmds)))
            elif cmds[0] == "conf":
                exec("import etc.config.core as cfos")
                exec("cfos.run({})".format(self.exec_formatter(cmds)))
            elif cmds[0] == "goozshell":
                exec("import dev.goozshell.core as shell")
                exec("shell.run({})".format(self.exec_formatter(cmds)))
            elif cmds[0] == "delay":
                delay(float(cmds[1]))
            else:
                exec("import app."+cmds[0]+".main as command")
                exec("command.run({})".format(self.exec_formatter(cmds)))
        except Exception as ex:
            LOG.error(ex)
            EngineErrors.command_not_found()


    def exec_formatter(self,cmds):
        cmd_temp = "["
        for i in range(len(cmds)-1):
            cmd_temp += "'{}',".format(cmds[i])
        cmd_temp += "'{}'".format(cmds[len(cmds)-1])
        cmd_temp += "]"
        return cmd_temp
    
    def env_var_parser(self,cmds,ind):
        f = open("/etc/env/env_variables.txt","r")
        variables = f.readlines()
        for vari in variables:
            if vari == cmds[ind]:
                del cmds[ind]
                cmds.insert(ind,vari)
                return cmds
        raise Exception("This env var not found -> {}".format(cmds[ind]))
    
    def check_env_var(self,cmds):
        env_var_list = []
        for i in range(len(cmds)):
            if "$" in cmds[i]:
                env_var_list.append(i)

        return env_var_list

    @staticmethod
    def exec_formatter_api(cmds):
        cmd_temp = "["
        for i in range(len(cmds)-1):
            cmd_temp += "'{}',".format(cmds[i])
        cmd_temp += "'{}'".format(cmds[len(cmds)-1])
        cmd_temp += "]"
        return cmd_temp

    @staticmethod
    def shutdown():
        LOG.warning("System will be shutdown")
        sys.exit()
    @staticmethod
    def reset():
        machine.reset()
    @staticmethod
    def parameter_parser(cmds):
        parameter_blueprints = {}
        for i in range(len(cmds)):
            if "--" in cmds[i]:
                parameter_blueprints[cmds[i]] = cmds[i+1]
        return parameter_blueprints
                