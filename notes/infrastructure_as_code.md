## Infrastructure as Code

If you have ever spent hours manually configuring Linux servers, installing packages one by one, editing configuration files by hand, and then trying to remember exactly what you did when it is time to set up the next server, you already understand the problem that Infrastructure as Code solves. Infrastructure as Code, or IaC, is the practice of managing and provisioning computing infrastructure through machine-readable definition files rather than through interactive configuration tools or physical hardware configuration. Instead of logging into servers and running commands by hand, you describe your desired infrastructure in code, and tools take care of making it happen.

Think of it this way: all the Linux administration skills you have built, managing packages, configuring services, setting up firewalls, creating users, are still essential. IaC simply gives you a repeatable, version-controlled, and automated way to apply those skills across one server or a thousand.

```
+----------------------------------------------------------------------+
|                     Traditional Manual Approach                      |
+----------------------------------------------------------------------+
|                                                                      |
|   Admin SSH's into Server A ----> Runs commands manually             |
|   Admin SSH's into Server B ----> Runs commands manually             |
|   Admin SSH's into Server C ----> Runs commands manually             |
|                                                                      |
|   Problem: Inconsistent configs, no audit trail, hard to scale       |
+----------------------------------------------------------------------+

+----------------------------------------------------------------------+
|                   Infrastructure as Code Approach                    |
+----------------------------------------------------------------------+
|                                                                      |
|   Admin writes code -----> IaC Tool -----> Server A (configured)     |
|         (one file)            |  |                                    |
|                               |  +-------> Server B (configured)     |
|                               |                                      |
|                               +----------> Server C (configured)     |
|                                                                      |
|   Benefit: Consistent configs, version controlled, scales easily     |
+----------------------------------------------------------------------+
```

### Core Principles of IaC

Before diving into specific tools, it helps to understand the foundational ideas that make IaC effective. These principles guide how every major IaC tool is designed and how you should think about writing infrastructure code.

#### Idempotency

An operation is idempotent if running it once produces the same result as running it multiple times. This is critical in IaC because you want to be able to apply your configuration repeatedly without causing unintended side effects. If your code says "ensure nginx is installed," it should not fail or reinstall nginx if it is already present. It should simply verify the desired state and move on.

#### Declarative vs Imperative

There are two broad approaches to writing IaC:

| Approach | Description | Example |
|---|---|---|
| **Declarative** | You describe the desired end state, and the tool figures out how to achieve it. | "There should be 3 web servers running nginx." |
| **Imperative** | You describe the exact steps to take in order. | "Create a VM, install nginx, start the service, repeat 2 more times." |

Most modern IaC tools lean declarative because it is easier to reason about and the tool handles the complexity of determining what changes are needed.

#### Version Control

IaC files are plain text, which means they belong in a version control system like Git. This gives you a full history of every infrastructure change, the ability to review changes before applying them, and the power to roll back if something goes wrong. Treat your infrastructure definitions with the same care you would give application source code.

#### Immutable Infrastructure

With immutable infrastructure, rather than updating a running server in place, you replace it entirely with a new one built from the latest code. This eliminates configuration drift, where servers slowly become different from each other over time due to manual patches and tweaks.

```
+----------------------------------------------------------------------+
|                        IaC Workflow Overview                         |
+----------------------------------------------------------------------+
|                                                                      |
|   +----------+     +-----------+     +----------+     +----------+   |
|   |  Write   |---->|  Version  |---->|  Review  |---->|  Apply   |   |
|   |   Code   |     |  Control  |     |  & Test  |     | (Deploy) |   |
|   +----------+     +-----------+     +----------+     +----------+   |
|        |                                                    |        |
|        |                                                    v        |
|        |                                            +----------+     |
|        +<------- Iterate on failures <--------------|  Verify  |     |
|                                                     +----------+     |
|                                                                      |
+----------------------------------------------------------------------+
```

### Configuration Management with Ansible

Ansible is one of the most popular IaC tools for configuration management, and it is especially friendly to Linux administrators because it works over SSH. There is no agent to install on your target machines, which means you can start using Ansible with your existing infrastructure immediately.

#### How Ansible Works

Ansible follows an agentless, push-based architecture. You run Ansible from a control node (your workstation or a dedicated management server), and it connects to your managed nodes over SSH, pushes small programs called modules, executes them, and then removes them.

