## Virtualization

Virtualization is the process of creating a virtual version of a computer, device, or network using software. One type of virtualization is called KVM (Kernel-based Virtual Machine), which allows a single physical server to run multiple virtual machines (VMs). There are several other types of virtualization, including:

1. Hardware-level virtualization
1. Operating system-level virtualization
1. Application virtualization

## Networking in Virtual Environments

Networking in a virtual environment involves setting up communication between VMs on the same host, VMs accessing external services, and external services accessing VMs. There are several options for networking VMs, including:

## NAT (Network Address Translation)

With NAT-based networking, VMs can communicate with the outside world through the host. External services can access VMs using address translation. However, NAT can make it difficult for guest VMs to be accessed outside the hypervisor server unless you use complicated port forwarding or IP masquerading.

## Bridge

A bridged network extends the LAN network and connects the virtual interface of the VM to the outside local network via the physical interface of the host. A DHCP server on the bridged local network assigns an IP address to the VM. Any device on the LAN can access the VMs.

## Host Only

In a host only configuration, VMs are inaccessible to outside devices, but can still access the internet via port forwarding from the host (mapping a port from the host to a port on the guest).

## VirtualBox

VirtualBox is a virtualization software that allows you to create and run virtual machines (VMs) on your computer. To run a VM from the terminal in VirtualBox, you will need to perform the following steps:

1. Install the VirtualBox Extension Pack:

```
wget http://download.virtualbox.org/virtualbox/4.2.36/Oracle_VM_VirtualBox_Extension_Pack-4.2.36-104064a.vbox-extpack
sudo VBoxManage extpack install ./Oracle_VM_VirtualBox_Extension_Pack-4.2.36-104064a.vbox-extpack
```

2. Create a VM with a desired name (in this example, "vm_example"):

```
VBoxManage createvm --name "vm_example" --register
```

3. Configure the VM with desired settings, such as the amount of memory to allocate, the type of network connection to use, and the type of operating system to install:

```
 VBoxManage modifyvm "vm_example" --memory 1024 --acpi on --boot1 dvd --nic1 bridged --bridgeadapter1 eth0 --ostype Ubuntu
```

4. Assign some disk space to the VM:

```
VBoxManage createvdi --filename ~/VirtualBox VMs/vm_example/vm_example.vdi --size 15000
```

5. Load an ISO file containing the operating system you want to install:

```
VBoxManage storagectl "vm_example" --name "IDE Controller" --add ide
VBoxManage storageattach "vm_example" --storagectl "IDE Controller" --port 0 --device 0 --type hdd --medium ~/VirtualBox VMs/vm_example/vm_example.vdi
VBoxManage storageattach "vm_example" --storagectl "IDE Controller" --port 1 --device 0 --type dvddrive --medium ~/Downloads/ubuntu-24.02.1.iso
```

6. To start the VM, we simply use:

```
VBoxHeadless --startvm "vm_example" &
```

## VMware

VMware is another virtualization software that allows you to create and run virtual machines (VMs) on your computer. To find the IP address of a VM in VMware, you will need to follow these steps:

### NAT Networking

If you are using NAT networking, you can find the IP address of the VM in the dhcpd.leases file:

```
cat /etc/vmware/vmnet8/dhcpd/dhcpd.leases
```

### Bridged Networking

To find the IP address of a VM in a bridged network, you will need the MAC address of the VM. You can retrieve the MAC address from the VM's .vmx file:

```
cat path/to/example_vm.vmx
```

Once you have the MAC address (e.g., `01:1a:bb:32:12:99`), you can use it to find the IP address of the VM:

```
dhcpdump -i eth0 -h ^01:1a:bb:32:12:99
```

## KVM

KVM (Kernel-based Virtual Machine) is an open source virtualization software that allows you to create and run virtual machines (VMs) on your computer. To find the IP address of a VM in KVM, you will need to follow these steps:

### NAT Networking

If you are using NAT networking, you can find the IP address of the VM by specifying the network name (the default is default):

```
virsh net-dhcp-leases default
```

### Bridged Networking

To find the IP address of a VM in a bridged network, you will need the name of the bridge and the MAC address of the VM. If your bridge is called bridge1, you can find the IP address of the VM using the following command:

```
dhcpdump -i eth0 -h ^00:0c:29:bd:81:01
```

Replace 00:0c:29:bd:81:01 with the actual MAC address of the VM.
