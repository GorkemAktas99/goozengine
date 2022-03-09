from engine.engine_template import EngineTemplate
from wifuxlogger import WifuxLogger as LOG
import network
sta_if = network.WLAN(network.STA_IF)

def run(cmds):
    exec("{}({})".format(cmds[1],EngineTemplate.exec_formatter_api(cmds)))

def connect(cmds):
    blueprint = EngineTemplate.parameter_parser(cmds)
    if not sta_if.isconnected():
        LOG.debug('connecting to network...')
        try:
            sta_if.active(True)
            sta_if.connect(blueprint["--name"], blueprint["--password"])
        except Exception as ex:
            LOG.error(ex)
    LOG.info('Connection Successfull')

def disconnect(cmds):
    sta_if.active(False)
    LOG.debug(sta_if.isconnected())
    sta_if.active(True)

def ifconfig(cmds):
    LOG.info("")
    print("--------------------------")
    print("Network Information")
    print("--------------------------")
    info = sta_if.ifconfig()
    if sta_if.isconnected():
        print("<BROADCASTING>")
    else:
        print("<>")
    print("--------------------------")
    print("Access Point Name: "+str(sta_if.config('essid')))
    print("Access Point MAC Address: "+str(sta_if.config('mac')))
    print("--------------------------")
    print("Your Device IP: "+info[0])
    print("Subnet Mask: "+info[1])
    print("Gateway: "+info[2])
    print("DNS: "+info[3])
    

def ls(cmds):
    LOG.debug("Available WLANs")
    wlans = sta_if.scan()
    for i in wlans:
        print(str(i[0]))

def on(cmds):
    sta_if.active(True)
    LOG.info("WiFi ON")

def off(cmds):
    sta_if.active(False)
    LOG.info("WiFi OFF")

def status(cmds):
    status_code = sta_if.status()
    if status_code == 1000:
        LOG.info("No Connection and No Activities")
    elif status_code == 1001:
        LOG.info("Connecting")
    elif status_code == 202:
        LOG.error("Failed due to password error")
    elif status_code == 201:
        LOG.warning("Failed, because there is no access point reply")
    elif status_code == 1010:
        LOG.info("Connected")
    elif status_code == 203:
        LOG.error("Failed")
    elif status_code == 200:
        LOG.error("Timeout")
    elif status_code == 204:
        LOG.error("Handshake timeout")