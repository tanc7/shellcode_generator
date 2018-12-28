import subprocess, threading, os, sys, operator

# Generates shellcode from C and Python files

def bash_cmd(cmd):
    subprocess.call(
        cmd,
        shell=True,
        executable='/bin/bash'
    )
    return

def popen_subprocess(cmd):
    p = subprocess.Popen(
        cmd,
        shell=True,
        executable='/bin/bash',
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    o = p.stdout.read()
    output = str(o.encode('utf-8')).strip().rstrip()
    return output

def Reverse(buffer):
    # shellcode = buffer[::-1]
    shellcode = list(reversed(buffer))
    return shellcode

def main():

    # how to use

    if len(sys.argv) != 2:
        print "-----------------------\r\nUsage:\r\npython shellcodegenerator.py code.c\r\nor\r\npython shellcodegenerator.py code.py"
        exit(0)

    infile = sys.argv[1]
    n = infile.split('.')
    filenoext = n[0]
    # if file ends with .py

    if infile.endswith(".py"):
        print "-----------------------\r\n.py file detected, converting to C language using Cython"
        cmd = "cython {}".format(str(infile))
        infile = filenoext + '.c'
        bash_cmd(cmd)
    

    # if file ends with .c

    
    cmd = "gcc {} -o {}".format(str(infile),str(filenoext))
    print "-----------------------\r\nCompiling to executable using gcc\r\n" + str(cmd)

    bash_cmd(cmd)

    # commands in /bin/bash to eliminate null bytes and generate formatted shellcode
    cmd = """objdump -d {} | tr "\t" " " | tr " " "\n" | egrep "^[0-9a-f]{{2}}$" | grep -v 00""".format(str(filenoext))
    print "-----------------------\r\nUsing objdump to dump significant opcodes and eliminating nullbytes\r\n"+str(cmd)

        # for i in $purgenullbytes:
        #     do echo -n "\\x$i"
        #     done""".format(str(filenoext))

    out = popen_subprocess(cmd)
    outw = open("out",'w')
    outw.write(out)
    outw.close()

    r = open("out",'r')
    l = r.readlines()
    # print l
    # l = out.split()
    m = []
    for i in l:
        i = i.replace('\n','')
        # i = "\\x" + str(i)
        m.append(i)
    # print m
    
    # for i in m:
    #     buffer = ''.join(i)
    # buffer = ''.join(m)
    buffer = m
    # print buffer
    # reverse the assembly code to make injectable LIFO assembly opcodes

    print "-----------------------\r\nReversing buffer into usable shellcode"
    shellcode = Reverse(buffer)
    scl = []
    for i in shellcode:
        i = '\\x' + str(i)
        scl.append(i)
    sc = ''.join(scl)

    print "-----------------------\r\nShellcode generated! Enter into EIP/RIP Register for execution.\r\n\n\n"
    print sc

    w = open("shellcode.asm","w")
    w.write(sc)
    w.close()

    print "-----------------------\r\nShellcode saved as shellcode.asm"
    return
main()