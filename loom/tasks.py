from fabric.api import *
import subprocess

__all__ = ['ssh', 'all', 'uptime', 'upgrade', 'restart', 'reboot']

@task
def all():
    """
    Select all hosts
    """
    env.hosts = []
    for hosts in env.roledefs.values():
        env.hosts.extend(hosts)
    # remove dupes
    env.hosts = list(set(env.hosts))

@task
def uptime():
    run('uptime')

@task
def upgrade(non_interactive=False):
    """
    Upgrade apt packages
    """
    with settings(hide('stdout'), show('running')):
        sudo('apt-get update')
    upgrade_command = ['apt-get', 'upgrade']
    if non_interactive:
        upgrade_command.append('-y')
    sudo(' '.join(upgrade_command))

@task
def ssh(*cmd):
    """
    Open an interactive ssh session
    """
    run = ['ssh', '-A', '-t']
    if env.key_filename:
        run.extend(["-i", env.key_filename])
    run.append('%s@%s' % (env.user, env.host_string))
    run += cmd
    subprocess.call(run)

@task
def restart(service):
    """
    Restart or start an upstart service
    """
    with settings(warn_only=True):
        result = sudo('restart %s' % service)
    if result.failed:
        sudo('start %s' % service)

@task
def reboot():
    """
    Reboot a host
    """
    sudo('reboot')


