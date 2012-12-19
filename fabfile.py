from fabric.api import task, run, put, cd
from fabric.context_managers import shell_env


@task
def copy_public_key():
    put(local_path="~/.ssh/id_rsa.pub", remote_path="~/id_rsa.pub")
    run("mkdir -p ~/.ssh")
    run("cat ~/id_rsa.pub >> ~/.ssh/authorized_keys")
    run("chmod -R 600 ~/.ssh")
    run("rm ~/id_rsa.pub")


@task
def deploy():
    install_deps()

    run("mkdir -p /opt/freedomfone")
    with cd("/opt/freedomfone"):
        run("svn co https://dev.freedomfone.org/svn/freedomfone/branches/3.0/ .")

        run("sh download_bin_1204.sh")
        with cd("packages"):
            # Install Cepstral
            run("tar zxvf Cepstral_Allison-8kHz_i386-linux_5.1.0.tar.gz")
            with cd("Cepstral_Allison-8kHz_i386-linux_5.1.0"):
                run("sh install.sh agree /opt/swift")

            # Install freeswitch
            run("sh install_fs_1204.sh")

        # Configs
        with cd("rootconf_1204"):
            run("cp bin/setmixers /bin/")
            run("cp -r etc/* /etc/")
            run("cp -r opt/freeswitch /opt/")

        # Fix permissions for runnable scripts
        run("chmod 0755 /etc/init.d/freeswitch")
        run("chmod 0755 /etc/init.d/dispatcher_in")
        run("chmod 0755 /etc/init.d/iwatch")
        run("chmod 0755 /etc/init.d/gsmopen")

        run("a2enmod rewrite")
        run("a2dissite default")
        run("a2ensite freedomfone")

        with cd("esl/lib"):
            run("sh install.ESL.sh")

        # Configure DB
        run("service mysql restart")
        run("sh db_install.sh")

        run("sh fix_perms_all.sh")

        run("service apache2 reload")
        run("service cron restart")

        # Interface Aliasing for OfficeRoute
        run("/sbin/ifconfig eth0:0 192.168.1.250 netmask 255.255.255.0 up")
        run("service gsmopen start")

        run("service freeswitch start")
        run("service gsmopen reload")
        run("service dispatcher_in start")


@task
def install_demo_data():
    with cd("/opt/freedomfone"):
        run("sh demo_install.sh")


def install_deps():
    run("apt-get update")

    # Avoid prompt for mysql and postfix
    with shell_env(DEBIAN_FRONTEND="noninteractive"):
        run("apt-get install -y {0}".format(" ".join(DEPENDENCIES)))

DEPENDENCIES = [
    "apache2",
    "bsd-mailx",
    "gammu",
    "gammu-smsd",
    "gettext",
    "iwatch",
    "lame",
    "libapache2-mod-php5",
    "libssl0.9.8",
    "mp3info",
    "mysql-server",
    "php5",
    "php5-cli",
    "php5-curl",
    "php5-mysql",
    "php5-snmp",
    "php5-xsl",
    "sox",
    "subversion",
    "wget",
]
