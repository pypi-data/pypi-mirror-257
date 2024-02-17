<p><span><span style="font-family:Verdana, Arial, Helvetica, sans-serif;line-height:19px;text-indent:26px;"><span style="font-size:14px;"><span style="font-family:Arial;line-height:26px;"><br></span></span></span></span></p>

# BFFuck

 Makes brainfucking easier

This is a work in progress

The tools is an esoteric language that compiles to brainfuck, using algorithms in [brainfuck algorithms](https://esolangs.org/wiki/Brainfuck_algorithms).

### Usage:
Run this in Python:
```python
from bffuck import BFFuck
bff=BFFuck()
bf=bff.compile('Your code')
```

Note that if a BFFuck object is created and used, its status will change and therefore cannot compile another program.
### Syntax
BFFuck currently supports the following syntax:

Comment:
```
# Comment
```
Variable definition:
```text
<variable 1>=<variable 2>
or
<variable>=<number>
```

Addition:
```text
add(x,<number>)
or
add(x,<variable>)
```

Subtraction:
```
sub(x,<number>)
or
sub(x,<variable>)
```

Multiplication:
```
mul(x,<number>)
or
mul(x,<variable>)
```

While loop:
```text
while(<variable or number>)
CODE
endwhile
```

I/O:
```text
<variable>=in # Reads <variable> as decimal integer
<variable>=inc # Reads <variable> as ASCII character
out(<variable or number>) # Outputs <variable> as decimal integer
outc(<variable or number>) # Outputs <variable> as ASCII character
```

String output shortcut:
```text
print(STRING) # Without quotes
# For instance
print(Hello World!)
```

One-branch if statement:
```text
if(<variable or number>)
CODE
endif
```

### Platform
BFFuck is in **pure Python** and therefore it supports any platform.

### Constraints
Programs compiled from BFFuck needs you to have 8 bit cells that wrap.

### Disadvantages
BFFuck currently has these disadvantages:
1. It's numbers are 8 bit numbers.
2. It has some bugs.


The repository contains some examples, including a Hello World program, a cat program and an A+B program.
