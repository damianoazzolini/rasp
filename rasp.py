import sys
import readline
import argparse
import signal
# import time

try:
    import clingo
except:
    print("Install clingo to use this.")
    sys.exit()

options = '''
Interactive mode options:
- in: inputs a program
- all | a: computes all the answer sets
- solve | s: computes 1 answer set
- solve(n) | s(n): compute n answer sets
- cautious | c: compute cautious consequences
- brave | b: compute brave consequences
- clear: delete the content of the file passed as input from rasp memory
- what | ?: prints what is currently in memory
- dump: prints the current session into a file called 'rasp_session.lp'
- exit | e: exits (for input mode and program)
'''

def ctrl_c_handler(signum, frame):  # type: ignore
    print('\nBye')
    sys.exit()


# mode = 0 -> all AS
# mode = 1 -> 1 AS
# mode = 2 -> cautious
# mode = 3 -> brave
def call_clingo(program_lines : 'list[str]', mode : int, n_as : int = 1):
    e_type = ""
    if mode == 0:
        e_type = "0"
    elif mode == 1:
        e_type = str(n_as)
    elif mode == 2:
        e_type = "--enum-mode=cautious"
    elif mode == 3:
        e_type = "--enum-mode=brave"

    ctl = clingo.Control([e_type])  # type: ignore

    try:
        for l in program_lines:
            ctl.add('base', [], l)  # type: ignore
        ctl.ground([("base", [])])  # type: ignore
    except RuntimeError as e:
        print(repr(e))
        return

    # start_time = time.time()

    i = 0
    with ctl.solve(yield_=True) as handle:  # type: ignore
        for m in handle:  # type: ignore
            print(f"{i}: {str(m)}")  # type: ignore
            i = i + 1
        handle.get()  # type: ignore
    
    # end_time = start_time - time.time()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, ctrl_c_handler)  # type: ignore

    stop_loop = False
    lines : 'list[str]' = []

    command_parser = argparse.ArgumentParser(
        description="rasp: a REPL for ASP", epilog=options)
    command_parser.add_argument("--filename", help="Starting program", type=str, default="")
    args = command_parser.parse_args()

    f_lines : 'list[str]' = []

    if args.filename != "":
        try:
            f = open(args.filename, 'r')
            f_lines = f.readlines()
            f.close()
        except:
            print(f"file {args.filename} not found")
            sys.exit()

    lines = f_lines.copy()

    print('rasp: type \'exit\' or \'e\' to exit')
    while not stop_loop:
        command = input('> ').strip()
        if command == 'input' or command == 'in':
            lines = []
            if f_lines != []:
                lines = f_lines.copy()
            print('Input mode, type \'exit\' or \'e\' to exit')
            command = input(': ')
            while command != 'exit' and command != 'e':
                lines.append(command)
                command = input(': ')
        elif command == 'solve' or command == 's':
            call_clingo(lines, 1)
        elif command == 'cautious' or command == 'c':
            call_clingo(lines, 2)
        elif command == 'brave' or command == 'b':
            call_clingo(lines, 3)
        elif command == 'all' or command == 'a':
            call_clingo(lines, 0)
            # all solutions
        elif command.startswith('solve(') or command.startswith('s('):
            n_as = int(command.split('(')[1].split(')')[0])
            call_clingo(lines, 1, n_as)
        elif command == 'clear':
            # deletes the file lines from memory
            f_lines.clear()
            lines.clear()
        elif command == 'what' or command == '?':
            for l in lines:
                print(l)
        elif command == 'dump':
            try:
                f = open('rasp_session.lp', 'w')
                for l in lines:
                    f.write(f"{l}\n")
                f.close()
            except:
                print('Cannot open rasp_session.lp to write the current session')
        elif command == 'help' or command == 'h':
            print(options)
        elif command == 'exit' or command == 'e':
            print('bye')
            stop_loop = True
        else:
            print(f"command <{command}> not recognized.")
