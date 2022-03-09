from wifuxlogger import WifuxLogger as LOG

class EnvSyntaxErrors:
    @staticmethod
    def equal_format_error():
        LOG.error("There is a equal format syntax error")

def write(cmds):
    try:
        if cmds[1] == "=":
            f = open("/etc/env/env_variables.txt","r")
            env_vars = f.readlines()
            format_var = ""
            for i in cmds:
                format_var += i
                format_var += " "
            format_var += "\n"
            env_vars.append(format_var)
            f.close()
            open("/etc/env/env_variables.txt","w").close()
            f = open("/etc/env/env_variables.txt","r")
            for i in env_vars:
                f.write(i)
            f.close()

    except Exception:
        EnvSyntaxErrors.equal_format_error()

def show():
    f = open("/etc/env/env_variables.txt","r")
    env_vars = f.readlines()
    for i in env_vars:
        print(i,end="")
    f.close()
