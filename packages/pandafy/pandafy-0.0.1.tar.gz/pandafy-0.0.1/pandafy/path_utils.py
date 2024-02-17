import sys
import os




def get_platform():
    if sys.platform.startswith('win'):
        return 1
    elif sys.platform.startswith('linux'):
        return 0
    else:
        raise SystemError("Only works on Linux or Windows")

def generate_homedir():
    platform = get_platform()
    homedir_dict = {0:os.path.expanduser("~"),1:"C:\\"}
    return homedir_dict[platform]