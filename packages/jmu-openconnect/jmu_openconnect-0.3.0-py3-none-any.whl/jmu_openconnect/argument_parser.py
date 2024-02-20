"""Module for parsing command line arguments."""

import argparse


def parse_args() -> argparse.Namespace:
	"""Parse command line arguments.

	Returns:
		argparse.Namespace: an argparse Namespace containing the parsed arguments
	"""
	parser = argparse.ArgumentParser(
		description='OpenConnect helper for logging into the JMU Ivanti VPN through Duo',
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
		'-P',
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
		'-A',
		'--only-authenticate',
		action='store_true',
		help="Only authenticate and don't start openconnect. Prints the DSID cookie to STDOUT",
	)

	return parser.parse_args()
