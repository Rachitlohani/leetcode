#### Basics
**userspace** : Virtual memory space dedicated to user process. This is where your shell runs. 

**KernelSpace** :  Virtual memory space from where you can run any syscall and has access to all the userspaces. 

**syscall** : system calls, collection of interfaces in the kernel that are resposible for interacting with the hardware. 


```
while (1) { 
char *cmd = read_command(); 
int child_pid = fork(); 
if (child_pid == 0) { 
exec(cmd); 
}
else { 
waitpid(child_pid); 
 } 
} 
```