```
+----------------------------------------------------------------------+
|                      Ansible Architecture                            |
+----------------------------------------------------------------------+
|                                                                      |
|   +------------------+         SSH          +------------------+     |
|   |                  |--------------------->|  Managed Node A  |     |
|   |   Control Node   |--------------------->|  Managed Node B  |     |
|   |  (runs Ansible)  |--------------------->|  Managed Node C  |     |
|   |                  |                      +------------------+     |
|   +------------------+                                               |
|          |                                                           |
|          v                                                           |
|   +------------------+                                               |
|   |    Inventory     |  Defines which hosts belong to which groups   |
|   |    Playbooks     |  Defines what configuration to apply          |
|   |    Roles         |  Reusable bundles of tasks                    |
|   +------------------+                                               |
|                                                                      |
+----------------------------------------------------------------------+
```

#### Inventory Files

The inventory file tells Ansible which machines to manage. At its simplest, it is a list of hostnames or IP addresses, but you can organize hosts into groups for easier management.

```ini
# /etc/ansible/hosts or a custom inventory file

[webservers]
web1.example.com
web2.example.com
192.168.1.50

[dbservers]
db1.example.com
db2.example.com

[loadbalancers]
lb1.example.com

[production:children]
webservers
dbservers
loadbalancers
```

You can also use a dynamic inventory that queries a cloud provider's API to automatically discover your hosts, which becomes essential as your infrastructure grows.

#### Playbook Syntax

Playbooks are YAML files that describe the desired state of your systems. Each playbook contains one or more plays, and each play targets a group of hosts and defines a list of tasks.

```yaml
---
- name: Configure web servers
  hosts: webservers
  become: yes

  vars:
    http_port: 80
    doc_root: /var/www/html

  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
        update_cache: yes

    - name: Start and enable nginx
      service:
        name: nginx
        state: started
        enabled: yes

    - name: Deploy index page
      copy:
        content: "<h1>Managed by Ansible</h1>"
        dest: "{{ doc_root }}/index.html"
        owner: www-data
        group: www-data
        mode: "0644"
```

#### Common Ansible Modules for Linux Administration

Ansible ships with hundreds of modules that map directly to the Linux administration tasks you already know.

| Module | Purpose | Linux Admin Equivalent |
|---|---|---|
| `apt` / `yum` / `dnf` | Package management | `apt install`, `yum install` |
| `service` / `systemd` | Service management | `systemctl start`, `systemctl enable` |
| `user` | User account management | `useradd`, `usermod` |
| `group` | Group management | `groupadd`, `groupmod` |
| `copy` | Copy files to remote hosts | `scp`, manual file editing |
| `template` | Deploy Jinja2 templates | Editing config files by hand |
| `file` | Manage file properties | `chmod`, `chown`, `mkdir` |
| `firewalld` / `ufw` | Firewall management | `firewall-cmd`, `ufw` commands |
| `cron` | Manage cron jobs | Editing crontabs manually |
| `lineinfile` | Ensure a line exists in a file | `sed`, manual editing |

### Ansible Practical Examples

The real power of Ansible becomes clear when you see how it handles tasks you would normally do by hand across multiple servers.

#### Managing Packages and Services

This playbook installs a LAMP stack on your web servers, tying together concepts from [package management](./package_managers.md) and [services](./services.md):

```yaml
---
- name: Deploy LAMP stack
  hosts: webservers
  become: yes

  tasks:
    - name: Install Apache, MariaDB, and PHP
      apt:
        name:
          - apache2
          - mariadb-server
          - php
          - php-mysql
          - libapache2-mod-php
        state: present
        update_cache: yes

    - name: Ensure Apache is running and enabled
      service:
        name: apache2
        state: started
        enabled: yes

    - name: Ensure MariaDB is running and enabled
      service:
        name: mariadb
        state: started
        enabled: yes
```

#### Configuring Firewalls

If you have worked through the [firewall notes](./firewalls.md), you know the importance of controlling network traffic. Ansible can manage firewall rules consistently across all your servers:

```yaml
---
- name: Configure firewall rules
  hosts: webservers
  become: yes

  tasks:
    - name: Install firewalld
      apt:
        name: firewalld
        state: present

    - name: Start and enable firewalld
      service:
        name: firewalld
        state: started
        enabled: yes

    - name: Allow HTTP traffic
      firewalld:
        service: http
        permanent: yes
        state: enabled
        immediate: yes

    - name: Allow HTTPS traffic
      firewalld:
        service: https
        permanent: yes
        state: enabled
        immediate: yes

    - name: Allow SSH traffic
      firewalld:
        service: ssh
        permanent: yes
        state: enabled
        immediate: yes

    - name: Deny all other incoming traffic
      firewalld:
        zone: public
        state: enabled
        permanent: yes
        immediate: yes
```

#### Managing Users and Groups

