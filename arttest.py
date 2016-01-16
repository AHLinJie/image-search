# coding=utf-8

import sys

def main():
    print ('Hello there', "arg1:", sys.argv[1], "arg2:", sys.argv[2], "arg3", sys.argv[3], "arg0", sys.argv[0])
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()