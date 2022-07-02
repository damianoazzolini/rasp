# rasp: a REPL for ASP (clingo)
REPL for ASP (clingo).

It allows to compute the answer sets for a program read from stdin or to combine the content of a program stored into a file and a program read from stdin.

Interactive mode options:
```
- in: inputs a program
- all | a: computes all the answer sets
- solve | s: computes 1 answer set
- solve(n) | s(n): compute n answer sets
- cautious | c: compute cautious consequences
- brave | b: compute brave consequences
- clear: delete the content of the file from memory
- exit | e: exits (for input mode and program)
- what | ?: prints what is currently in memory
- dump: prints the current session on a file called 'rasp_session.lp'
```

## Installation
git clone 

## Examples
```
rasp: type 'exit' or 'e' to exit
> in
Input mode, type 'exit' or 'e' to exit
: 0{a}1.
: e
> a
0: 
1: a
> e
bye
```

```
$ cat a.tmp 
0{a}1.
$ rasp.py --filename="a.tmp"
rasp: type 'exit' or 'e' to exit
> in
Input mode, type 'exit' or 'e' to exit
: 0{b}1.
: exit
> all
0: 
1: a
2: b
3: a b
```
```
rasp: type 'exit' or 'e' to exit
> in
Input mode, type 'exit' or 'e' to exit
: 0{b}1.
: e
> a
0: 
1: a
2: b
3: a b
> ?
0{a}1.

0{b}1.
> clear
> ?
> e
bye
```