User management, a topic covered in [managing users](./managing_users.md), becomes much simpler when done through code. This playbook creates developer accounts with proper group memberships and SSH keys:

```yaml
---
- name: Manage developer accounts
  hosts: all
  become: yes

  vars:
    developers:
      - name: alice
        uid: 1050
        groups: "developers,sudo"
        ssh_key: "ssh-rsa AAAAB3... alice@workstation"
      - name: bob
        uid: 1051
        groups: "developers"
        ssh_key: "ssh-rsa AAAAB3... bob@workstation"

  tasks:
    - name: Create developers group
      group:
        name: developers
        state: present

    - name: Create user accounts
      user:
        name: "{{ item.name }}"
        uid: "{{ item.uid }}"
        groups: "{{ item.groups }}"
        shell: /bin/bash
        create_home: yes
        state: present
      loop: "{{ developers }}"

    - name: Deploy SSH authorized keys
      authorized_key:
        user: "{{ item.name }}"
        key: "{{ item.ssh_key }}"
        state: present
      loop: "{{ developers }}"

    - name: Set password expiration policy
      command: "chage -M 90 -W 14 {{ item.name }}"
      loop: "{{ developers }}"
      changed_when: false
```

#### Running Playbooks

Once your playbook is written, executing it is straightforward:

```bash
# Run a playbook against the default inventory
ansible-playbook site.yml

# Run against a specific inventory file
ansible-playbook -i production_hosts site.yml

# Run with a specific user and ask for the sudo password
ansible-playbook -i hosts site.yml -u admin --ask-become-pass

# Dry run to see what would change without making changes
ansible-playbook site.yml --check --diff

# Limit execution to a specific group or host
ansible-playbook site.yml --limit webservers
```

### Infrastructure Provisioning with Terraform

While Ansible excels at configuring existing servers, Terraform is designed to provision the infrastructure itself, creating virtual machines, networks, storage, and other cloud resources. Terraform uses a declarative language called HCL (HashiCorp Configuration Language) to describe what resources you need.

```
+----------------------------------------------------------------------+
|                     Terraform Workflow                                |
+----------------------------------------------------------------------+
|                                                                      |
|   +----------+     +----------+     +----------+     +----------+    |
|   |  Write   |---->|   Init   |---->|   Plan   |---->|  Apply   |    |
|   |  .tf     |     | download |     | preview  |     | create/  |    |
|   |  files   |     | providers|     | changes  |     | update   |    |
|   +----------+     +----------+     +----------+     +----------+    |
|                                                            |         |
|                                                            v         |
|                                                     +----------+     |
|                                                     |  State   |     |
|                                                     |  File    |     |
|                                                     | (.tfstate)|    |
|                                                     +----------+     |
|                                                                      |
+----------------------------------------------------------------------+
```

#### Providers

Providers are plugins that let Terraform interact with cloud platforms, SaaS providers, and other APIs. Each provider adds a set of resource types and data sources that Terraform can manage.

```hcl
# Configure the AWS provider
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.5.0"
}

provider "aws" {
  region = "us-east-1"
}
```

#### Resources and Data Sources

Resources are the most important element in Terraform. Each resource block describes one or more infrastructure objects, such as a virtual machine, a network interface, or a DNS record.

```hcl
# Create a VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "production-vpc"
    Environment = "production"
  }
}

# Create a subnet within the VPC
resource "aws_subnet" "web" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "web-subnet"
  }
}
```

#### State Management

Terraform keeps track of the real-world resources it manages in a state file. This file maps the resources defined in your configuration to the actual objects in your infrastructure. For team environments, storing state remotely is essential.

