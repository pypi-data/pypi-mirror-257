"""Main pyaws manager class and entry point

The main driver class contains code for common actions performed by all subscreens such as
profile management, as well as functions for switching between subscreens.

Author: James Lavender 
Created: 2023-12-01
"""
# Core Python Utilities
import argparse
import json
import os
import shutil
import subprocess
import threading
import datetime
from subprocess import Popen, PIPE

# py_cui library used for Command Line UI construction
import py_cui

# AWS SDK used for AWS operations
import boto3

# Subscreens and pyaws modules
import pyaws.logger as LOGGER
import pyaws.about_screen as ABOUT
import pyaws.settings_screen as SETTINGS
import pyaws.metadata_manager as METADATA
import pyaws.account_select_screen as SELECT
import pyaws.account_console_screen as CONTROL

# AWS Subscreens and modules
import pyaws.aws as AWS
import pyaws.aws.ec2 as EC2CONSOLE
import pyaws.aws.iam as IAMCONSOLE
import pyaws.aws.secrets_manager as SMCONSOLE
import pyaws.aws.systems_manager as SSMCONSOLE
import pyaws.aws.route53 as R53CONSOLE

# Module version + copyright
__version__     = '0.0.3'
__copyright__   = '2024'


# Helper functions
def get_aws_credentials_path(self):
    """Returns the path to the AWS credentials file

    Returns
    -------
    path : str
        Path to the AWS credentials file
    """

    path = ""
    path = os.path.expanduser('~/.aws/credentials')

    LOGGER.write('PyAWS - Found credentials file in path: {}'.format(path))

    return path


def get_aws_profiles(self):
    """Returns a list of AWS profiles from the AWS credentials file

    Returns
    -------
    profiles : list of str
        List of AWS profiles from the AWS credentials file
    """
    profiles = []
    try:
        with open(get_aws_credentials_path(self), 'r') as cred_file:
            for line in cred_file.readlines():
                if line.startswith('['):
                    profiles.append(line[1:-2])
    except:
        pass
    
    LOGGER.write('PyAWS - Found profiles: {}'.format(profiles))

    return profiles


def get_aws_regions(self):
    """Returns a list of AWS regions available as of April 2023.

    Returns
    -------
    regions : list of str
        List of AWS regions
    """

    regions = [
        "us-east-1",
        "us-east-2",
        "us-west-1",
        "us-west-2",
        "af-south-1",
        "ap-east-1",
        "ap-south-1",
        "ap-northeast-3",
        "ap-northeast-2",
        "ap-southeast-1",
        "ap-southeast-2",
        "ap-northeast-1",
        "ca-central-1",
        "eu-central-1",
        "eu-west-1",
        "eu-west-2",
        "eu-south-1",
        "eu-west-3",
        "eu-north-1",
        "me-south-1",
        "sa-east-1"
    ]
    LOGGER.write('PyAWS - Found regions: {}'.format(regions))
    return regions


def parse_args():
    """Parses command line arguments

    Returns
    -------
    credentials_file : str
        AWS Credentials file path
    save_metadata : bool
        flag to say if metadata should be saved
    """

    target_dir = "."

    parser = argparse.ArgumentParser(description='pyaws - A command line AWS console')
    parser.add_argument('-p', '--profile',          help='AWS profile to use. Overwrites working directory profile setting.')
    parser.add_argument('-r', '--region',           help='AWS region to use. Overwrites working directory region.')
    parser.add_argument('-w', '--workspace',        help='Pass a path to this argument to start pyaws in a workspace not the current directory.')
    parser.add_argument('-n', '--nosavemetadata',   action='store_true', help='Disables Metadata saving between sessions. Includes profile and region.')
    parser.add_argument('-d', '--debug',            action='store_true', help='Enable debug logging. Logs to .pyaws/pyaws.log. Overrides metadata setting.')
    parser.add_argument('-v', '--version',          action='store_true', help='Show version')
    args = vars(parser.parse_args())

    if args['version']:
        print('pyaws version: v{}\n'.format(__version__))
        exit()
    
    if args['workspace'] is not None:
        if os.path.exists(args['workspace']):
            if os.path.isdir(args['workspace']):
                os.chdir(args['workspace'])
            else:
                print('ERROR - Path {} is not a directory.'.format(args['workspace']))
                exit(-1)
        else:
            print('ERROR - Path {} does not exist.'.format(args['workspace']))
            exit(-1)

    return target_dir, args

