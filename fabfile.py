from fabric.api import task, run, sudo, put, cd
from fabric.contrib.files import exists
from fabric.context_managers import shell_env


BINARY_DOWNLOAD_SERVER="http://archive.freedomfone.org/installer_1204"


@task
def copy_public_key():
    """Copy your rsa public key from ~/.ssh/id_rsa.pub to the remote server.
    """
    put(local_path="~/.ssh/id_rsa.pub", remote_path="~/id_rsa.pub")
    sudo("mkdir -p ~/.ssh")
    sudo("cat ~/id_rsa.pub >> ~/.ssh/authorized_keys")
    sudo("chmod -R 600 ~/.ssh")
    sudo("rm ~/id_rsa.pub")


@task
def deploy(vcs="git"):
    """Deploy a Freedom Fone instance to a clean installation of Ubuntu 12.04.

    This *might* work in a non clean install, but it was only tested
    against fresh installations of 12.04. Right now it depends on some
    binary packages that are only compiled for 12.04, so other Ubuntu
    versions will most likely not work properly.
    """
    install_deps()

    sudo("mkdir -p /opt/freedomfone")
    

    with cd("/opt/freedomfone"):
        if vcs == "git":
            if not exists("/opt/freedomfone/.git"):
                sudo("git clone -b 2.S.5 https://github.com/freedomfone/freedomfone.git .")
        else:
            sudo("svn co https://dev.freedomfone.org/svn/freedomfone/branches/3.0/ .")

        sudo("mkdir -p /opt/freedomfone/packages")
        
        with cd("packages"):
            install_cepstral()
            install_freeswitch()

        with cd("esl/lib"):
            sudo("sh install.ESL.sh")

        # Configs
        with cd("rootconf_1204"):
            sudo("cp bin/setmixers /bin/")
            sudo("cp -r etc/* /etc/")
            sudo("cp -r opt/freeswitch /opt/")

        # Fix permissions for runnable scripts
        sudo("chmod 0755 /etc/init.d/freeswitch")
        sudo("chmod 0755 /etc/init.d/dispatcher_in")
        sudo("chmod 0755 /etc/init.d/iwatch")
        sudo("chmod 0755 /etc/init.d/gsmopen")

        sudo("a2enmod rewrite")
        sudo("a2dissite default")
        sudo("a2ensite freedomfone")

        # Configure DB
        sudo("service mysql restart")
        sudo("sh db_install.sh")

        sudo("sh fix_perms_all.sh")

        sudo("service apache2 reload")
        sudo("service cron restart")

        # Interface Aliasing for OfficeRoute
        sudo("/sbin/ifconfig eth0:0 192.168.1.250 netmask 255.255.255.0 up")
        sudo("service gsmopen start")

        sudo("service freeswitch start")
        sudo("service gsmopen reload")
        sudo("service dispatcher_in start")


@task
def install_demo_data():
    """Installs a voice menu and leave a message service for testing and demo.
    """
    with cd("/opt/freedomfone"):
        sudo("sh demo_install.sh")


def install_deps():
    sudo("apt-get update")

    # Avoid prompt for mysql and postfix
    with shell_env(DEBIAN_FRONTEND="noninteractive"):
        sudo("apt-get install -y {0}".format(" ".join(DEPENDENCIES)))


def install_cepstral():
    CEPSTRAL="Cepstral_Allison-8kHz_i386-linux_5.1.0"
    sudo("wget -nc {0}/{1}.tar.gz".format(BINARY_DOWNLOAD_SERVER, CEPSTRAL))
    sudo("tar zxvf {0}.tar.gz".format(CEPSTRAL))
    with cd(CEPSTRAL):
        sudo("sh install.sh agree /opt/swift")


def install_freeswitch():
    BUILD="1.2~ffrc3-1_i386"

    all_urls = ["{0}/{1}_{2}.deb".format(BINARY_DOWNLOAD_SERVER, package, BUILD)
                for package in FREESWITCH_BINARIES]
    all_debs = ["{0}*deb".format(package) for package in FREESWITCH_BINARIES]

    sudo("wget -nc {0}".format(" ".join(all_urls)))
    sudo("dpkg -i {0}".format(" ".join(all_debs)))


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
    "libgsmme1c2a",
    "libnspr4",
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

FREESWITCH_BINARIES = [
    "libctb",
    "libfreeswitch1",
    "libjs1",

    "freeswitch",
    "freeswitch-mod-amr",
    "freeswitch-mod-amrwb",
    "freeswitch-mod-cdr-csv",
    "freeswitch-mod-cepstral",
    "freeswitch-mod-cluechoo",
    "freeswitch-mod-codec2",
    "freeswitch-mod-commands",
    "freeswitch-mod-conference",
    "freeswitch-mod-console",
    "freeswitch-mod-dialplan-asterisk",
    "freeswitch-mod-dialplan-directory",
    "freeswitch-mod-dialplan-xml",
    "freeswitch-mod-dingaling",
    "freeswitch-mod-directory",
    "freeswitch-mod-distributor",
    "freeswitch-mod-dptools",
    "freeswitch-mod-enum",
    "freeswitch-mod-esf",
    "freeswitch-mod-event-socket",
    "freeswitch-mod-expr",
    "freeswitch-mod-fifo",
    "freeswitch-mod-fsv",
    "freeswitch-mod-g723-1",
    "freeswitch-mod-g729",
    "freeswitch-mod-gsmopen",
    "freeswitch-mod-h26x",
    "freeswitch-mod-local-stream",
    "freeswitch-mod-logfile",
    "freeswitch-mod-loopback",
    "freeswitch-mod-lua",
    "freeswitch-mod-native-file",
    "freeswitch-mod-say-en",
    "freeswitch-mod-say-ru",
    "freeswitch-mod-sndfile",
    "freeswitch-mod-sofia",
    "freeswitch-mod-speex",
    "freeswitch-mod-spidermonkey",
    "freeswitch-mod-tone-stream",
    "freeswitch-mod-voicemail",
    "freeswitch-mod-voicemail-ivr",
    "freeswitch-mod-xml-curl",
]
