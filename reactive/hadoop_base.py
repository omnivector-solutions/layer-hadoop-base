from charms.reactive import (
    when,
    when_not,
    set_flag,
)

from charmhelpers.core.host import (
    adduser,
)

from charmhelpers.core import unitdata

from charmhelpers.core.hookenv import log

from charms.layer import status

from charms.layer.hadoop_base import (
    HADOOP_LOG_DIR,
    get_hadoop_version,
    provision_hadoop_resource,
    hadoop_perms_init,
    render_hadoop_init_config,
)


KV = unitdata.kv()


@when('apt.installed.openjdk-8-jre-headless')
@when_not('hadoop.apt.deps.available')
def hadoop_apt_deps_available():
    """Hadoop deps available.
    """
    set_flag('hadoop.apt.deps.available')


@when_not('hadoop.user.available')
def create_hadoop_user():
    """Create spark user.
    """
    adduser('hadoop', system_user=True)
    set_flag('hadoop.user.available')


@when_not('hadoop.dirs.available')
def create_hadoop_log_dir():
    """Create hadoop log dir.
    """
    if not HADOOP_LOG_DIR.exists():
        HADOOP_LOG_DIR.mkdir(parents=True)
    set_flag('hadoop.dirs.available')


@when('hadoop.apt.deps.available')
@when_not('hadoop.resource.available')
def provision_hadoop():
    """Proivision hadoop resource.
    """
    log("PROVISIONING HADOOP RESOURCE")
    status.maint("PROVISIONING HADOOP RESOURCE")

    hadoop_resource_provisioned = provision_hadoop_resource()

    if not hadoop_resource_provisioned:
        status.blocked("TROUBLE PROVISIONING HADOOP RESOURCE, PLEASE DEBUG")
        log("TROUBLE PROVISIONING HADOOP RESOURCE, PLEASE DEBUG")
        return

    hadoop_version = get_hadoop_version()
    log("HADOOP RESOURCE {} ready".format(hadoop_version))
    status.maint("HADOOP RESOURCE {} ready".format(hadoop_version))

    KV.set('hadoop_version', hadoop_version)
    set_flag('hadoop.resource.available')


@when('hadoop.user.available',
      'hadoop.dirs.available',
      'hadoop.resource.available')
@when_not('hadoop.base.config.available')
def render_hadoop_initial_sane_default_configs():
    render_hadoop_init_config({'hadoop_version': get_hadoop_version()})
    set_flag('hadoop.base.config.available')


@when('hadoop.base.config.available')
@when_not('hadoop.init.perms.available')
def apply_hadoop_init_perms():
    hadoop_perms_init()
    set_flag('hadoop.init.perms.available')


@when('hadoop.init.perms.available')
@when_not('hadoop.base.available')
def set_hadoop_base_complete():
    set_flag('hadoop.base.available')
