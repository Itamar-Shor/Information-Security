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
        /* inspiration from: https://stackoverflow.com/questions/15047116/an-iterative-algorithm-for-fibonacci-numbers */
        "CMP EBX, 0;"
        "JL _RET_ZERO;"

        "MOV ECX, 0;"
        "MOV ESI, 0;"           // ESI = 0 (first element in the Squarebonacci series).
        "MOV EDI, 1;"           // EDI = 0 (first element in the Squarebonacci series).

        "_LOOP:;"
            "CMP ECX, EBX;"
            "JGE _SET_VALUE;"
            "MOV EAX, ESI;"     
            "MUL EAX;"          // EAX = ESI^2.
            "MOV ESI, EAX;"     // ESI = EAX.
            "MOV EAX, EDI;"
            "MUL EAX;"          // EAX = EDI^2.
            "ADD EAX, ESI;"     // EAX = EDI^2 + ESI^2;
            "MOV ESI, EDI;"     // ESI = EDI.
            "MOV EDI, EAX;"     // EDI = EAX.
            "INC ECX;"
            "JMP _LOOP;"

        "_RET_ZERO:;"
            "MOV EAX, 0;"
            "JMP _END;"
        
        "_SET_VALUE:;"
            "MOV EAX, ESI;"

        "_END:;"
        /* Your code stops here. */
    );

    asm ("MOV   %0, EAX"
        : "=r"(output));

    printf("%d\n", output);

    return 0;
}
