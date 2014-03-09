from fabric.api import hosts, sudo, task


@task
@hosts('106.187.44.69')
def host_type():
    sudo('uname -s')
