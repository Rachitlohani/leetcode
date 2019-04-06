Every application(program) comes into execution through means of process, process is a running instance of a program. Processes are created through different system calls, most popular are fork() and exec()

  # fork()

pid_t pid = fork();
fork() creates a new process by duplicating the calling process, The new process, referred to as child, is an exact duplicate of the calling process, referred to as parent, except for the following :

1. The child has its own unique process ID, and this PID does not match the ID of any existing process group.
2. The child’s parent process ID is the same as the parent’s process ID.
3. The child does not inherit its parent’s memory locks and semaphore adjustments.
4. The child does not inherit outstanding asynchronous I/O operations from its parent nor does it inherit any asynchronous I/O contexts from its parent.

### Return value of fork()
On success, the PID of the child process is returned in the parent, and 0 is returned in the child. On failure, -1 is returned in the parent, no child process is created, and errno is set appropriately.

  # exec()

The exec() family of functions replaces the current process image with a new process image. It loads the program into the current process space and runs it from the entry point.

The exec() family consists of following functions, I have implemented execv() in following C program, you can try rest as an exercise

```int execl(const char *path, const char *arg, ...);
int execlp(const char *file, const char *arg, ...);
int execle(const char *path, const char *arg, ..., 
                               char * const envp[]);
int execv(const char *path, char *const argv[]);
int execvp(const char *file, char *const argv[]);
int execvpe(const char *file, char *const argv[], 
                              char *const envp[]);

```
### fork vs exec

1. fork starts a new process which is a copy of the one that calls it, while exec replaces the current process image with another (different) one.
2. Both parent and child processes are executed simultaneously in case of fork() while Control never returns to the original program unless there is an exec() error.
