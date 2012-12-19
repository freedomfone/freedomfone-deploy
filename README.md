freedomfone-deploy
==================

These project provides an automated deployment script for
[Freedom Fone](http://freedomfone.org) that uses
[Fabric](http://fabfile.org). There's also a
[Vagrantfile](http://vagrantup.com) to easily setup a local VM with
Ubuntu 12.04 to ease the setup of a local Freedom Fone installation.

How to deploy
-------------

For the deployment script you'll need Python (preferably 2.7, but
might work with older versions) and Fabric 1.5. The
[Python language website](http://python.org) have installation
instructions for multiple operating systems. Mac OS X and many Linux
flavors already come with Python pre-installed. You can check that by
typing

    $ python --version

in a terminal.

To install fabric, first get [pip](http://www.pip-installer.org) by
doing

    $ easy_install pip
    
After that you can just

    $ pip install fabric

After you have Fabric install, `cd` to this project directory on the
terminal and do

    $ fab --list
    
to see which tasks are available. If it worked fine you should have
seen a few tasks listed along with their description.

Fabric runs tasks with a target host that you specify by a command
line parameter. For example, to run `deploy` task in host
`user@12.34.56.78` you'd type

    $ fab deploy -H user@12.34.56.78

That will deploy Freedom Fone to the target machine and by the end of
it should be up and running and accepting calls.


Creating a Local VM
-------------------

You can create a local VM by installing Vagrant on your machine. First
you'll need [Virtual Box](http://virtualbox.org) installed. For
Vagrant itself, you can download a installer from their website or use
RubyGems

    $ gem install vagrant

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
