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
        /* The idea: divide the input by all posibble divisor and check if divisor == quotient (and the reminder is zero). */
        "CMP EBX, 1;"
        "JL _RET_ZERO;"         //if input < 1: need to return 0.
        
        "MOV ECX, 0;"           //initial divisor.
        "MOV ESI, EBX;"
        "SHR ESI, 1;"           // ESI = EBX / 2. so we could run till input / 2.
        "INC ESI;"              // ESI = EBX / 2 + 1. 
        "_LOOP:;"
            /*information about div: https://www.aldeid.com/wiki/X86-assembly/Instructions/div */
            "INC ECX;"          // divisor++.
            "CMP ECX, ESI;"
            "JG _RET_ZERO;"
            "MOV EDX, 0;"       //clear dividend.
            "MOV EAX, EBX;"     //dividend.
            "div ECX;"          //EAX = quotient, EDX = reminder.

            "CMP EDX, 0;"
            "JNE _LOOP;"        // if the reminder is not 0, check the next divisor.
            "CMP EAX, ECX;"
            "JNE _LOOP;"        // if tdivisor == quotient, check the next divisor.
            "JMP _END;"         // the require result is already in EAX.

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
