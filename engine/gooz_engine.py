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

