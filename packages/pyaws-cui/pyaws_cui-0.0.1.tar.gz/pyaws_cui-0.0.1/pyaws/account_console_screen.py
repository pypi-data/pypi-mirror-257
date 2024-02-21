"""File containing functions used by the Account Console CUI screen.

This file is meant to handle the intermediate considerations between the 
CUI and the underlying aws commands found in pyaws.aws.
"""

from sys import platform
import datetime
import py_cui
import pyaws
import pyaws.screen_manager
import pyaws.aws as AWS
import pyaws.logger as LOGGER

class AccountConsoleManager(pyaws.screen_manager.ScreenManager):
    """Class used to manage functions for the Account Console CUI screen.

    This class provides the interface between the Account Console CUI screen and the underlying
    aws commands found in pyaws.aws. It inherits from the ScreenManager class, which provides
    the basic functionality for all screen managers in pyaws.
    
    Attributes
    ----------
    menu_choices : list of str
        Overriden list of menu choices accessible from the account select menu
    """

    def __init__(self, top_manager):
        """Constructor for AccountConsoleManager class.
        """

        super().__init__(top_manager, 'Account Console')
        self.menu_choices = ['(Re)Select Account',
                                'Settings',
                                'Exit']
        
    def process_menu_selection(self, selection):
        """Override of base class, executes depending on menu selection

        Parameters
        ----------
        selection : str
            The user's menu selection
        """

        LOGGER.write('AccountConsoleManager - process_menu_selection - Processing menu selection: {}'.format(selection))
        if selection == '(Re)Select Account':
            self.manager.open_account_select_window()
        elif selection == 'Settings':
            self.manager.open_settings_window()
        elif selection == 'Exit':
            self.manager.close_cleanup()
            exit()
        else:
            self.manager.open_not_supported_popup(selection)
    
    def initialize_screen_elements(self):
        """Override of base class function. Initializes Account Console widgets, returns screen widget set.
        
        Returns
        -------
        account_console_widget_set : py_cui.widget_set.WidgetSet
            Widget set object for Account Console screen
        """

        LOGGER.write('AccountConsoleManager - initialize_screen_elements - Initializing widgets')
        # Create widget set
        account_console_widget_set = self.manager.root.create_new_widget_set(7, 4)

        # Base keyboard shortcuts.
        account_console_widget_set.add_key_command(py_cui.keys.KEY_BACKSPACE,   self.manager.open_account_select_window)
        account_console_widget_set.add_key_command(py_cui.keys.KEY_R_LOWER,     self.refresh_status)
        account_console_widget_set.add_key_command(py_cui.keys.KEY_M_LOWER,     self.show_menu)
        # account_console_widget_set.add_key_command(py_cui.keys.KEY_H_LOWER,     self.show_help_overview)
        account_console_widget_set.add_key_command(py_cui.keys.KEY_Q_LOWER,     self.manager.clean_exit)

        # Create resource selection box
        self.resource_select_box = account_console_widget_set.add_scroll_menu('Consoles', 2, 1, row_span=3, column_span=1)
        self.resource_select_box.add_item_list(self.available_resources())
        self.resource_select_box.add_text_color_rule('.*', py_cui.RED_ON_BLACK, rule_type='contains', match_type='line')
        self.resource_select_box.add_key_command(py_cui.keys.KEY_BACKSPACE, self.manager.open_account_select_window)
        self.resource_select_box.add_key_command(py_cui.keys.KEY_ENTER,     self.manager.open_resource_console_window)
        # self.resource_select_box.add_key_command(py_cui.keys.KEY_ENTER,     self.open_console_window)
        self.resource_select_box.add_key_command(py_cui.keys.KEY_M_LOWER,   self.show_menu)
        self.resource_select_box.add_key_command(py_cui.keys.KEY_R_LOWER,   self.refresh_status)
        self.resource_select_box.add_key_command(py_cui.keys.KEY_Q_LOWER,   self.manager.clean_exit)
        self.resource_select_box.add_key_command(py_cui.keys.KEY_S_LOWER,   self.manager.open_settings_window)
        self.resource_select_box.set_focus_text('Return - Bcksp | Quit - q | Open Selected Console - Enter | Menu - m | Refresh Connection - r | Settings - s')

        self.region_menu = account_console_widget_set.add_scroll_menu('Regions', 2, 2, row_span=3, column_span=1)
        self.region_menu.add_item_list(self.manager.regions)
        self.region_menu.add_text_color_rule('.*', py_cui.RED_ON_BLACK, rule_type='contains', match_type='line')
        self.region_menu.add_key_command(py_cui.keys.KEY_ENTER,    self.update_default_region)
        self.region_menu.add_key_command(py_cui.keys.KEY_R_LOWER,  self.refresh_status)
        self.region_menu.add_key_command(py_cui.keys.KEY_M_LOWER,  self.show_menu)
        self.region_menu.add_key_command(py_cui.keys.KEY_Q_LOWER,  self.manager.clean_exit)
        self.region_menu.add_key_command(py_cui.keys.KEY_S_LOWER,  self.manager.open_settings_window)
        self.region_menu.add_key_command(py_cui.keys.KEY_A_LOWER,  self.manager.open_about_window)
        self.region_menu.add_key_command(py_cui.keys.KEY_L_LOWER,  self.manager.open_account_console_window)
        self.region_menu.set_focus_text('Quit - q | Set Region - Enter | Menu - m | Refresh - r | Settings - s')

        self.logo_label = account_console_widget_set.add_block_label(self.manager.get_logo_text(), 0, 1, row_span=1, column_span=2, center=True)
        self.logo_label.set_color(py_cui.CYAN_ON_BLACK)
        self.logo_label.set_selectable(False)

        # Create status box
        self.connection_status_box = account_console_widget_set.add_text_block('Status', 1, 1, row_span=1, column_span=2)
        self.connection_status_box.add_text_color_rule('.*', py_cui.MAGENTA_ON_BLACK, rule_type='contains', match_type='line')
        self.connection_status_box.set_selectable(False)

        # Create button widgets
        self.refresh_status_button = account_console_widget_set.add_button('Refresh', 5, 1, row_span=1, column_span=2, command=self.ask_refresh_status)

        # self.info_panel = self.connection_status_box

        # self.refresh_status()
        return account_console_widget_set
    

    def clear_elements(self):
        """Override of base class function, clears text fields
        """

        LOGGER.write('AccountConsoleManager - clear_elements - Clearing elements')
        self.connection_status_box.clear()
    

    def set_initial_values(self):
        """Override of base function. Sets some initial text for the widgets
        """

        LOGGER.write('AccountConsoleManager - set_initial_values - Setting initial values')
        self.manager.current_screen = 'console'
        LOGGER.write('AccountConsoleManager - set_initial_values - Set current_screen: {}'.format(self.manager.current_screen))
        if self.manager.default_profile is None:
            self.connection_status_box.set_text('No profile selected')
        else:
            self.connection_status_box.set_text('Profile: {}'.format(self.manager.default_profile))
        self.manager.root.set_status_bar_text('Return - Bcksp | Quit - q | Menu - m | Refresh Connection - r | Settings - s')
        self.refresh_status()


    def set_initial_focus(self):
        """Override of base function. Sets initial focus to the resource select box.
        """

        LOGGER.write('AccountConsoleManager - set_initial_focus - Setting initial focus')
        self.manager.root.move_focus(self.resource_select_box)


    def refresh_status(self):
        """Function that refreshes the status of the connection to the AWS account
        """

        LOGGER.write('AccountConsoleManager - refresh_status - Refreshing connection status')
        # self.manager.root.show_message_popup('Refresh', 'Refreshing connection status...\n')
        profile = self.manager.default_profile
        region = self.manager.default_region
        self.clear_elements()

        status_message = ''
        status_message = status_message + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n'
        if profile is None:
            status_message = 'No profile selected\n'
        else:
            status_message = status_message + 'Profile: {}\n'.format(profile)
            status_message = status_message + 'Region: {}\n'.format(region)
            if self.manager.establish_aws_connection():
                status_message = status_message + 'Connection Successful\n'
            else:
                status_message = status_message + 'Connection Failed\n'
        self.connection_status_box.set_text(status_message)

    def ask_refresh_status(self):
        """Function that refreshes the status of the connection to the AWS account on command.
        """
        
        LOGGER.write('AccountConsoleManager - ask_refresh_status - User requested connection refresh')
        self.refresh_status()


    def available_resources(self):
        """Function that returns a list of the available console screens.

        Returns
        -------
        list of str
            List of available console screens
        """

        available_resources = ['EC2',
                                'S3', 
                                'IAM', 
                                'Lambda',
                                'ECS',
                                'EKS',
                                'Route53',
                                'SystemsManager',
                                'SecretsManager', 
                                'RDS',
                                'DynamoDB',
                                'SimpleDB']
                                # 'CloudFormation', 
                                # 'CloudWatch', 
                                # 'CloudTrail']
        return available_resources


    def update_default_region(self):
        """Function that updates the default region based on user selection.
        """

        LOGGER.write('AccountConsoleManager - update_default_region - Updating default region')
        selected_region = self.region_menu.get()
        self.manager.update_default_region(region=selected_region)
        self.refresh_status()
        self.manager.root.show_message_popup('Region Set', 'Default region set to {}'.format(selected_region))


    # def open_console_window(self):
    #     """Function that opens the selected console window
    #     """

    #     # if self.manager.session is None:
    #     #     # LOGGER.write('PyAWSManager - open_resource_console_window - Session not set. Returning to account console window')
    #     #     self.manager.open_connection_not_established_popup()
    #     #     return

    #     # if self.manager.default_region == '' or self.manager.default_region is None:
    #     #     # LOGGER.write('PyAWSManager - open_resource_console_window - Region not set. Returning to account console window')
    #     #     self.manager.open_region_not_provied_popup()
    #     #     return

    #     LOGGER.write('AccountConsoleManager - open_console_window ')
    #     selected_resource = self.resource_select_box.get().lower()
    #     self.manager.current_screen = selected_resource
    #     LOGGER.write('AccountConsoleManager - open_console_window - Set current_screen: {}'.format(self.manager.current_screen))
    #     self.manager.open_resource_console_window()

    # def establish_connection(self):
    #     """Function that establishes a connection to the AWS account

    #     Returns
    #     -------
    #     bool
    #         True if connection successful, False otherwise
    #     """
    #     LOGGER.write('AccountConsoleManager - establish_connection - Initializing AWS Manager')
    #     self.aws_manager = AWS.AWSManager(self.manager.default_profile, self.manager.default_region)
        
    #     LOGGER.write('AccountConsoleManager - establish_connection - Establishing connection to {} in {}'.format(self.manager.default_profile, self.manager.default_region))
    #     self.connection_established = self.aws_manager.establish_aws_connection()

    #     if self.connection_established:
    #         LOGGER.write('AccountConsoleManager - establish_connection - Connection established')
    #         self.manager.session = self.aws_manager.session
    #         return self.connection_established
    #     elif not self.connection_established:
    #         LOGGER.write('AccountConsoleManager - establish_connection - Connection not established')
    #         return self.connection_established
