"""File containing functions used by the secrets manager commands.

This file is meant to handle the AWS SecretsManager CUI elements and connections 
to the underlying AWS SecretsManager commands found in pyaws.aws.secretsmanager.commands.
"""

import json

import pyperclip

import py_cui
import pyaws
import pyaws.screen_manager
import pyaws.logger as LOGGER
import pyaws.aws.secrets_manager.sm_commands as SMCommands
from tabulate import tabulate

class SMConsoleManager(pyaws.screen_manager.ScreenManager):
    """Class responsible for managing the Secrets Manager Console screen.

    This class provides functions used by pyaws to manage the Secrets Manager Console CUI screen.
    It provides the interface between the CUI and the underlying AWS SecretsManager 
    commands aws commands found in pyaws.aws. It inherits from the ScreenManager class, which provides
    the basic functionality for all screen managers in pyaws.

    Attributes
    ----------
    menu_choices : list of str
        Overriden list of menu choices accessible from the account select menu
    """

    def __init__(self, top_manager):
        """Constructor for the SecretsManagerScreen class.
        """

        super().__init__(top_manager, "Secrets Manager Console")
        self.menu_choices = ['Change Console',
                        'Settings',
                        # 'Enter Custom Command',
                        'Exit']
    

    def process_menu_selection(self, selection):
        """Override of base class, executes depending on menu selection

        Parameters
        ----------
        selection : str
            The user's menu selection
        """
        
        LOGGER.write('SMConsoleManager - process_menu_selection - Selection: {}'.format(selection))
        if selection == 'Change Console':
            self.manager.open_account_console_window()
        elif selection == 'Settings':
            self.manager.open_settings_window()
        # elif selection == 'Enter Custom Command':
        #     self.ask_custom_command()
        elif selection == 'Exit':
            self.manager.close_cleanup()
            exit()
        else:
            self.manager.open_not_supported_popup(selection)


    def initialize_screen_elements(self):
        """Function that initializes the screen elements for the Secrets Manager Console.
        """

        LOGGER.write('SMConsoleManager - initialize_screen_elements')

        # SecretsManager Console Screen Widgets and Keybindings
        sm_console_manager_widget_set = self.manager.root.create_new_widget_set(12, 3)

        # Base Keyboard Bindings
        sm_console_manager_widget_set.add_key_command(py_cui.keys.KEY_BACKSPACE, self.manager.open_account_console_window)
        sm_console_manager_widget_set.add_key_command(py_cui.keys.KEY_R_LOWER, self.set_initial_values)
        sm_console_manager_widget_set.add_key_command(py_cui.keys.KEY_S_LOWER, self.manager.open_settings_window)
        sm_console_manager_widget_set.add_key_command(py_cui.keys.KEY_H_LOWER, self.show_help_text)
        sm_console_manager_widget_set.add_key_command(py_cui.keys.KEY_M_LOWER, self.show_menu)
        sm_console_manager_widget_set.add_key_command(py_cui.keys.KEY_C_LOWER, self.copy_current_secret_value_to_clipboard)

        # Secrets Manager Secrets Selection Menu
        self.sm_secrets_menu = sm_console_manager_widget_set.add_scroll_menu('Secrets', 2, 0, row_span=7, column_span=1)
        self.sm_secrets_menu.add_key_command(py_cui.keys.KEY_BACKSPACE, self.manager.open_account_console_window)
        self.sm_secrets_menu.add_key_command(py_cui.keys.KEY_ENTER, self.display_secret_versions)
        self.sm_secrets_menu.add_key_command(py_cui.keys.KEY_C_LOWER, self.copy_current_secret_value_to_clipboard)
        self.sm_secrets_menu.add_key_command(py_cui.keys.KEY_H_LOWER, self.show_help_text)
        self.sm_secrets_menu.add_key_command(py_cui.keys.KEY_Q_LOWER, self.manager.clean_exit)
        self.sm_secrets_menu.set_focus_text('View Secret - Enter | Copy Displayed Secret Value to Clipboard - c | Backspace - Console Selection | Quit - q')
        self.sm_secrets_menu.add_text_color_rule('.*', py_cui.RED_ON_BLACK, rule_type='contains', match_type='line')

        # Secrets Manager Secret Versions Selection Menu
        self.sm_secret_versions_menu = sm_console_manager_widget_set.add_scroll_menu('Versions', 9, 0, row_span=3, column_span=1)
        self.sm_secret_versions_menu.add_key_command(py_cui.keys.KEY_BACKSPACE, self.manager.open_account_console_window)
        self.sm_secret_versions_menu.add_key_command(py_cui.keys.KEY_ENTER, self.set_current_secret_version)
        self.sm_secret_versions_menu.add_key_command(py_cui.keys.KEY_H_LOWER, self.show_help_text)
        self.sm_secret_versions_menu.add_key_command(py_cui.keys.KEY_Q_LOWER, self.manager.clean_exit)
        self.sm_secret_versions_menu.set_focus_text('View Secret Version - Enter | Copy Displayed Secret Value to Clipboard - c | Backspace - Console Selection | Quit - q')
        self.sm_secret_versions_menu.add_text_color_rule('.*', py_cui.MAGENTA_ON_BLACK, rule_type='contains', match_type='line')

        # Secrets Manager Secret Details Textbox
        self.sm_info_text_block = sm_console_manager_widget_set.add_text_block('Details', 0, 1, row_span=3, column_span=2)
        # Colorize all text (skips all table formatting). Obviously there is no way I figured this out myself. Thanks GPT!
        self.sm_info_text_block.add_text_color_rule('│ ([^│]+)', py_cui.GREEN_ON_BLACK, rule_type='contains', match_type='regex')
        # self.sm_info_text_block.add_text_color_rule('(?<=\│ )[^│]*(?= )', py_cui.GREEN_ON_BLACK, rule_type='contains', match_type='regex')

        # Secrets Manger Secret Value Textbox
        self.sm_value_text_block = sm_console_manager_widget_set.add_text_block('Secret Value', 3, 1, row_span=9, column_span=2)

        # Custom command input box
        # self.custom_command_input_box = sm_console_manager_widget_set.add_text_box('Custom Command', 11, 0, row_span=1, column_span=3, initial_text='aws secretsmanager help')

        self.logo_label = sm_console_manager_widget_set.add_block_label(self.get_logo_text(), 0, 0, row_span=2, column_span=1, center=True)
        self.logo_label.set_color(py_cui.CYAN_ON_BLACK)
        self.logo_label.set_selectable(False)

        return sm_console_manager_widget_set


    def refresh_status(self):
        """Function that refreshes the Secrets Manager Console screen.
        """

        LOGGER.write('SMConsoleManager - refresh_status')
        # self.manager.open_secrets_manager_console_window()


    def clear_elements(self):
        """Function that clears the Secrets Manager Console screen elements.
        """

        LOGGER.write('SMConsoleManager - clear_resource_elements')
        self.sm_secrets_menu.clear()
        self.sm_secret_versions_menu.clear()
        self.sm_info_text_block.clear()
        self.sm_value_text_block.clear()
        # self.custom_command_input_box.clear()


    def set_initial_values(self):
        """Function that sets the initial values for the Secrets Manager Console screen elements.
        """

        LOGGER.write('SMConsoleManager - set_initial_values')
        self.manager.current_screen = 'secrets_manager'
        LOGGER.write('SMConsoleManager - set_initial_values - Set current_screen: {}'.format(self.manager.current_screen))
        LOGGER.write('SMConsoleManager - set_initial_values - Set AWS Session.')
        self.session = self.manager.session
        self.current_secret_name = None
        self.current_secret_version = None
        self.sm_commands = SMCommands.SecretsManagerCommands(self.session)
        LOGGER.write('SMConsoleManager - set_initial_values - Clearing screen widgets and adding initial secret names to menu.')
        self.manager.root.set_status_bar_text('Backspace - Console Selection | Refresh - r | Menu - m | Copy Displayed Secret Value to Clipboard - c | h - Show help menu | Quit - q')
        self.clear_elements()
        self.sm_secrets_menu.set_title(self.manager.default_region)
        self.display_secret_names()


    def set_initial_focus(self):
        """Override of base function. Sets initial focus to the resource select box.
        """

        LOGGER.write('EC2ConsoleManager - set_initial_focus - Setting initial focus')
        self.manager.root.move_focus(self.sm_secrets_menu)    

    
    def display_secret_names(self):
        """Function that gets the secret names from the AWS Secrets Manager.

        Returns
        -------
        list
            The secret names.
        """

        LOGGER.write('SMConsoleManager - display_secret_names')
        secret_names = self.sm_commands.get_secret_names()
        self.sm_secrets_menu.clear()
        if secret_names == []:
            LOGGER.write('SMConsoleManager - display_secret_names - No secret names found.')
            self.sm_info_text_block.set_text('No secrets found.')
        elif isinstance(secret_names, str) and secret_names.startswith('Error'):
            LOGGER.write('SMConsoleManager - display_secret_names - Error getting secret names. Error: {}'.format(secret_names))
            self.sm_info_text_block.set_text(secret_names)
        elif secret_names:
            LOGGER.write('SMConsoleManager - display_secret_names - Secret names: {}'.format(secret_names))
            self.sm_secrets_menu.add_item_list(secret_names)
            LOGGER.write('SMConsoleManager - display_secret_names - Setting current secret name to first in list: {}'.format(secret_names[0]))
            self.current_secret_name = secret_names[0]
        else:
            LOGGER.write('SMConsoleManager - display_secret_names - Error getting secret names.')
            self.sm_info_text_block.set_text('Error getting secret names.')
    

    def display_secret_versions(self):
        """Function that gets the secret versions from the AWS Secrets Manager.

        Returns
        -------
        list
            The secret versions.
        """

        secret_name = self.sm_secrets_menu.get()
        self.current_secret_name = secret_name
        LOGGER.write('SMConsoleManager - display_secret_versions - Secret name: {}'.format(self.current_secret_name))
        secret_versions = self.sm_commands.get_all_secret_versions(self.current_secret_name)
        self.sm_secret_versions_menu.clear()
        self.sm_info_text_block.clear()
        if secret_versions == []:
            LOGGER.write('SMConsoleManager - display_secret_versions - No secret versions found.')
            self.sm_info_text_block.set_text('No secret versions found.')
        elif isinstance(secret_versions, str) and secret_versions.startswith('Error'):
            LOGGER.write('SMConsoleManager - display_secret_names - Error getting secret names. Error: {}'.format(secret_versions))
            self.sm_info_text_block.set_text(secret_versions)
        elif secret_versions:
            LOGGER.write('SMConsoleManager - display_secret_versions - Secret versions: {}'.format(secret_versions))
            self.sm_secret_versions_menu.add_item_list(secret_versions)
            LOGGER.write('SMConsoleManager - display_secret_versions - Setting current secret version to first in list: {}'.format(secret_versions[0]))
            self.current_secret_version = secret_versions[0]
            LOGGER.write('SMConsoleManager - display_secret_versions - Opening first secret value.')
            self.display_secret_value()
        else:
            LOGGER.write('SMConsoleManager - display_secret_versions - Error getting secret versions.')
            self.sm_info_text_block.set_text('Error getting secret versions.')

    def set_current_secret_version(self):
        """Function that sets the current secret version.
        """

        secret_version = self.sm_secret_versions_menu.get()
        self.current_secret_version = secret_version
        LOGGER.write('SMConsoleManager - set_current_secret_version - Secret version: {}'.format(self.current_secret_version))
        LOGGER.write('SMConsoleManager - set_current_secret_version - Opening secret value.')
        self.display_secret_value()


    def display_secret_value(self):
        """Function that gets the secret value from the AWS Secrets Manager.

        Returns
        -------
        dict
            The secret value.
        """

        secret_name = self.current_secret_name
        version_id = self.current_secret_version
        LOGGER.write('SMConsoleManager - display_secret_value - Secret name: {}, Version ID: {}'.format(secret_name, version_id))
        self.sm_info_text_block.clear()
        self.sm_value_text_block.clear()
        secret = self.sm_commands.get_secret_version_data(secret_name, version_id)
        if isinstance(secret, str) and secret.startswith('Error'):
            LOGGER.write('SMConsoleManager - display_secret_value - Error fetching {}.'.format(secret))
            self.sm_value_text_block.set_text(secret)
            return
        secret_table = self.build_secret_data_table(secret)
        # Intenionally not logging secret data.
        if secret_table:
            LOGGER.write('SMConsoleManager - display_secret_value - Setting secret details table.')
            self.sm_info_text_block.set_text(secret_table)
            try:
                LOGGER.write('SMConsoleManager - display_secret_value - Attempting to prettify secret value as JSON.')
                secret_value = json.loads(secret['SecretString'])
                pretty_secret_value = json.dumps(secret_value, indent=4, sort_keys=True)
                # Colorize the JSON key/value pairs. Thanks again GPT!   Only the first one is being applied. Second one is being ignored. Not sure why.
                self.sm_value_text_block.add_text_color_rule(r'": \"(\w+)\"', py_cui.RED_ON_BLACK, rule_type='contains', match_type='regex') # Matches all JSON values.
                self.sm_value_text_block.add_text_color_rule(r'\"(\w+)\":', py_cui.GREEN_ON_BLACK, rule_type='contains', match_type='regex') # Matches all JSON keys.
            except json.decoder.JSONDecodeError:
                LOGGER.write('SMConsoleManager - display_secret_value - Secret value is not JSON. Setting as is.')
                pretty_secret_value = secret['SecretString']
            self.sm_value_text_block.set_text(pretty_secret_value)
        else:
            LOGGER.write('SMConsoleManager - display_secret_value - Error getting secret details.')
            self.sm_info_text_block.set_text('Error getting secret details.')
            self.sm_value_text_block.set_text('Error getting secret value.')


    def build_secret_data_table(self, secret_data):
        """Function that builds the secret value table.

        Parameters
        ----------
        secret_data : dict
            The secret version metadata.

        Returns
        -------
        list
            The secret value table.
        """

        # This is meant to return some error text in case secret data isn't properly provided. 
        # Not sure if this works. Need to test.
        if secret_data == '':
            LOGGER.write('SMConsoleManager - build_secret_data_table - No secret data provided.')
            secret_data = "No secret data provided."
            return secret_data

        LOGGER.write('SMConsoleManager - build_secret_data_table - Building secret data table.')
        table = [
            ['Name', secret_data['Name']],
            ['ARN', secret_data['ARN']],
            ['Version Stages', secret_data['VersionStages']],
            ['Created Date', secret_data['CreatedDate']],
        ]
        return tabulate(table, headers='firstrow', tablefmt='fancy_grid')


    def copy_current_secret_value_to_clipboard(self):
        """Function that copies the current secret value to the clipboard.

        Returns
        -------
        str
            The secret value.
        """
        LOGGER.write('SMConsoleManager - copy_current_secret_value_to_clipboard')
        secret_value = self.sm_value_text_block.get()
        pyperclip.copy(secret_value)


    def get_logo_text(self):
        """Generates ascii-art version of pyaws logo

        Returns
        -------
        logo : str
            ascii-art logo
        """

        LOGGER.write('PyAWSManager - get_logo_text - Generating logo text')
        logo =  "  __  ___ ______ ___ _____  __       \n"
        logo += "/' _/| __/ _/ _ \\ __|_   _/' _/      \n"
        logo += "`._`.| _| \\_| v / _|  | | `._`.      \n"
        logo += "|___/|___\\__/_|_\\___|_|_|_|___/ ___  \n"
        logo += " |  V  |/  \\|  \\| |/  \\ / _] __| _ \\ \n"
        logo += " | \\_/ | /\\ | | ' | /\\ | [/\\ _|| v / \n"
        logo += " |_| |_|_||_|_|\\__|_||_|\\__/___|_|_\\ \n"
        return logo


    def show_help_text(self):
        """Function that shows the help text for the SM Console screen.
        """

        LOGGER.write('SMConsoleManager - show_help_text')
        help_text = self.get_help_text()
        self.sm_info_text_block.clear()
        self.sm_value_text_block.clear()
        self.sm_value_text_block.set_text(help_text)


    def get_help_text(self):
        """Generates help text for SM Console screen

        Returns
        -------
        help_text : str
            The help text for the SM Console screen
        """

        LOGGER.write('SMConsoleManager - get_help_text')
        help_text = 'SecretsManager Console Help\n\n'
        help_text += 'Use the arrow keys to navigate the resource selection menu.\n\n'
        help_text += 'Shortcuts:\n'
        help_text += 'ENTER - Select Menu Option.\n'
        help_text += 'BACKSPACE - Return to Account Console.\n'
        help_text += 'c - Copy Displayed Secret Value to Clipboard\n'
        help_text += 'r - Refresh\n'
        help_text += 'h - Show Help Text\n'
        help_text += 'm - Open Menu\n'
        help_text += 'q - Exit\n'
        help_text += '\n'
        help_text += 'Inside Resource Selection:\n'
        help_text += 'ENTER - Select Resource.\n'

        return help_text