def main(): 
    """Entry point for the pyaws application. It is responsible for parsing command line arguments and initializing the CUI.
    """

    # Parse command line arguments
    target, args = parse_args()
    save_metadata = not args['nosavemetadata']
    debug_logging = args['debug']

    target_abs = os.path.abspath(target)
    
    # Make sure we have write permissions
    if not os.access(target, os.W_OK):
        print('PyAWS - Main - ERROR - Permission error for target {}'.format(target_abs))
        exit(-1)

    if debug_logging:
        LOGGER.set_log_file_path('.pyaws/{}.log'.format(str(datetime.datetime.today()).split(' ')[0]))
        LOGGER.toggle_logging()
        LOGGER.write('PyAWS - Main - Initialized debug logging')

    root = py_cui.PyCUI(5, 4)

    if debug_logging:
        root.enable_logging(log_file_path='.pyaws/py_cui_root.log')
    
    # Use feature added in py_cui 0.0.3 to add unicode widget borders
    root.toggle_unicode_borders()

    _ = PyAWSManager(root, target, save_metadata, args)

    LOGGER.write('PyAWS - Main - Parsed args. Target location - {}'.format(target_abs))
    LOGGER.write('PyAWS - Main - Initialized manager object, starting CUI...')

    root.start()

# Main pyaws manager class
    
