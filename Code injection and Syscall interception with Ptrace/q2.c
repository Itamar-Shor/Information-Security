#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

int pid         = 0x12345678;
int addr        = 0x87654321;
int ret_zero    = 0x11111111;

int main() {

    if (ptrace(PTRACE_ATTACH, pid, NULL, NULL) == -1) {  // Attach to the process
        perror("attach");
        return 0;
    }
    int status;
    waitpid(pid, &status, 0);  // Wait for the process to stop
    if (WIFEXITED(status)) { return 0; }  // Abort if the process exits

    if(ptrace(PTRACE_POKEDATA, pid, addr, ret_zero) == -1){
        perror("poke_data");
        return 0;
    }

    if (ptrace(PTRACE_DETACH, pid, NULL, NULL) == -1) {  // Detach when done
        perror("detach");
        return 0;
    }
    return 0;
}
