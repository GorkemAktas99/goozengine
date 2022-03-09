import os
from engine.engine_template import EngineTemplate
from wifuxlogger import WifuxLogger as LOG

def run(cmds): 
    exec("{}({})".format(cmds[0],EngineTemplate.exec_formatter_api(cmds)))

def ls(cmds):
    try:
        LOG.info(os.listdir(cmds[1]))
    except Exception:
        LOG.info(os.listdir())

def pwd(cmds):
    LOG.info(os.getcwd())

def cd(cmds):
    os.chdir(cmds[1])

def rm(cmds):
    try:
        os.remove(cmds[1])
    except Exception:
        LOG.error("File couldn't be deleted")
        
def rmdir(cmds):
    try:
        os.rmdir(cmds[1])
    except Exception:
        LOG.error("Directory couldn't be deleted")

def cat(cmds):
    if cmds[1][0] == ".":
        break_flag = 0
        str_temp_cat = ""
        pwd = os.getcwd()
        for i in cmds[1]:
            if i == "." and break_flag == 0:
                break_flag = 1
                continue
            else:
                str_temp_cat += i
        path = pwd+str_temp_cat
        read(path)
    elif cmds[1][0] == "/":
        read(cmds[1])
    else:
        pwd = os.getcwd()
        path = pwd+"/"+cmds[1]
        read(path)

def read(path):
    try:
        f = open(path,'r',encoding='utf-8')
        LOG.info("\n"+f.read())
        f.close()
    except:
        LOG.error("File does not exist.")

def clear(cmds):
    print("\n" * 100)

def echo(cmds):
    for i in range(1,len(cmds)):
        print(cmds[i],end=" ")
    print("")