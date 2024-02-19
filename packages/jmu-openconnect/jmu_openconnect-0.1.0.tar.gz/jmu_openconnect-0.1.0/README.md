# JMU OpenConnect

<p align="center">
	<a href="https://badge.fury.io/py/jmu-openconnect"><img alt="PyPI" src="https://img.shields.io/pypi/v/jmu-openconnect" /></a>
	<a href="https://pepy.tech/project/jmu-openconnect"><img alt="Downloads" src="https://pepy.tech/badge/jmu-openconnect" /></a>
	<a href="https://github.com/TabulateJarl8/jmu-openconnect/blob/master/LICENSE"><img alt="License" src="https://img.shields.io/pypi/l/jmu-openconnect.svg" /></a>
	<a href="https://github.com/TabulateJarl8/vapor/graphs/commit-activity"><img alt="Maintenance" src="https://img.shields.io/badge/Maintained%3F-yes-green.svg" /></a>
	<a href="https://github.com/TabulateJarl8/vapor/issues/"><img alt="GitHub Issues" src="https://img.shields.io/github/issues/TabulateJarl8/vapor.svg" /></a>
	<a href="https://github.com/TabulateJarl8"><img alt="GitHub followers" src="https://img.shields.io/github/followers/TabulateJarl8?style=social" /></a>
	<br>
	<a href="https://ko-fi.com/L4L3L7IO2"><img alt="Kofi Badge" src="https://ko-fi.com/img/githubbutton_sm.svg" /></a>
</p>

This is a wrapper script around openconnect to help with authentication for the JMU VPN on Linux. Openconnect used to work fine until Ivanti purchased Pulse Secure, and then that broke something. This script opens up a web browser to allow the user to authenticate with Duo, and then grabs the DSID cookie to use for openconnect authentication.

## Installation
This script can easily be installed with pip or [pipx](https://pipx.pypa.io/stable/) with the following commands:

```console
$ pip3 install jmu-openconnect
$ # OR
$ pipx install jmu-openconnect
```

This script can also be used as a standalone script by downloading the `main.py` file and ensuring that selenium is installed with `pip3 install selenium`, or by cloning the repository and running `poetry install`.

## Usage
Once the script is installed, you can run the following command in your terminal:

```console
$ jmu-openconnect
```

You can also specify a username and password to be automatically typed in, however you will still have to do 2FA manually. You can specify one or the other or both, and if both are specified, the "Log in" button will automatically be clicked.

```console
$ jmu-openconnect -u <EID> -p <PASSWORD>
```

You can alternatively specify the `--prompt-password` option instead of using `-p`, which will prompt the user for a password without echoing, much like sudo. This is more secure as your password won't be saved in your command line history.

JMU OpenConnect defaults to using firefox, but you can easily change which browser you're using by specifying `--browser`, which accepts `firefox`, `chrome`, or `edge`.

```console
$ jmu-openconnect --browser chrome
```

To see all of the available options, run `jmu-openconnect --help`.

## Dependencies
This script just requires openconnect, [selenium](https://pypi.org/project/selenium/), and a webdriver. On my machine, it seems that the webdrivers are automatically installed if you have Firefox or Chromium installed, so you probably don't need to worry about this. If you are having problems, check the [Selenium Python Documentation](https://selenium-python.readthedocs.io/installation.html#drivers0).

## Why is this all in one script?
I heavily considered splitting this up into multiple files, but I really wanted to preserve the ability to just have this script up on a website somewhere where people could just download this script, install selenium, and run it with Python. This may change in the future but this is what I've gone with for now.

## DSID Cookie was not found
If you get the error that the DSID cookie was not found, then you may be logged on in multiple places at once. Navigate to https://vpn.jmu.edu and after signing in, you should see a screen like this:

![Maximum number of open user sessions screenshot](img/multi_sign_in.png)

If this is the case, just select the box to remove that sign in and retry the script after verifying that you are signed out of all browser sessions. If this is not the problem, try running the script with `jmu-openconnect --debug-auth-error` to see the error for a longer period of time.