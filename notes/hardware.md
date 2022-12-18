In Linux, there are several commands that can be used to check hardware information. In general, these commands can be divided into two categories:
Information about the internal hardware

* `lsusb`: displays a list of the USB devices that are connected to the system. It shows the vendor and product ID of each device, as well as its manufacturer and product name.
* `lspci`: displays a list of the PCI devices that are connected to the system. It shows the vendor and device ID of each device, as well as its class and function.
* `lsdev`: displays a list of the devices that are known to the system. It shows the device type, device name, and device driver for each device.
* `lsblk`: displays a list of the block devices that are connected to the system. It shows the device name, size, and type for each device.
* `lscpu`: displays information about the CPU in the system. It shows the processor architecture, number of CPUs, number of cores, and other information.

Information about the plugged devices

* `dmesg`: displays the kernel ring buffer, which contains messages from the kernel and device drivers. It can be used to view information about plugged devices, as well as other system events.

These are just a few of the many commands that can be used to check hardware information in Linux. To learn more about these commands and their options, you can consult the man pages or use the `--help` option.
