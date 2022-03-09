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