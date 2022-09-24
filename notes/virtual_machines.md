## Virtualization

primarily KVM, also need to know the types of virtualization and other technologies;


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
