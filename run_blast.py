""" Program to run the blast algorithm and
 return useful information from it """


import pickle
from blast import blast
import sys
from termcolor import colored
import os


def run_blast(args):
    """ Application wrapper for blast algorithm """
    print(colored("\n\n\n ____  _                _____ _______ \n|  _ \| |        /\    / ____|__   __|\n| |_) | |       /  \  | (___    | |   \n|  _ <| |      / /\ \  \___ \   | |   \n| |_) | |____ / ____ \ ____) |  | |   \n|____/|______/_/    \_\_____/   |_|   \n", "blue", attrs=['bold']))
    print(colored("A python implementation of BLAST (basic local alignment search tool)\n\n\n", 'blue'))
    if len(args) < 2:
        data_file = input("Enter data file path: ")
        dict_file = input("Enter dictionary file path: ")
    else:
        data_file = os.getcwd() + args[1]
        dict_file = os.getcwd() + args[2]
    sequence = input("Enter Search sequence: ")
    print("Calculating...")
    results = blast(sequence, dict_file, data_file)
    results.sort(key=lambda x:x[2], reverse=True)

    print('\n\nResults:\n')
    
    for result in results[:5]:
        print(colored("\nScore: ", "green", attrs=['bold']), result[2])
        print(colored("Position: ", "blue", attrs=['bold']), result[1])
        print(colored("Sequence", "blue", attrs=['bold']), result[0])

    
if __name__ == "__main__":
    run_blast(sys.argv)