```hcl
# Configure remote state storage
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "production/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

🔴 **Caution**: The state file can contain sensitive information such as database passwords and API keys. Always store it securely and never commit it to a public Git repository.

### Terraform Practical Examples

#### Creating a Web Server Instance

This example provisions an EC2 instance configured as a web server, pulling together networking and compute concepts:

```hcl
# Security group allowing HTTP, HTTPS, and SSH
resource "aws_security_group" "web_sg" {
  name        = "web-server-sg"
  description = "Allow web and SSH traffic"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 instance for the web server
resource "aws_instance" "web" {
  ami                    = "ami-0c55b159cbfafe1f0"
  instance_type          = "t3.micro"
  subnet_id              = aws_subnet.web.id
  vpc_security_group_ids = [aws_security_group.web_sg.id]
  key_name               = "my-ssh-key"

  user_data = <<-EOF
    #!/bin/bash
    apt-get update
    apt-get install -y nginx
    systemctl start nginx
    systemctl enable nginx
  EOF

  tags = {
    Name        = "web-server-01"
    ManagedBy   = "terraform"
  }
}
```

#### Output Variables

Outputs let you extract useful information from your Terraform-managed infrastructure:

```hcl
output "web_server_public_ip" {
  description = "Public IP address of the web server"
  value       = aws_instance.web.public_ip
}

output "vpc_id" {
  description = "ID of the production VPC"
  value       = aws_vpc.main.id
}
```

After running `terraform apply`, you can view outputs and manage the lifecycle:

```bash
# Initialize, plan, and apply
terraform init
terraform plan
terraform apply

# View outputs after deployment
terraform output web_server_public_ip

# Destroy all resources when no longer needed
terraform destroy
```

### Comparison of IaC Tools

Different tools serve different purposes, and many organizations use more than one. Here is how the major IaC tools compare:

| Feature | Ansible | Terraform | Puppet | Chef | SaltStack |
|---|---|---|---|---|---|
| **Primary Use** | Configuration management | Infrastructure provisioning | Configuration management | Configuration management | Configuration management |
| **Language** | YAML (playbooks) | HCL | Puppet DSL (Ruby-based) | Ruby DSL | YAML / Jinja2 |
| **Approach** | Declarative + Imperative | Declarative | Declarative | Imperative | Declarative + Imperative |
| **Architecture** | Agentless (SSH) | Agentless (API calls) | Agent-based | Agent-based | Agent or agentless |
| **State Management** | Stateless | Stateful (.tfstate) | Stateful (PuppetDB) | Stateful (Chef Server) | Stateful (Salt Mine) |
| **Learning Curve** | Low | Medium | High | High | Medium |
| **Best For** | Server config, app deployment | Cloud resource provisioning | Large enterprise environments | Complex application configs | Event-driven automation |
| **Idempotent** | Yes (most modules) | Yes | Yes | Yes (with care) | Yes |
| **Community** | Very large | Very large | Large | Medium | Medium |

A common pattern in production environments is to use Terraform to provision the infrastructure and Ansible to configure the software on those machines.

### IaC Best Practices

#### Use Version Control for Everything

Every piece of your infrastructure code should live in a Git repository. This includes playbooks, Terraform configurations, variable files, and documentation. Use branching strategies and pull requests to review infrastructure changes before they are applied.

```
+----------------------------------------------------------------------+
|                   Git-Based IaC Workflow                              |
+----------------------------------------------------------------------+
|                                                                      |
|   +----------+     +----------+     +----------+     +----------+    |
|   | Feature  |---->|  Pull    |---->|  CI/CD   |---->|  Merge   |    |
|   | Branch   |     | Request  |     |  Tests   |     | & Deploy |    |
|   +----------+     +----------+     +----------+     +----------+    |
|                         |                |                            |
|                         v                v                            |
|                    Peer Review     Lint + Validate                    |
|                    of changes      + Dry Run                         |
|                                                                      |
+----------------------------------------------------------------------+
```

#### Write Modular, Reusable Code

Break your infrastructure code into small, reusable components. In Ansible, this means using roles. In Terraform, this means using modules. Modularity makes your code easier to test, maintain, and share across projects.

```
project/
├── ansible/
│   ├── site.yml
│   ├── inventory/
│   │   ├── production
│   │   └── staging
│   └── roles/
│       ├── common/
│       ├── webserver/
│       └── database/
├── terraform/
│   ├── modules/
│   │   ├── networking/
│   │   └── compute/
│   ├── environments/
│   │   ├── production/
│   │   └── staging/
│   └── main.tf
└── README.md
```

#### Manage Secrets Securely

Never store passwords, API keys, or certificates in plain text within your IaC files.
I. Use Ansible Vault for encrypting sensitive variables:

```bash
# Encrypt a variables file
ansible-vault encrypt group_vars/production/secrets.yml

# Run a playbook that uses encrypted variables
ansible-playbook site.yml --ask-vault-pass
```

II. Use environment variables or a secrets manager for Terraform:

```hcl
# Reference a variable without hardcoding the value
variable "db_password" {
  description = "Database administrator password"
  type        = string
  sensitive   = true
}

resource "aws_db_instance" "main" {
  engine         = "mysql"
  instance_class = "db.t3.micro"
  username       = "admin"
  password       = var.db_password
}
```

```bash
# Pass the secret at runtime
export TF_VAR_db_password="secure-password-from-vault"
terraform apply
```

#### Test Your Infrastructure Code

Just as you test application code, you should test infrastructure code before deploying to production.

| Testing Level | Tool | Purpose |
|---|---|---|
| Syntax checking | `ansible-playbook --syntax-check`, `terraform validate` | Catch typos and syntax errors |
| Linting | `ansible-lint`, `tflint` | Enforce best practices and style |
| Dry runs | `ansible-playbook --check`, `terraform plan` | Preview changes without applying |
| Integration testing | Molecule, Terratest | Verify behavior in real environments |
| Compliance testing | InSpec, Open Policy Agent | Ensure security and policy compliance |

### Integrating IaC with Linux Administration

Your existing skills are the foundation. The table below shows how common tasks translate directly into IaC:

| Linux Admin Task | Manual Approach | Ansible Equivalent | Terraform Equivalent |
|---|---|---|---|
| Install packages | `apt install nginx` | `apt` module with `state: present` | `user_data` script in instance resource |
| Manage services | `systemctl enable nginx` | `service` module with `enabled: yes` | Cloud-init or provisioner scripts |
| Configure firewall | `ufw allow 80/tcp` | `ufw` module with `rule: allow` | Security group resource |
| Create users | `useradd -m alice` | `user` module with `state: present` | IAM user resource (cloud level) |
| Edit config files | `vim /etc/nginx/nginx.conf` | `template` module with Jinja2 | N/A (configuration management domain) |
| Set up cron jobs | `crontab -e` | `cron` module | CloudWatch Events / scheduled tasks |
| Manage disk mounts | `mount /dev/sdb1 /data` | `mount` module | EBS volume + attachment resources |
| Configure networking | `ip addr add ...` | `nmcli` or `template` for config files | VPC, subnet, and ENI resources |

The key insight is that Ansible automates the same commands you would run manually, while Terraform operates at a higher level, creating the machines and networks those commands run on.

When building your IaC practice, start with what you know:

I. Take a server you have configured manually and write an Ansible playbook that reproduces that configuration from scratch.

II. Document every manual step you perform during a server setup, then translate each step into a task in a playbook.

III. Use `ansible-playbook --check --diff` to verify that your playbook matches the current state of a manually configured server.

IV. Gradually move from configuring existing servers to provisioning new ones with Terraform and configuring them with Ansible in a single automated pipeline.

### Challenges

1. Install Ansible on your local machine and create an inventory file that groups at least three virtual machines (or containers) into two groups called `webservers` and `dbservers`. Run the `ansible all -m ping` command to verify connectivity to all hosts and troubleshoot any connection failures.

2. Write an Ansible playbook that installs a web server package (such as nginx or Apache) on all hosts in the `webservers` group, ensures the service is running and enabled at boot, and deploys a custom `index.html` file. Run the playbook and verify the result by accessing the web server in a browser or with `curl`.

3. Create an Ansible playbook that configures firewall rules on your servers, allowing HTTP (port 80), HTTPS (port 443), and SSH (port 22) traffic while blocking all other incoming connections. Test the rules by attempting to connect on both allowed and blocked ports.

4. Write an Ansible playbook that creates three user accounts, each belonging to a shared `developers` group and having their own SSH public key deployed to `~/.ssh/authorized_keys`. Run the playbook twice and confirm that the second run reports no changes, demonstrating idempotency.

5. Install Terraform and write a configuration that provisions a single virtual machine (using any cloud provider or a local provider like `libvirt`). Include a VPC or network resource, a security group that allows SSH access, and an output that displays the instance's IP address after creation. Run `terraform plan` to review the execution plan before applying.

6. Extend your Terraform configuration to create two web server instances behind a simple network setup with separate subnets. Use variables for the instance type and region so the same configuration can be reused across environments. Run `terraform apply` and then `terraform destroy` to verify the full lifecycle.

7. Take a server you have previously configured manually and write an Ansible playbook that reproduces the entire setup from a fresh base image. Include package installation, service configuration, user creation, firewall rules, and any custom configuration files. Run the playbook against a clean server and compare the result to the original.

8. Set up a project directory following the modular structure described in the best practices section, with separate Ansible roles for a web server, a database server, and a common baseline configuration. Each role should handle its own packages, services, configuration files, and firewall rules. Write a `site.yml` that applies the appropriate roles to each host group.

9. Create an Ansible Vault-encrypted file containing sensitive variables (such as a database password and an API key) and write a playbook that references those variables. Run the playbook using `--ask-vault-pass` and verify that the secrets are never displayed in the playbook output. Then try running the playbook without the vault password to confirm it fails securely.

10. Build a complete IaC pipeline that uses Terraform to provision a virtual machine and then uses Ansible to configure it, combining both tools in a single workflow. The Terraform output should generate an Ansible inventory file dynamically, and the Ansible playbook should install and configure a web server with a firewall. Document each step and verify the end-to-end process by accessing the deployed web application.
