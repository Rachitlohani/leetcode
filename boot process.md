## Booting Linux from a Disk
A two-stage boot loader is required to boot a Linux kernel from disk. A well-known
Linux boot loader on 80 × 86 systems is named LInux LOader (LILO). Other boot
loaders for 80 × 86 systems do exist; for instance, the GRand Unified Bootloader
(GRUB) is also widely used. GRUB is more advanced than LILO, because it recognizes
several disk-based filesystems and is thus capable of reading portions of the
boot program from files. Of course, specific boot loader programs exist for all architectures
supported by Linux.
LILO may be installed either on the MBR (replacing the small program that loads the
boot sector of the active partition) or in the boot sector of every disk partition. In
both cases, the final result is the same: when the loader is executed at boot time, the
user may choose which operating system to load.
Actually, the LILO boot loader is too large to fit into a single sector, thus it is broken
into two parts. The MBR or the partition boot sector includes a small boot loader,
which is loaded into RAM starting from address 0x00007c00 by the BIOS. This small
program moves itself to the address 0x00096a00, sets up the Real Mode stack (rangingfrom 0x00098000 to 0x000969ff), loads the second part of the LILO boot loader into
RAM starting from address 0x00096c00, and jumps into it.
In turn, this latter program reads a map of bootable operating systems from disk and
offers the user a prompt so she can choose one of them. Finally, after the user has
chosen the kernel to be loaded (or let a time-out elapse so that LILO chooses a
default), the boot loader may either copy the boot sector of the corresponding partition
into RAM and execute it or directly copy the kernel image into RAM.
Assuming that a Linux kernel image must be booted, the LILO boot loader, which
relies on BIOS routines, performs essentially the following operations:
1. Invokes a BIOS procedure to display a “Loading” message.
2. Invokes a BIOS procedure to load an initial portion of the kernel image from
disk: the first 512 bytes of the kernel image are put in RAM at address
0x00090000, while the code of the setup( ) function (see below) is put in RAM
starting from address 0x00090200.
3. Invokes a BIOS procedure to load the rest of the kernel image from disk and puts
the image in RAM starting from either low address 0x00010000 (for small kernel
images compiled with make zImage) or high address 0x00100000 (for big kernel
images compiled with make bzImage). In the following discussion, we say that the
kernel image is “loaded low” or “loaded high” in RAM, respectively. Support for
big kernel images uses essentially the same booting scheme as the other one, but
it places data in different physical memory addresses to avoid problems with the
ISA hole mentioned in the section “Physical Memory Layout” in Chapter 2.
4. Jumps to the setup( ) code.


Middle Ages: the setup( ) Function

