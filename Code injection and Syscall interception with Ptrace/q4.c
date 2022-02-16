#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/user.h>

int pid = 0x12345678;

int main(int argc, char **argv) {
    // Make the malware stop waiting for our output by forking a child process:
    if (fork() != 0) {
        // Kill the parent process so we stop waiting from the malware
        return 0;
    } else {
        // Close the output stream so we stop waiting from the malware
        fclose(stdout);
    }
    
    struct user_regs_struct regs;
    unsigned int read_syscall = 3;
    int status;

    if (ptrace(PTRACE_ATTACH, pid, NULL, NULL) == -1) {  // Attach to the process
        perror("attach");
        return 0;
    }
    waitpid(pid, &status, 0);  // Wait for the process to stop
    if (WIFEXITED(status)) { return 0; }  // Abort if the process exits


    while(1){

        //before the syscall
        if(ptrace(PTRACE_SYSCALL, pid, NULL, NULL) == -1){
            perror("poke_data");
            return 0;
        }
        waitpid(pid, &status, 0);  // Wait for the process to stop
        if (WIFEXITED(status)) { return 0; }  // Abort if the process exits

        //read regs
        if(ptrace(PTRACE_GETREGS, pid, NULL, &regs) == -1){
            perror("get_regs");
            return 0;
        }
        if(regs.orig_eax == read_syscall){
            //changing edx = 0 (size to read)
            regs.edx = 0;
            if(ptrace(PTRACE_SETREGS, pid, NULL, &regs) == -1){
                perror("set_regs");
                return 0;
            }
        }

        //after the syscall
        if(ptrace(PTRACE_SYSCALL, pid, NULL, NULL) == -1){
            perror("poke_data");
            return 0;
        }
        waitpid(pid, &status, 0);  // Wait for the process to stop
        if (WIFEXITED(status)) { return 0; }  // Abort if the process exits
    }
    //not really neccessary
    if (ptrace(PTRACE_DETACH, pid, NULL, NULL) == -1) {  // Detach when done
        perror("detach");
        return 0;
    }
    return 0;
}
