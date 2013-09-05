Freedom Fone Deployment Scripts
===============================

These project provides an automated deployment script for
[Freedom Fone](http://freedomfone.org) version 2S4, that uses
[Fabric](http://fabfile.org). There's also a
[Vagrantfile](http://vagrantup.com) to easily setup a local VM with
Ubuntu 12.04 to ease the setup of a local Freedom Fone installation.

How to deploy
-------------

For the deployment script you'll need Python (preferably 2.7, but
might work with older versions) and Fabric 1.5. The
[Python language website](http://python.org) have installation
instructions for multiple operating systems. Mac OS X and many Linux
flavors already come with Python pre-installed. On Ubuntu 12.04 open 
the command terminal and enter the following commands;

    $apt-get install python-setuptools

This should install all the required python utilities

    $apt-get install git

Installs the git utilities required fro pulling the source code
from the repository

    apt-get install openssh-server
    
Installs ssh.
Check to see if python has been installed using the command below

    $ python --version

in a terminal.

To install fabric, first get [pip](http://www.pip-installer.org) by
doing

    $ easy_install pip
    
After that you can just

    $ pip install fabric

After you have Fabric installed, clone this project using Git:

    $ git clone git://github.com/freedomfone/freedomfone-deploy.git
    
and then `cd freedomfone-deploy` to get into this project directory on
the terminal and do

    $ fab --list
    
to see which tasks are available. If it worked fine you should have
seen something like.

    Available commands:

    copy_public_key    Copy your rsa public key from ~/.ssh/id_rsa.pub to the remote server.
    deploy             Deploy a Freedom Fone instance to a clean installation of Ubuntu 12.04.
    install_demo_data  Installs a voice menu and leave a message service for testing and demo.

Fabric runs tasks with a target host that you specify by a command
line parameter. For example, to run `deploy` task in host
`user@12.34.56.78` you'd type

    $ fab deploy -H user@12.34.56.78

That will deploy Freedom Fone to the target machine and by the end of
it should be up and running and accepting calls.

If you want to deploy Freedom Fone to the machine you're in, you can
specify `localhost` on the host parameter.

    $ fab deploy -H user@localhost

Creating a Local VM
-------------------

*This is currently experimental and the deploy task still need some
 testing to make sure it works on a local VM*

### Using Vagrant

Vagrant is a tool that lets you quickly create *headless* (that is,
non GUI, only terminal access) [Virtual Box](http://virtualbox.org)
Virtual Machines from a specification contained in a Vagrantfile. The
advantage is that Vagrantfiles make it easy to share a VM setup that's
appropriate for your project.

To use Vagrant, first you'll need [Virtual Box](http://virtualbox.org)
installed. Download an installer from their website. For Vagrant
itself, you should download a installer from
[their website](http://downloads.vagrantup.com) choosing the latest
version and the package corresponding to your operating system (not
the one you'll install Freedomfone into).

After Vagrant is installed, you should be able to issue `vagrant`
commands from the Terminal. You need to be in the same directory as
the `Vagrantfile`. After it's installed you can issue

    $ vagrant up

on your terminal to create a VM with Ubuntu 12.04 installed. It will
download the base box if necessary. The included `Vagrantfile` is setup
so the created VM is visible from the host machine (that's your
machine) on ip address `11.22.33.44`. That means that after the box is
up and running, you should be able to deploy Freedom Fone to it by
doing

    $ fab deploy -H vagrant@11.22.33.44
    
Refer to the
[Vagrant Getting Started Guide](http://vagrantup.com/v1/docs/getting-started/index.html)
if you need extra help on using it get more information on how to use
it.

### Using VirtualBox, VMWare, etc

You should be able to use any virtualization software to setup a local
Ubuntu 12.04 VM and use Fabric to deploy to it. You just need to make
sure your VM has an ip address that's visible to your host VM so you
can specify on your `fabric deploy -H user@<ip address of VM>`
command. Please refer to the documentation of the software you're
using to find out about this.
