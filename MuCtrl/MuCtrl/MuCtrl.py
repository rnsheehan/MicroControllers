import sys
import os 

# add path to our file
#sys.path.append('c:/Users/Robert/Programming/Python/Common/')
#sys.path.append('c:/Users/Robert/Programming/Python/Plotting/')

import MicroController

def main():
    pass

if __name__ == '__main__':
    main()

    pwd = os.getcwd() # get current working directory

    print(pwd)
    print("")

    MicroController.Talk_With_Hardware()
    