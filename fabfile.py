from fabric.api import sudo, hosts, task

@task
@hosts('106.187.44.69')
def host_type():
    sudo('uname -s')
