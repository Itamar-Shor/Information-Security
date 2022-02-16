#include <stdio.h>
#include <stdlib.h>

int main(int argc, char* argv[])
{
    int input, output;

    if (argc != 2) {
        printf("USAGE: %s <number>\n", argv[0]);
        return -1;
    }

    input = atoi(argv[1]);

    asm ("MOV   EBX, %0"
        :
        : "r"(input));

    asm (
        /* Your code starts here. */
        /* Last semester in the course 'Computer structure' we had to implement fibonacci in MIPS assembly, so I took inspiration from there.*/
        /*information about mul: https://www.aldeid.com/wiki/X86-assembly/Instructions/mul */
        "CMP EBX, 0;"
        "JL _RET_ZERO;"
        "CALL _SQUAR_FIB;"
        "JMP _END;"

        "_SQUAR_FIB:;"
            "PUSH EBX;"
            "PUSH ESI;"
            "CMP EBX, 1;"
            "JG _REC;"
            "MOV EAX, EBX;"                     // if EBX = 0 or 1 then the result is 0 or 1 (respectively).
            "JMP _POP_AND_RET;"

        "_REC:;"                                // we get here only if EBX > 1.
            "SUB EBX, 1;"                       // EBX--.
            "CALL _SQUAR_FIB;"                  // EAX = Squarebonacci(EBX-1).
            "MOV ESI, EAX;"                     // store in ESI the Squarebonacci(EBX-1).
            "MOV EBX, [ESP + 4];"
            "SUB EBX, 2;"                       // EBX-=2.
            "CALL _SQUAR_FIB;"                  // EAX = Squarebonacci(EBX-2).
            "MUL EAX;"                          // EAX = quarebonacci(EBX-2) ^ 2.
            "MOV ECX, EAX;"
            "MOV EAX, ESI;"
            "MUL EAX;"                          // EAX = quarebonacci(EBX-1) ^ 2.
            "ADD EAX, ECX;"                     // EAX = quarebonacci(EBX-1) ^ 2 + quarebonacci(EBX-2) ^ 2.
            "POP ESI;"
            "POP EBX;"
            "RET;"

        "_POP_AND_RET:;"
            "ADD ESP, 8;"
            "RET;"
        
        "_RET_ZERO:;"
            "MOV EAX, 0;"

        "_END:;"
        /* Your code stops here. */
    );

    asm ("MOV   %0, EAX"
        : "=r"(output));

    printf("%d\n", output);

    return 0;
}