class PyAWSManager:
    """
    Main pyaws manager class. Controls all operations of the CUI.
    
    """
    def __init__(self, root, target_path, save_metadata, args):
        """Constructor for PyAWSManager
        """

        self.root = root
        self.settings_manager = SETTINGS.SettingsScreen(self)
        self.about_manager = ABOUT.AboutScreenManager(self)
        self.select_manager = SELECT.AccountSelectManager(self)
        self.console_manager = CONTROL.AccountConsoleManager(self)
        self.ec2_manager = EC2CONSOLE.EC2ConsoleManager(self)
        self.secretsmanager_manager = SMCONSOLE.SMConsoleManager(self)
        self.iam_manager = IAMCONSOLE.IAMConsoleManager(self)
        self.systemsmanager_manager = SSMCONSOLE.SSMConsoleManager(self)
        self.route53_manager = R53CONSOLE.R53ConsoleManager(self)
        LOGGER.write('PyAWSManager - init - Initialized subscreen managers')

        self.save_metadata = save_metadata

        self.current_path   = os.path.abspath(target_path)
        self.workspace_path = self.current_path
        
        self.current_screen = 'select'
        self.default_profile = None
        self.default_region = None
        self.session = None

        self.metadata_manager = METADATA.PyAWSMetadataManager(self)
        self.loaded_metadata  = self.metadata_manager.read_metadata()
        LOGGER.write('PyAWSManager - init - Loaded metadata')
        LOGGER.write(self.loaded_metadata)
        self.metadata_manager.apply_metadata(self.loaded_metadata)
        LOGGER.write('PyAWSManager - init - Applied metadata')

        if args['profile']:
            LOGGER.write('PyAWSManager - init - Overwriting default profile to {}'.format(args['profile']))
            self.default_profile = args['profile']
        if args['region']:
            LOGGER.write('PyAWSManager - init - Overwriting default region to {}'.format(args['region']))
            self.default_region = args['region']

        if self.default_profile:
            self.current_screen = 'console'

        # Temp variable fired on callback after input
        self.post_input_callback = None

        # Add a run on exit callback to save metadata and close log file
        self.root.run_on_exit(self.close_cleanup)

        # Account select screen widgets, key commands
        self.profile_path = get_aws_credentials_path(self)
        self.profiles = get_aws_profiles(self)
        self.regions  = get_aws_regions(self)

        # Initialize CUI elements for each sub-screen
        self.select_widget_set = self.select_manager.initialize_screen_elements()
        self.console_widget_set = self.console_manager.initialize_screen_elements()
        self.ec2_manager_widget_set = self.ec2_manager.initialize_screen_elements()
        self.iam_manager_widget_set = self.iam_manager.initialize_screen_elements()
        self.secretsmanager_manager_widget_set = self.secretsmanager_manager.initialize_screen_elements()
        self.systemsmanager_manager_widget_set = self.systemsmanager_manager.initialize_screen_elements()
        self.route53_manager_widget_set = self.route53_manager.initialize_screen_elements()
        self.settings_widget_set = self.settings_manager.initialize_screen_elements()
        self.about_widget_set = self.about_manager.initialize_screen_elements()
        LOGGER.write('PyAWSManager - init - Initialized screen elements')

        # Open screen based on metadata
        if self.current_screen == 'select':
            LOGGER.write('PyAWSManager - init - Opening account select window')
            self.open_account_select_window()
        
        elif self.current_screen == 'console':
            LOGGER.write('PyAWSManager - init - Opening account console window')
            self.open_account_console_window()

    # Helper functions
    def close_cleanup(self):
        """Function fired upon closing pyaws
        """

        LOGGER.write('PyAWSManager - close_cleanup - Closing pyaws')
        if self.save_metadata:
            self.metadata_manager.write_metadata()
        LOGGER.close_logger()


    def clean_exit(self):
        """Function that exits the CUI cleanly
        """

        LOGGER.write('PyAWSManager - clean_exit - Exiting pyaws.')
        self.close_cleanup()
        exit()


    def error_exit(self):
        """Function that exits the CUI with an error code
        """

        LOGGER.write('PyAWSManager - error_exit - Exiting with error!')
        self.close_cleanup()
        exit(-1)


    def open_not_supported_popup(self, operation):
        """Function that displays warning for a non-supported operation

        Parameters
        ----------
        operation : str
            The name of the non-supported operation
        """

        LOGGER.write('PyAWSManager - open_not_supported_popup - Opening warning popup for non-supported operation: {}'.format(operation))
        self.root.show_warning_popup('Warning - Not Supported', 'The {} operation is not yet supported.'.format(operation))


    def open_profile_not_provied_popup(self):
        """Function that displays warning when default_profile is not set.
        """

        LOGGER.write('PyAWSManager - open_profile_not_provied_popup - Opening warning popup for non-provided profile')
        self.root.show_warning_popup('Warning - No Connection', 'Profile not provided. Unable to open console. Please set the profile first.')


    def open_region_not_provied_popup(self):
        """Function that displays warning when default_region is not set.
        """

        LOGGER.write('PyAWSManager - open_region_not_provied_popup - Opening warning popup for non-provided region')
        self.root.show_warning_popup('Warning - No Connection', 'Region not provided. Unable to open console. Please set the region first.')


    def open_connection_not_established_popup(self):
        """Function that displays warning when connection is not established.
        """

        LOGGER.write('PyAWSManager - open_connection_not_established_popup - Opening warning popup for non-established connection')
        self.root.show_warning_popup('Warning - No Connection', 'AWS Session not established. Please verify credentials, region, and profile selection.')


    # Open subscreen functions
    def open_account_console_window(self):
        """Function that opens the account console window
        """

        if self.default_profile == '' or self.default_profile is None:
            LOGGER.write('PyAWSManager - open_account_console_window - Profile not set. Returning to account select window')
            self.open_profile_not_provied_popup()
            return

        LOGGER.write('PyAWSManager - open_account_console_window - Opening account console window')
        self.console_manager.set_initial_values()
        self.root.apply_widget_set(self.console_widget_set)
        self.root.set_title('{} - {} - {}'.format(self.current_screen, self.default_profile, self.default_region))
        self.console_manager.set_initial_focus()


    def open_account_select_window(self):
        """Function that opens the account select window
        """

        LOGGER.write('PyAWSManager - open_account_select_window - Opening account select window')
        self.select_manager.set_initial_values()
        self.root.apply_widget_set(self.select_widget_set)
        self.root.set_title('{} - {} - {}'.format(self.current_screen, self.default_profile, self.default_region))
        self.select_manager.set_initial_focus()


    def open_settings_window(self):
        """Function that opens the settings window
        """

        LOGGER.write('PyAWSManager - open_settings_window - Opening settings window')
        self.settings_manager.set_initial_values()
        self.root.apply_widget_set(self.settings_widget_set)
        self.root.set_title('{} - {} - {}'.format(self.current_screen, self.default_profile, self.default_region))
        self.settings_manager.set_initial_focus()


    def open_about_window(self):
        """Function that opens the about window
        """

        LOGGER.write('PyAWSManager - open_about_window - Opening settings window')
        self.about_manager.set_initial_values()
        self.root.apply_widget_set(self.about_widget_set)
        self.root.set_title('{} - {} - {}'.format(self.current_screen, self.default_profile, self.default_region))
        self.about_manager.set_initial_focus()


    def open_resource_console_window(self):
        """Function that opens the resource console window

        Parameters
        ----------
        selection : str
            The name of the window to open
        """
        selection = self.console_manager.resource_select_box.get().lower()
        # selection = self.current_screen

        self.resource_screen_managers = {
            'ec2': self.ec2_manager,
            'secretsmanager': self.secretsmanager_manager,
            'iam': self.iam_manager,
            'systemsmanager': self.systemsmanager_manager,
            'route53': self.route53_manager
        }

        self.resource_screen_widget_sets = {
            'ec2': self.ec2_manager_widget_set,
            'secretsmanager': self.secretsmanager_manager_widget_set,
            'iam': self.iam_manager_widget_set,
            'systemsmanager': self.systemsmanager_manager_widget_set,
            'route53': self.route53_manager_widget_set
        }

        if self.session is None:
            LOGGER.write('PyAWSManager - open_resource_console_window - Session not set. Returning to account console window')
            self.open_connection_not_established_popup()
            return

        if self.default_region == '' or self.default_region is None:
            LOGGER.write('PyAWSManager - open_resource_console_window - Region not set. Returning to account console window')
            self.open_region_not_provied_popup()
            return
        
        if selection in self.resource_screen_managers:
            LOGGER.write('PyAWSManager - open_resource_console_window - Opening selected resrouce console: {}'.format(selection))
            manager = self.resource_screen_managers[selection]
            widget_set = self.resource_screen_widget_sets[selection]

            manager.set_initial_values()
            self.root.apply_widget_set(widget_set)
            self.root.set_title('{} - {} - {}'.format(self.current_screen, self.default_profile, self.default_region))
            manager.set_initial_focus()
        else:
            LOGGER.write('PyAWSManager - open_resource_console_window - Resource Console {} not supported: '.format(selection))
            self.open_not_supported_popup('{} console'.format(selection.upper()))
            LOGGER.write('PyAWSManager - open_resource_console_window - Returning to account console window')
            self.open_account_console_window()


    # Settings update functions
    def update_default_profile(self, profile):
        """Function that updates the default profile

        Parameters
        ----------
        profile : str
            The new default profile
        """

        LOGGER.write('PyAWSManager - Updating default profile to {}'.format(profile))
        self.default_profile = profile

    
    def update_default_region(self, region):
        """Function that updates the default region

        Parameters
        ----------
        region : str
            The new default region
        """

        LOGGER.write('PyAWSManager - Updating default region to {}'.format(region))
        self.default_region = region


    def establish_aws_connection(self):
        """Function that establishes a connection to the AWS account

        Returns
        -------
        bool
            True if connection successful, False otherwise
        """
        LOGGER.write('PyAWSManager - establish_connection - Initializing AWS Manager')
        self.aws_manager = AWS.AWSManager(self.default_profile, self.default_region)
        
        LOGGER.write('PyAWSManager - establish_connection - Establishing connection to {} in {}'.format(self.default_profile, self.default_region))
        self.connection_established = self.aws_manager.establish_aws_connection()

        if self.connection_established:
            LOGGER.write('PyAWSManager - establish_connection - Connection established')
            self.session = self.aws_manager.session
            return self.connection_established
        elif not self.connection_established:
            LOGGER.write('PyAWSManager - establish_connection - Connection not established')
            return self.connection_established


    # Message Functions
    def update_message(self, message):
        """Function that is run after user inputs message
        
        Parameters
        ----------
        message : str
            User returned input
        """

        LOGGER.write('PyAWSManager - update_message - Updating message to {}'.format(message))
        self.user_message = message
        if self.post_input_callback is not None:
            self.post_input_callback()
        self.post_input_callback = None
    
    def ask_message(self, prompt, callback=None):
        """Function that asks the user for input.
        
        Parameters
        ----------
        prompt : str
            Prompt for user input
        callback : function
            Default None, otherwise, function fired after credentials are asked
        """

        LOGGER.write('PyAWSManager - ask_message - Asking user for input with prompt: {}'.format(prompt))
        if callback is not None:
            self.post_input_callback = callback
        self.root.show_text_box_popup(prompt, self.update_message)

    # PyAWS Metadata Functions
    def get_logo_text(self):
        """Generates ascii-art version of pyaws logo

        Returns
        -------
        logo : str
            ascii-art logo
        """

        LOGGER.write('PyAWSManager - get_logo_text - Generating logo text')
        logo = '\n'
        logo =  '                _____  __      __  _________ \n'
        logo += '______ ___.__. /  _  \\/  \\    /  \\/   _____/ \n'
        logo += '\\____ <   |  |/  /_\\  \\   \\/\\/   /\\_____  \\  \n'
        logo += '|  |_> >___  /    |    \\        / /        \\ \n'
        logo += '|   __// ____\\____|__  /\\__/\\  / /_______  / \n'
        logo += '|__|   \\/            \\/      \\/          \\/  \n'
        return logo

    def get_about_info(self, with_logo=True):
        """Generates some about me information

        Parameters
        ----------
        with_logo : bool
            flag to show logo or not.
        
        Returns
        -------
        about_info : str
            string with about information
        """

        LOGGER.write('PyAWSManager - get_about_info - Generating about info')
        if with_logo:
            about_info = ' ' + self.get_logo_text() + '\n\n\n'
        else:
            about_info = '\n'
        about_info = about_info + 'Author: James Lavender \n\nPython CUI AWS Client: https://github.com/j-lavender/pyaws_cui\n\n\n'
        about_info = about_info + 'Created from PyAutoGit (Python CUI Git Client):\n\n'
        about_info = about_info + 'https://github.com/jwlodek/pyautogit\n\n'
        about_info = about_info + 'Powered by PyCUI (Python CUI Library):\n'
        about_info = about_info + 'https://github.com/jwlodek/py_cui\n\n\n'
        about_info = about_info + 'Documentation available here:\n\n'
        about_info = about_info + 'pyaws:   https://j-lavender.github.io/pyaws-docs\n'
        about_info = about_info + 'Be sure to Star on Github!\n\n'
        about_info = about_info + 'Copyright (c) {} James Lavender'.format(__copyright__)
        return about_info
    
    def get_welcome_message(self):
        """Function that gets a basic welcome message shown at first run
        
        Returns
        -------
        welcome : str
            welcome message string
        """

        LOGGER.write('PyAWSManager - get_welcome_message - Generating welcome message')
        welcome = 'Welcome to pyaws!\n\n'
        welcome = welcome + 'This is a command line AWS console written in Python.\n\n'
        welcome = welcome + 'This is a work in progress, so please report any bugs you find on Github!\n\n'
        return welcome