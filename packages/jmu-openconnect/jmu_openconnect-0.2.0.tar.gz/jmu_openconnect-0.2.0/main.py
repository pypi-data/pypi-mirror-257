#!/usr/bin/env python3

import argparse
import getpass
import json
import logging
import os
import shutil
import subprocess
import sys
import time
from enum import Enum
from typing import Optional
from urllib import request

from selenium import webdriver
from selenium.common.exceptions import (
	NoSuchElementException,
	TimeoutException,
	WebDriverException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812
from selenium.webdriver.support.wait import WebDriverWait


class Browser(Enum):
	"""Specify a browser to use"""

	FIREFOX = {'driver': webdriver.Firefox, 'options': webdriver.FirefoxOptions}
	CHROME = {'driver': webdriver.Chrome, 'options': webdriver.ChromeOptions}
	EDGE = {'driver': webdriver.Edge, 'options': webdriver.EdgeOptions}


class MissingDSIDError(Exception):
	"""Raised if DSID cooke was not found."""

	def __init__(
		self,
		msg='DSID Cookie was not found',
		*args,
		**kwargs,
	):
		super().__init__(msg, *args, **kwargs)


class TimedOutError(Exception):
	"""Raised if the webdriver timed out while waiting for authentication."""

	def __init__(
		self,
		msg='webdriver timed out while waiting for authentication',
		*args,
		**kwargs,
	):
		super().__init__(msg, *args, **kwargs)


class MissingOpenConnectError(Exception):
	"""If openconnect could not be found on the PATH."""

	def __init__(
		self,
		msg="openconnect binary could not be found. make sure it's installed and on your PATH",
		*args,
		**kwargs,
	):
		super().__init__(msg, *args, **kwargs)


def fetch_latest_browser_version(browser: Browser) -> str:
	"""Fetches the latest firefox/chromium version from mozilla's/google's API.

	Args:
		browser (Browser): The browser to fetch the version number

	Returns:
		str: The version number as a string. Empty string if something went wrong
	"""
	if browser == Browser.FIREFOX:
		firefox_ver = request.urlopen(
			'https://product-details.mozilla.org/1.0/firefox_history_major_releases.json'
		)
		if firefox_ver.getcode() == 200:
			try:
				# load firefox version info
				firefox_data: dict[str, str] = json.loads(firefox_ver.read())
				# sort firefox version info by most recent release first
				ver = sorted(
					firefox_data.keys(), key=lambda ver: int(ver.split('.')[0])
				)
				# return the greatest version number (last in the list)
				return ver[-1]
			except json.JSONDecodeError:
				return ''
		else:
			return ''

	elif browser == Browser.CHROME:
		chrome_ver = request.urlopen(
			'https://versionhistory.googleapis.com/v1/chrome/platforms/win/channels/stable/versions'
		)
		if chrome_ver.getcode() == 200:
			try:
				# load chrome version info
				chrome_data: dict[str, list[dict[str, str]]] = json.loads(
					chrome_ver.read()
				)
				# return the greatest version number (first in the list)
				return chrome_data['versions'][0]['version']
			except json.JSONDecodeError:
				return ''
		else:
			return ''
	elif browser == Browser.EDGE:
		edge_ver = request.urlopen(
			'https://edgeupdates.microsoft.com/api/products/?view=enterprise'
		)
		if edge_ver.getcode() == 200:
			try:
				# load edge version info
				edge_data: list[dict] = json.loads(edge_ver.read())
				# find the latest stable release
				stable_rel = next(
					item for item in edge_data if item['Product'] == 'Stable'
				)
				# return the greatest version number (first in the list)
				return stable_rel['Releases'][0]['ProductVersion']
			except json.JSONDecodeError:
				return ''
		else:
			return ''
	else:
		return ''


def get_dsid_cookie(
	username: str = '',
	password: str = '',
	browser: Browser = Browser.FIREFOX,
	browser_binary: Optional[str] = None,
	webdriver_timeout: int = 300,
	debug_auth_error: bool = False,
) -> str:
	"""Use selenium to fetch the user's DSID cookie after authentication.

	If both a username and password are provided, the "Log in" button will automatically be clicked.

	Args:
		username (str, optional): Automatically type in a username.
		password (str, optional): Automatically type in a password.
		browser (Browser, optional): Specify a browser to use. Defaults to FIREFOX.
		browser_binary: (Optional[str], optional): Specify a path to your browser's binary. Defaults to None.
		webdriver_timeout (int, optional): The amount of time before the webdriver times out. Defaults to 300.
		debug_auth_error (bool, optional): Whether or not to pause after authentication for debugging. Defaults to False.

	Raises:
		TimedOutError: If the webdriver timed out while waiting for authentication
		MissingDSIDError: If the DSID cookie was not found after authentication

	Returns:
		str: The DSID cookie
	"""
	logging.info("Fetching user's DSID cookie")

	# create browser specific options
	options = browser.value['options']()

	# set the path to the browser's binary if set
	if browser_binary is not None:
		logging.debug(f'Setting browser binary path to `{browser_binary}`')
		options.binary_location = browser_binary

	# dynamically select the browser to use
	logging.debug('Launching browser')
	try:
		driver = browser.value['driver'](options=options)
	except WebDriverException as e:
		# the browser version probably wasn't detected correctly, try to fetch it from the web
		logging.warning('Browser version incorrectly detected')
		logging.debug(e, exc_info=True)
		logging.info(f'Trying to retreieve latest browser version for {browser}')
		options.browser_version = fetch_latest_browser_version(browser)
		logging.info(f'Latest browser version: {options.browser_version!r}')
		logging.info('Relaunching browser')
		# retry launching
		driver = browser.value['driver'](options=options)

	# driver has been successfully started
	logging.debug('Launching vpn.jmu.edu for authentication')
	driver.get('https://vpn.jmu.edu')

	# wait for the Duo prompt to show up
	WebDriverWait(driver, webdriver_timeout).until(
		EC.url_contains('itfederation.jmu.edu')
	)

	# try to input username
	if username:
		try:
			logging.debug('Inputting username')
			username_input = driver.find_element(By.NAME, 'j_username')
			username_input.send_keys(username)
		except NoSuchElementException:
			logging.warning('Username input not found')

	# try to input password
	if password:
		try:
			logging.debug('Inputting password')
			password_input = driver.find_element(By.NAME, 'j_password')
			password_input.send_keys(password)
		except NoSuchElementException:
			logging.warning('Password input not found')

	# automatically click the log in button if username and password were
	# both provided
	if username and password:
		try:
			logging.debug('Attempting to click the log in button')
			submit_button = driver.find_element(
				By.CSS_SELECTOR, "button[type='submit']"
			)
			submit_button.click()
		except NoSuchElementException:
			logging.warning('Log in button not found')

	try:
		# wait until the user authenticates, where they will then be redirected
		# to vpn.jmu.edu
		WebDriverWait(driver, webdriver_timeout).until(EC.url_contains('vpn.jmu.edu'))
	except TimeoutException as e:
		logging.debug('Quitting webdriver')
		driver.quit()

		raise TimedOutError from e

	# try to grab the DSID cookie from the user's storage
	dsid_cookie = driver.get_cookie('DSID')

	# check if the DSID cookie was found
	if dsid_cookie is None:
		logging.error(
			"DSID cookie not found. Make sure that you're only signed in once. See README"
		)

		logging.debug('Quitting webdriver')
		driver.quit()

		raise MissingDSIDError

	if debug_auth_error:
		logging.debug('Pausing for 10 seconds since debug_auth_error is set')
		time.sleep(10)

	logging.debug('Quitting webdriver')
	driver.quit()

	return dsid_cookie['value']


def start_openconnect(dsid_cookie: str) -> int:
	"""Start openconnect with the specified DSID cookie.

	Args:
		dsid_cookie (str): The DSID cookie to authenticate with

	Raises:
		MissingOpenConnectError: If openconnect couldn't be found on the PATH
		PermissionError: If the user isn't root and sudo/doas couldn't be found

	Returns:
		int: the openconnect return code
	"""
	logging.info('Starting openconnect')

	logging.debug('Checking if openconnect is installed')
	if shutil.which('openconnect') is None:
		raise MissingOpenConnectError

	as_root = next(([prog] for prog in ('doas', 'sudo') if shutil.which(prog)), [])
	logging.debug(f'Root program identified: {as_root}')

	# check if the script is running as root or if sudo/doas were not found
	# os.geteuid() will be 0 if root
	if os.geteuid() and not as_root:
		raise PermissionError('sudo/doas were not found')

	oc_command = as_root + [
		'openconnect',
		'--protocol',
		'pulse',
		'--cookie',
		dsid_cookie,
		'https://vpn.jmu.edu',
	]

	logging.debug(f'OC Command: {oc_command}')

	# we use subprocess.call to prompt the user for root if needed, and return the return code
	return subprocess.call(oc_command)


def main():
	logging.basicConfig(
		format='%(asctime)s | %(levelname)s | %(module)s:%(module)s:%(lineno)d - %(message)s',
		level=os.environ.get('LOGLEVEL', 'INFO').upper(),
	)

	parser = argparse.ArgumentParser(
		description='OpenConnect helper for logging into the JMU Ivanti VPN through Duo'
	)

	parser.add_argument(
		'--browser',
		'-b',
		choices=['firefox', 'chrome', 'edge'],
		default='firefox',
		nargs='?',
		help='Which web browser to use in Duo authentication. Default firefox',
	)

	parser.add_argument(
		'--browser-binary',
		'-B',
		help="Specify a path to your browser's binary. Useful if you use a derivative of a supported browser, like WaterFox.",
	)

	parser.add_argument(
		'--username',
		'-u',
		default='',
		help='Automatically type in a username',
	)

	parser.add_argument(
		'--password',
		'-p',
		default='',
		help='Automatically type in a password',
	)

	parser.add_argument(
		'--prompt-password',
		action='store_true',
		help='Prompt for the password without echoing as to not show it in your command history',
	)

	parser.add_argument(
		'--timeout',
		type=int,
		default=300,
		help='Number of seconds it takes before the webdriver times out waiting for authentication. Default 300 seconds',
	)

	parser.add_argument(
		'--debug-auth-error',
		action='store_true',
		help='Pause for 10 seconds after authentication. Useful for debugging errors',
	)

	parser.add_argument(
		'--only-authenticate',
		action='store_true',
		help="Only authenticate and don't start openconnect. Prints the DSID cookie to STDOUT",
	)

	args = parser.parse_args()

	# check if we need to prompt the user for a password
	password = args.password
	if args.prompt_password:
		password = getpass.getpass('Password: ')

	# assign the browser to use. argparse guarentees that it will be one of these three
	browser = {
		'firefox': Browser.FIREFOX,
		'chrome': Browser.CHROME,
		'edge': Browser.EDGE,
	}[args.browser]

	try:
		dsid_cookie = get_dsid_cookie(
			username=args.username,
			password=password,
			browser=browser,
			browser_binary=args.browser_binary,
			webdriver_timeout=args.timeout,
			debug_auth_error=args.debug_auth_error,
		)
	except TimedOutError:
		print('webdriver timed out while waiting for authentication')
		sys.exit(1)
	except MissingDSIDError:
		print(
			'DSID Cookie was not found. Ensure that you are not logged in multiple times. See README for details.'
		)
		sys.exit(1)

	if args.only_authenticate:
		print(dsid_cookie)
		sys.exit(0)

	exit_code = 0
	try:
		exit_code = start_openconnect(dsid_cookie=dsid_cookie)
	except MissingOpenConnectError:
		print(
			'openconnect was not found on your PATH. Please ensure that openconnect is installed.'
		)
		exit_code = 1
	except PermissionError:
		print(
			'sudo was not found on your PATH. Please install sudo or run this script as root.'
		)
		exit_code = 1

	sys.exit(exit_code)


if __name__ == '__main__':
	main()
