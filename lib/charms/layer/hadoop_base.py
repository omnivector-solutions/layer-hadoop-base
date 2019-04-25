import os
from time import sleep
from pathlib import Path
import re

from subprocess import check_call, check_output

from charmhelpers.core.hookenv import resource_get
from charmhelpers.core.templating import render
from charmhelpers.core.host import chownr


HADOOP_HOME = Path('/opt/hadoop')
HADOOP_BIN = HADOOP_HOME / 'bin' / 'hadoop'
HADOOP_CONFIG_DIR = HADOOP_HOME / 'etc' / 'hadoop'
HADOOP_ENV_SH = HADOOP_CONFIG_DIR / 'hadoop-env.sh'
HADOOP_LOG_DIR = Path('/var/log/hadoop')


def provision_hadoop_resource():
    """Unpack the hadoop resource.
    """

    # Provision hadoop resource
    hadoop_tarball = resource_get('hadoop-tarball')

    if not hadoop_tarball:
        return False

    if HADOOP_HOME.exists():
        check_call(['rm', '-rf', str(HADOOP_HOME)])

    check_call(['mkdir', '-p', str(HADOOP_HOME)])

    check_call(
        ['tar', '-xzf', hadoop_tarball, '--strip=1', '-C', str(HADOOP_HOME)])

    while not HADOOP_BIN.exists():
        sleep(1)

    return True


def get_hadoop_version():
    """Return the Hadoop version.
    """

    os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-8-openjdk-amd64/jre'
    output = check_output([str(HADOOP_BIN), 'version'])
    return re.findall(re.compile('Hadoop ([\\d\\.]+)'), str(output))[0]


def hadoop_perms_init():
    """Set hadoop ownership and perms.
    """

    # Set hadoop ownership on the home, log, and work dir
    for directory in [HADOOP_HOME, HADOOP_LOG_DIR]:
        chownr(str(directory), 'hadoop', 'hadoop', chowntopdir=True)


def render_hadoop_init_config(ctxt=None):
    """Render hadoop base initial configs.
    """

    if ctxt:
        context = ctxt
    else:
        context = {}
    # Render the configs
    if HADOOP_ENV_SH.exists():
        HADOOP_ENV_SH.unlink()
    render('hadoop-base-env.sh', str(HADOOP_ENV_SH),
           context=context, perms=0o755)
