## Virtualization

primarily KVM, also need to know the types of virtualization and other technologies;

## Networking

* VMs on the same host talking to each other.
* VMs accessing external services.
* External services acessing VM.

### NAT

VMs can talk to outside world trough the host .
External services can access VMs using the address translation.

The disadvantage of NAT-based networking is that your guest VM is concealed behind the NAT bridge and is inaccessible outside of the hypervisor server unless you use complicated port forwarding or IP masquerading.

### Bridge

An extension of LAN network.
The physical interface of the VM host connects the virtual interface of your VM to the outside of local network.
The DHCP server on the bridged local network assigns an IP address to the VM.

Any device on the LAN can see and access the VMs.

### Host only

Outside devices are inaccessible to VMs.

Connection to the internet is only accessible trough port forwarding from the host (mapping a port from the host to port on the guest).

## VirtualBox


### Runing VMs from the terminal

1. You need to install VirtualBox Extension Pack:

        wget http://download.virtualbox.org/virtualbox/4.2.36/Oracle_VM_VirtualBox_Extension_Pack-4.2.36-104064a.vbox-extpack
        sudo VBoxManage extpack install ./Oracle_VM_VirtualBox_Extension_Pack-4.2.36-104064a.vbox-extpack
        
2. To create a Virtual Machine called "vm_example", use:

        VBoxManage createvm --name "vm_example" --register

3. Let's choose standard configurations for an Ubuntu machine (1024 Mb of memeory, bridged network and so on):

        VBoxManage modifyvm "vm_example" --memory 1024 --acpi on --boot1 dvd --nic1 bridged --bridgeadapter1 eth0 --ostype Ubuntu

4. We need to give some disk space to our VM (15GB = 15000MB):

        VBoxManage createvdi --filename ~/VirtualBox VMs/vm_example/vm_example.vdi --size 15000

5. Lastly we need to load an existing Ubuntu .iso file (in the example below located at *~/Downloads/ubuntu-24.02.1.iso*

        VBoxManage storagectl "vm_example" --name "IDE Controller" --add ide
        VBoxManage storageattach "vm_example" --storagectl "IDE Controller" --port 0 --device 0 --type hdd --medium ~/VirtualBox VMs/vm_example/vm_example.vdi
        VBoxManage storageattach "vm_example" --storagectl "IDE Controller" --port 1 --device 0 --type dvddrive --medium ~/Downloads/ubuntu-24.02.1.iso

6. To start the VM, we simply use:

        VBoxHeadless --startvm "vm_example" &

## VMware

### The IP address of a VM

If you are using NAT networking, you will find the IP address in the following special file:

        cat /etc/vmware/vmnet8/dhcpd/dhcpd.leases

The MAC address of the VM is required for a bridged network. You can retrive it from VMs .vmx file:

        cat path/to/example_vm.vmx

Suppose you found the following MAC address: 01:1a:bb:32:12:99.
You can now use it to find the IP address of a VM:

        dhcpdump -i eth0 -h ^01:1a:bb:32:12:99

## KVM

### The IP address of a VM

If you're using NAT networking, you'll need to specify the network name (the default is simply *default*): 

        virsh net-dhcp-leases default

The name of the bridge is required for a bridged network.
If your bridge is called *bridge1*, you can obtain the IP address of a VM by the following command: 

        dhcpdump -i eth0 -h ^00:0c:29:bd:81:01
