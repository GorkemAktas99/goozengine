class WifuxLogger:
    @staticmethod
    def warning(msg):
        print("\033[93mWARNING:",end="")
        print(msg,end="")
        print("\033[0m")
    @staticmethod
    def error(msg):
        print("\033[91mERROR:",end="")
        print(msg,end="")
        print("\033[0m")
    @staticmethod
    def info(msg):
        print("\033[94mINFO:",end="")
        print(msg,end="")
        print("\033[0m")
    @staticmethod
    def debug(msg):
        print("\033[92mDEBUG:",end="")
        print(msg,end="")
        print("\033[0m")
