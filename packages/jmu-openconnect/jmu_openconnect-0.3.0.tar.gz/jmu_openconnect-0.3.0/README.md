# JMU OpenConnect

<p align="center">
	<a href="https://badge.fury.io/py/jmu-openconnect"><img alt="PyPI" src="https://img.shields.io/pypi/v/jmu-openconnect" /></a>
	<a href="https://pepy.tech/project/jmu-openconnect"><img alt="Downloads" src="https://pepy.tech/badge/jmu-openconnect" /></a>
	<a href="https://github.com/TabulateJarl8/jmu-openconnect/blob/master/LICENSE"><img alt="License" src="https://img.shields.io/pypi/l/jmu-openconnect.svg" /></a>
	<a href="https://github.com/TabulateJarl8/jmu-openconnect/graphs/commit-activity"><img alt="Maintenance" src="https://img.shields.io/badge/Maintained%3F-yes-green.svg" /></a>
	<a href="https://github.com/TabulateJarl8/jmu-openconnect/issues/"><img alt="GitHub Issues" src="https://img.shields.io/github/issues/TabulateJarl8/jmu-openconnect.svg" /></a>
	<a href="https://github.com/TabulateJarl8"><img alt="GitHub followers" src="https://img.shields.io/github/followers/TabulateJarl8?style=social" /></a>
	<br>
	<a href="https://ko-fi.com/L4L3L7IO2"><img alt="Kofi Badge" src="https://ko-fi.com/img/githubbutton_sm.svg" /></a>
</p>

This is a wrapper script around openconnect to help with authentication for the JMU VPN on Linux. Openconnect used to work fine until Ivanti purchased Pulse Secure, and then that broke something. This script opens up a web browser to allow the user to authenticate with Duo, and then grabs the DSID cookie to use for openconnect authentication.

## Installation
This script can easily be installed with pip or [pipx](https://pipx.pypa.io/stable/) with the following commands:

```console
$ pipx install jmu-openconnect
$ # OR
$ pip3 install jmu-openconnect
```

## Usage
Once the script is installed, you can run the following command in your terminal:

```console
$ jmu-openconnect
```

You can also specify a username and password to be automatically typed in, however you will still have to do 2FA manually. You can specify one or the other or both, and if both are specified, the "Log in" button will automatically be clicked.

```console
$ jmu-openconnect -u <EID> -p <PASSWORD>
```

You can alternatively specify the `--prompt-password` (or `-P`) option instead of using `-p`, which will prompt the user for a password without echoing, much like sudo. This is more secure as your password won't be saved in your command line history.

JMU OpenConnect defaults to using firefox, but you can easily change which browser you're using by specifying `--browser`, which accepts `firefox`, `chrome`, or `edge`.

The first time that you launch JMU OpenConnect, it may take a little longer than normal, as selenium has to download and cache your webdriver.

```console
$ jmu-openconnect --browser chrome
```

To see all of the available options, run `jmu-openconnect --help`.

## Dependencies
This script just requires openconnect and [selenium](https://pypi.org/project/selenium/). If you are having problems, check the [Selenium Python Documentation](https://selenium-python.readthedocs.io/installation.html#drivers0).

## DSID Cookie was not found
If you get the error that the DSID cookie was not found, then you may be logged on in multiple places at once. Navigate to https://vpn.jmu.edu and after signing in, you should see a screen like this:

![Maximum number of open user sessions screenshot](img/multi_sign_in.png)

If this is the case, just select the box to remove that sign in and press "Close Selected Sessions and Log in". After this, you will need to press the log out button in the upper right corner of the VPN website, and then you can retry the script. If this is not the problem, try running the script with `jmu-openconnect --debug-auth-error` to see the error for a longer period of time.