The code of the setup( ) assembly language function has been placed by the linker at
offset 0x200 of the kernel image file. The boot loader can therefore easily locate the
code and copy it into RAM, starting from physical address 0x00090200.
The setup( ) function must initialize the hardware devices in the computer and set
up the environment for the execution of the kernel program. Although the BIOS
already initialized most hardware devices, Linux does not rely on it, but reinitializes
the devices in its own manner to enhance portability and robustness. setup( ) performs
essentially the following operations:
1. In ACPI-compliant systems, it invokes a BIOS routine that builds a table in RAM
describing the layout of the system’s physical memory (the table can be seen in
the boot kernel messages by looking for the “BIOS-e820” label). In older systems,
it invokes a BIOS routine that just returns the amount of RAM available in
the system.
2. Sets the keyboard repeat delay and rate. (When the user keeps a key pressed past
a certain amount of time, the keyboard device sends the corresponding keycode
over and over to the CPU.)
3. Initializes the video adapter card.
4. Reinitializes the disk controller and determines the hard disk parameters.
5. Checks for an IBM Micro Channel bus (MCA).
6. Checks for a PS/2 pointing device (bus mouse).
7. Checks for Advanced Power Management (APM) BIOS support.
8. If the BIOS supports the Enhanced Disk Drive Services (EDD), it invokes the
proper BIOS procedure to build a table in RAM describing the hard disks available
in the system. (The information included in the table can be seen by reading
the files in the firmware/edd directory of the sysfs special filesystem.)
9. If the kernel image was loaded low in RAM (at physical address 0x00010000), the
function moves it to physical address 0x00001000. Conversely, if the kernel image
was loaded high in RAM, the function does not move it. This step is necessary
because to be able to store the kernel image on a floppy disk and to reduce the
booting time, the kernel image stored on disk is compressed, and the decompression
routine needs some free space to use as a temporary buffer following
the kernel image in RAM.
10. Sets the A20 pin located on the 8042 keyboard controller. The A20 pin is a hack
introduced in the 80286-based systems to make physical addresses compatible
with those of the ancient 8088 microprocessors. Unfortunately, the A20 pin
must be properly set before switching to Protected Mode, otherwise the 21st bit
of every physical address will always be regarded as zero by the CPU. Setting the
A20 pin is a messy operation.
11. Sets up a provisional Interrupt Descriptor Table (IDT) and a provisional Global
Descriptor Table (GDT).
12. Resets the floating-point unit (FPU), if any.
13. Reprograms the Programmable Interrupt Controllers (PIC) to mask all interrupts,
except IRQ2 which is the cascading interrupt between the two PICs.
14. Switches the CPU from Real Mode to Protected Mode by setting the PE bit in the
cr0 status register. The PG bit in the cr0 register is cleared, so paging is still
disabled.
15. Jumps to the startup_32( ) assembly language function.
Renaissance: the startup_32( ) Functions
There are two different startup_32( ) functions; the one we refer to here is coded in
the arch/i386/boot/compressed/head.S file. After setup( ) terminates, the function has
been moved either to physical address 0x00100000 or to physical address 0x00001000,
depending on whether the kernel image was loaded high or low in RAM.
This function performs the following operations:
1. Initializes the segmentation registers and a provisional stack.
2. Clears all bits in the eflags register.
3. Fills the area of uninitialized data of the kernel identified by the _edata and _end
symbols with zeros (see the section “Physical Memory Layout” in Chapter 2).
4. Invokes the decompress_kernel( ) function to decompress the kernel image. The
“Uncompressing Linux...” message is displayed first. After the kernel image is
decompressed, the “OK, booting the kernel.” message is shown. If the kernel
image was loaded low, the decompressed kernel is placed at physical address
0x00100000. Otherwise, if the kernel image was loaded high, the decompressed
kernel is placed in a temporary buffer located after the compressed image. The
decompressed image is then moved into its final position, which starts at physical
address 0x00100000.
5. Jumps to physical address 0x00100000.
The decompressed kernel image begins with another startup_32( ) function included
in the arch/i386/kernel/head.S file. Using the same name for both the functions does
not create any problems (besides confusing our readers), because both functions are
executed by jumping to their initial physical addresses.
The second startup_32( ) function sets up the execution environment for the first
Linux process (process 0). The function performs the following operations:
1. Initializes the segmentation registers with their final values.
2. Fills the bss segment of the kernel (see the section “Program Segments and Process
Memory Regions” in Chapter 20) with zeros.
3. Initializes the provisional kernel Page Tables contained in swapper_pg_dir and
pg0 to identically map the linear addresses to the same physical addresses, as
explained in the section “Kernel Page Tables” in Chapter 2.
4. Stores the address of the Page Global Directory in the cr3 register, and enables
paging by setting the PG bit in the cr0 register.
5. Sets up the Kernel Mode stack for process 0 (see the section “Kernel Threads” in
Chapter 3).
6. Once again, the function clears all bits in the eflags register.
7. Invokes setup_idt( ) to fill the IDT with null interrupt handlers (see the section
“Preliminary Initialization of the IDT” in Chapter 4).
8. Puts the system parameters obtained from the BIOS and the parameters passed
to the operating system into the first page frame (see the section “Physical Memory
Layout” in Chapter 2).
9. Identifies the model of the processor.
10. Loads the gdtr and idtr registers with the addresses of the GDT and IDT tables.
11. Jumps to the start_kernel( ) function.

Modern Age: the start_kernel( ) Function

The start_kernel( ) function completes the initialization of the Linux kernel. Nearly
every kernel component is initialized by this function; we mention just a few of
them:

The scheduler is initialized by invoking the sched_init() function (see Chapter 7).
* The memory zones are initialized by invoking the build_all_zonelists() function (see the section “Memory Zones” in Chapter 8).
* The Buddy system allocators are initialized by invoking the page_alloc_init() and mem_init() functions (see the section “The Buddy System Algorithm” in Chapter 8).
* The final initialization of the IDT is performed by invoking trap_init( ) (see the
section “Exception Handling” in Chapter 4) and init_IRQ( ) (see the section
“IRQ data structures” in Chapter 4).
* The TASKLET_SOFTIRQ and HI_SOFTIRQ are initialized by invoking the softirq_
init() function (see the section “Softirqs” in Chapter 4).
* The system date and time are initialized by the time_init( ) function (see the section “The Linux Timekeeping Architecture” in Chapter 6).
* The slab allocator is initialized by the kmem_cache_init( ) function (see the section “General and Specific Caches” in Chapter 8).
* The speed of the CPU clock is determined by invoking the calibrate_delay() function (see the section “Delay Functions” in Chapter 6).
* The kernel thread for process 1 is created by invoking the kernel_thread( ) function.

In turn, this kernel thread creates the other kernel threads and executes the
/sbin/init program, as described in the section “Kernel Threads” in Chapter 3.
Besides the “Linux version 2.6.11...” message, which is displayed right after the
beginning of start_kernel( ), many other messages are displayed in this last phase,
both by the init program and by the kernel threads. At the end, the familiar login
prompt appears on the console (or in the graphical screen, if the X Window System
is launched at startup), telling the user that the Linux kernel is up and running.

From: Understanding the linux kernel. 
