import argparse
from rich import print
from rich.prompt import Prompt
import subprocess
import sys

from .llms import translateLlama, translateGPT4, translateAzure


def translateCommand(description, model, previous=[]):
    model=model.lower()

    if model == 'llama':
        return translateLlama(description, previous)
    elif model == 'gpt4':
        return translateGPT4(description, previous)
    elif model == 'azure':
        return translateAzure(description, previous)
    else:
        print(f"Unknown model: {model}")



def proposeCommand(command):
    print(f"Proposed command: '{command}'")
    answer = Prompt.ask("Do you want to run the above command?: ", choices=['y','n'])
    return answer.lower() == 'y'

def proposeRetry():
    answer = Prompt.ask("Do you want to try generating a different command?: ", choices=['y','n'])
    return answer.lower() == 'y'


def runCommand(command, verbose=False):
    if verbose:
        print(f"Running command: '{command}'")
    p = subprocess.run(command, shell=True, executable="/bin/bash", input=sys.stdin.read())
    if verbose:
        print(f"Command finished with returncode {p.returncode}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("description", help="English description of the command you'd like to run")
    parser.add_argument("-y", "--yes", help="Run the command without asking for confirmation (dangerous)", action="store_true")
    parser.add_argument("--verbose", help="Print the command before running it", action="store_true")
    parser.add_argument("--model", default="GPT4", choices=["Llama", "GPT4", "Azure"], help="Which model to use")

    args = parser.parse_args()

    previousCommands = []
    keepTrying = True
    while keepTrying:
        command = translateCommand(args.description, args.model, previousCommands)

        if args.yes or proposeCommand(command):
            keepTrying = False
            runCommand(command, verbose=args.verbose)
        else:
            previousCommands.append(command)
            keepTrying = proposeRetry()



if __name__ == "__main__":
    main()