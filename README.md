# Python and C shellcode generator

Converts any malicious inputs written in either Python or C into Assembly level "shellcode". Which are just Assembly Opcodes. It auto-reverses the order of the input so it can be used immediately by entry into the execution stream, LIFO-style.

# How to use

Run as a python app

`python shellcodegenerator.py code.py` or `python shellcodegenerator.py code.c`

A file called shellcode.asm is automatically generated in the same directory.

To convert python files into shellcode, you need to have both Cython installed `pip install cython` and the `Python.h` header files, `sudo apt-get update;sudo apt-get install -y python-dev python3-dev`.
