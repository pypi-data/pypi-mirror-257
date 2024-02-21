"""File containing functions used by the Systems Manager console screen.

This file is meant to handle the AWS SSM CUI elements and connections 
to the underlying AWS SSM commands found in pyaws.aws.systems_manager.ssm_commands.
"""

import pyperclip

import py_cui
import pyaws
import pyaws.screen_manager
import pyaws.logger as LOGGER
import pyaws.aws.systems_manager.ssm_commands as SSM
from pyaws.aws.systems_manager.ssm_tables import SSMConsoleTables as SSMTables


class SSMConsoleManager(pyaws.screen_manager.ScreenManager):
    """Class used to manage the Systems Manager console screen.

    This class provides functions used by pyaws to manage the Systems Manager Console CUI screen.
    It provides the interface between the SSM Console CUI screen and the underlying
    aws commands found in pyaws.aws. It inherits from the ScreenManager class, which provides
    the basic functionality for all screen managers in pyaws.

    Attributes
    ----------
    menu_choices : list of str
        Overriden list of menu choices accessible from the account select menu
    """

    def __init__(self, top_manager):
        """Constructor for SSMConsoleManager class.
        """

        super().__init__(top_manager, 'SSM Console')
        self.ssm_tables = SSMTables()
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
        
        LOGGER.write('SSMConsoleManager - process_menu_selection - Selection: {}'.format(selection))
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
        """Function that initialize the widgets for the SSM Console Screen. Overrides base class function.

        Returns
        -------
        ssm_console_manager_widget_set : py_cui.widget_set.WidgetSet
            The widget set for the SSM Console Screen
        """

        LOGGER.write('SSMConsoleManager - initialize_screen_elements')
        ssm_console_manager_widget_set = self.manager.root.create_new_widget_set(12, 9)

        # Base Keyboard Bindings
        ssm_console_manager_widget_set.add_key_command(py_cui.keys.KEY_BACKSPACE, self.manager.open_account_console_window)
        # ssm_console_manager_widget_set.add_key_command(py_cui.keys.KEY_R_LOWER, self.refresh_status)
        # ssm_console_manager_widget_set.add_key_command(py_cui.keys.KEY_S_LOWER, self.manager.open_settings_window)
        ssm_console_manager_widget_set.add_key_command(py_cui.keys.KEY_C_LOWER, self.copy_current_parameter_value_to_clipboard)
        ssm_console_manager_widget_set.add_key_command(py_cui.keys.KEY_H_LOWER, self.show_help_text)
        ssm_console_manager_widget_set.add_key_command(py_cui.keys.KEY_M_LOWER, self.show_menu)

        # SSM Console Menu
        self.ssm_resource_menu = ssm_console_manager_widget_set.add_scroll_menu('Menu', 1, 0, row_span=3, column_span=2)
        self.ssm_resource_menu.add_key_command(py_cui.keys.KEY_BACKSPACE, self.manager.open_account_console_window)
        self.ssm_resource_menu.add_key_command(py_cui.keys.KEY_ENTER, self.fetch_ssm_resource_list)
        self.ssm_resource_menu.add_key_command(py_cui.keys.KEY_C_LOWER, self.copy_current_parameter_value_to_clipboard)
        self.ssm_resource_menu.add_key_command(py_cui.keys.KEY_H_LOWER, self.show_help_text)
        self.ssm_resource_menu.add_key_command(py_cui.keys.KEY_Q_LOWER, self.manager.clean_exit)
        self.ssm_resource_menu.add_item_list(self.available_resources())
        self.ssm_resource_menu.add_text_color_rule('.*', py_cui.CYAN_ON_BLACK, rule_type='contains', match_type='line') # Not working.

        # SSM Resource List from selected resource selection
        self.ssm_resource_list_menu = ssm_console_manager_widget_set.add_scroll_menu('Resources', 4, 0, row_span=8, column_span=2)
        self.ssm_resource_list_menu.add_key_command(py_cui.keys.KEY_BACKSPACE, self.manager.open_account_console_window)
        self.ssm_resource_list_menu.add_key_command(py_cui.keys.KEY_C_LOWER, self.copy_current_parameter_value_to_clipboard)
        self.ssm_resource_list_menu.add_key_command(py_cui.keys.KEY_H_LOWER, self.show_help_text)
        self.ssm_resource_list_menu.add_key_command(py_cui.keys.KEY_Q_LOWER, self.manager.clean_exit)
        self.ssm_resource_list_menu.add_text_color_rule('.*', py_cui.MAGENTA_ON_BLACK, rule_type='contains', match_type='line')

        # Main Info Text Block
        self.ssm_resource_info_text_block = ssm_console_manager_widget_set.add_text_block('Details', 0, 2, row_span=4, column_span=7)
        # Colorize all text (skips all table formatting). Obviously there is no way I figured this out myself. Thanks GPT!
        self.ssm_resource_info_text_block.add_text_color_rule('│ ([^│]+)', py_cui.GREEN_ON_BLACK, rule_type='contains', match_type='regex')
        # self.ssm_resource_info_text_block.add_text_color_rule('(?<=\│ )[^│]*(?= )', py_cui.GREEN_ON_BLACK, rule_type='contains', match_type='regex')

        # Secondary Info Text Block
        self.ssm_secondary_resource_info_text_block = ssm_console_manager_widget_set.add_text_block('Details', 4, 2, row_span=8, column_span=7)
        self.ssm_secondary_resource_info_text_block.add_text_color_rule('.*', py_cui.RED_ON_BLACK, rule_type='contains', match_type='line')

        # self.custom_command_input_box = ssm_console_manager_widget_set.add_text_box('Custom Command Bar', 11, 0, row_span=1, column_span=9, initial_text='aws ssm help')

        self.logo_label = ssm_console_manager_widget_set.add_block_label(self.get_logo_text(), 0, 0, row_span=2, column_span=2, center=True)
        self.logo_label.set_color(py_cui.CYAN_ON_BLACK)
        self.logo_label.set_selectable(False)

        return ssm_console_manager_widget_set
    
    def available_resources(self):
        """Function to return a list of available SSM resources.

        Returns
        -------
        list
            A list of available SSM resources.
        """
        
        LOGGER.write('SSMConsoleManager - available_resources')
        available_resources = ['Paramaters']
                                # 'Documents',
                                # 'Automation',
                                # 'Run Command',
                                # 'Session Manager',
                                # 'Inventory',
                                # 'Patch Manager',
                                # 'Distributor',
                                # 'Maintenance Windows',
                                # 'Resource Groups',
                                # 'Explorer',
                                # 'OpsCenter',
                                # 'Fleet Manager',
                                # 'Application Manager',
                                # 'Change Manager',
                                # 'Service Catalog',
                                # 'Quick Setup',
                                # 'Inventory',
                                # 'Compliance',
                                # 'Resource Data Sync',
                                # 'Explorer',
                                # 'OpsCenter',
                                # 'Fleet Manager',
                                # 'Application Manager',
                                # 'Change Manager',
                                # 'Service Catalog',
                                # 'Quick Setup',
                                # 'Inventory',
                                # 'Compliance',
                                # 'Resource Data Sync']
        return available_resources


    # May need a rewrite. Written in haste.
    def refresh_status(self):
        """Function that refreshes the status of the SSM Console screen.
        """

        LOGGER.write('SSMConsoleManager - refresh_status')


    def clear_elements(self):
        """Function that clears the widgets for the SSM Console screen.
        """

        LOGGER.write('SSMConsoleManager - clear_elements')
        self.ssm_resource_menu.clear()
        self.ssm_resource_list_menu.clear()
        self.ssm_resource_info_text_block.clear()
        # self.custom_command_input_box.clear()


    def clear_resource_elements(self):
        """Function that clears the widgets for the SSM Console screen.
        """

        LOGGER.write('SSMConsoleManager - clear_resource_elements')
        self.ssm_resource_list_menu.clear()
        self.ssm_resource_info_text_block.clear()
        # self.custom_command_input_box.clear()


    def set_initial_values(self):
        """Function that sets the initial values for the SSM Console screen.
        """

        LOGGER.write('SSMConsoleManager - set_initial_values')
        self.manager.current_screen = 'systemsmanager'
        LOGGER.write('SSMConsoleManager - set_initial_values - Set current_screen: {}'.format(self.manager.current_screen))
        self.session = self.manager.session
        self.ssm_commands = SSM.SSMCommands(self.session)
        self.current_resource_id = None
        self.clear_elements()
        self.ssm_resource_menu.add_item_list(self.available_resources())
        self.ssm_resource_list_menu.set_title(self.manager.default_region)
        # self.clear_resource_elements()


    def set_initial_focus(self):
        """Override of base function. Sets initial focus to the resource select box.
        """

        LOGGER.write('EC2ConsoleManager - set_initial_focus - Setting initial focus')
        self.manager.root.move_focus(self.ssm_resource_menu)    


    def fetch_ssm_resource_list(self):
        """Function to parse and fetch teh SSM resource list associated
            with the selected SSM resource.
        """

        LOGGER.write('SSMConsoleManager - fetch_ssm_resource_list')
        selected_resource = self.ssm_resource_menu.get()
        LOGGER.write('SSMConsoleManager - fetch_ssm_resource_list - Selected Resource: {}'.format(selected_resource))
        if selected_resource == 'Paramaters':
            self.display_resource_menu('Parameters', self.ssm_commands.get_all_parameters, self.ssm_commands.get_parameter, self.ssm_tables.build_parameters_details_table)
        else:
            self.manager.open_not_supported_popup(selected_resource)
    

    def process_resource_menu(self, resources, resource_type):
        """Function to parse the resource menu for resources.

        Parameters
        ----------
        resources : list of dict
            The list of resources to parse
        resource_type : str
            The type of the resources

        Returns
        -------
        resource_ids : list of str
            The IDs of the resources in the current session
        resource_list : list of str
            The list of resources to display in the menu
        """

        if resource_type == 'Parameters':
            resources = resources['Parameters']
            resource_ids = [resource['Name'] for resource in resources]
            resource_list = resource_ids
        else:
            resource_ids = [resource.id for resource in resources]
            resource_list = resource_ids

        if resource_ids:
            self.current_resource_id = resource_ids[0]
        return resource_ids, resource_list


    def display_resource_menu(self, resource_type, get_resources, get_resource_details, build_resource_details_table):
        """Function to fetch the resources in the current session.

        Parameters
        ----------
        resource_type : str
            The type of resource to fetch
        get_resources : function
            The function to call to fetch the resources
        get_resource_details : function
            The function to call to fetch the details of the selected resource
        build_resource_details_table : function
            The function to call to build the details table for the selected resource
        
        Returns
        -------
        resource_ids : list of str
            The IDs of the resources in the current session
        """

        LOGGER.write('SSMConsoleManager - display_resource_menu')
        self.clear_resource_elements()
        resources = get_resources()
        if resources == []:
            LOGGER.write('SSMConsoleManager - display_resource_menu - No {} Found'.format(resource_type))
            self.ssm_resource_info_text_block.set_text('No {} Found'.format(resource_type))
            return
        if isinstance(resources, str) and resources.startswith('Error'):
            LOGGER.write('SSMConsoleManager - display_{}_menu - Error fetching {}.'.format(resource_type, resource_type))
            self.ssm_resource_info_text_block.set_text(resources)
            return
        LOGGER.write('SSMConsoleManager - display_{}_menu - Fetching {} - {}: {}'.format(resource_type, resource_type, resource_type, resources))
        resource_ids, resource_list = self.process_resource_menu(resources, resource_type)
        if resource_ids:
            LOGGER.write('SSMConsoleManager - display_{}_menu - Adding {} IDs to SSM Resource List Menu'.format(resource_type, resource_type))
            self.ssm_resource_list_menu.add_item_list(resource_list)
            self.ssm_resource_list_menu.add_key_command(py_cui.keys.KEY_ENTER, lambda: self.set_current_resource_id(resource_type, get_resource_details, build_resource_details_table))
            self.display_resource_details(resource_type, get_resource_details, build_resource_details_table)
        elif resource_ids == []:
            LOGGER.write('SSMConsoleManager - display_{}_menu - No {} found.'.format(resource_type, resource_type))
            self.ssm_resource_info_text_block.set_text('No {} found.'.format(resource_type))
        else:
            LOGGER.write('SSMConsoleManager - display_{}_menu - Error fetching {}.'.format(resource_type, resource_type))
            self.ssm_resource_info_text_block.set_text('Error fetching {}.'.format(resource_type))
    

    def set_current_resource_id(self, resource_type, get_resource_details, build_resource_details_table):
        """Function to set the current resource id.

        Parameters
        ----------
        resource_type : str
            The type of resource to fetch
        get_resource_details : function
            The function to call to fetch the details of the selected resource
        build_resource_details_table : function
            The function to call to build the details table for the selected resource
        
        Returns
        -------
        resource_details : str
            The details of the selected resource
        """

        LOGGER.write('SSMConsoleManager - set_current_{}_id'.format(resource_type))
        selected_resource = self.ssm_resource_list_menu.get()
        selected_resource_id = selected_resource
        LOGGER.write('SSMConsoleManager - set_current_{}_id - Selected {}: {}'.format(resource_type, resource_type, selected_resource_id))
        self.current_resource_id = selected_resource_id
        self.display_resource_details(resource_type, get_resource_details, build_resource_details_table)


    def display_resource_details(self, resource_type, get_resource_details, build_resource_details_table):
        """Function to fetch the details of the selected resource.

        Parameters
        ----------
        resource_type : str
            The type of resource to fetch
        get_resource_details : function
            The function to call to fetch the details of the selected resource
        build_resource_details_table : function
            The function to call to build the details table for the selected resource
        
        Returns
        -------
        resource_details : str
            The details of the selected resource
        """

        LOGGER.write('SSMConsoleManager - display_{}_details'.format(resource_type))
        selected_resource_id = self.current_resource_id
        LOGGER.write('SSMConsoleManager - display_{}_details - Selected {}: {}'.format(resource_type, resource_type, selected_resource_id))
        resource = get_resource_details(selected_resource_id)
        self.ssm_resource_info_text_block.clear()
        if resource == []:
            LOGGER.write('SSMConsoleManager - display_{}_details - No details found for {}: {}'.format(resource_type, resource_type, selected_resource_id))
            self.ssm_resource_info_text_block.set_text('{} details not found for {}'.format(resource_type, selected_resource_id))
        elif isinstance(resource, str) and resource.startswith('Error'):
            LOGGER.write('SSMConsoleManager - display_{}_menu - Error fetching {}.'.format(resource_type, resource_type))
            self.ssm_resource_info_text_block.set_text(resource)
        elif resource:
            LOGGER.write('SSMConsoleManager - display_{}_details - Adding {} Details to SSM Resource Info Text Block'.format(resource_type, resource_type))
            resource_details = build_resource_details_table(resource)
            LOGGER.write('SSMConsoleManager - display_{}_details - {} Details: {}'.format(resource_type, resource_type, resource_details))
            self.ssm_resource_info_text_block.set_text(resource_details)
            if resource_type == 'Parameters':
                LOGGER.write('SSMConsoleManager - display_{}_details - Adding {} Details to SSM Secondary Resource Info Text Block'.format(resource_type, resource_type))
                parameter_value = resource.get('Parameter', {}).get('Value')
                self.ssm_secondary_resource_info_text_block.set_text(parameter_value)
        else:
            LOGGER.write('SSMConsoleManager - display_{}_details - Error fetching {} details: {}'.format(resource_type, resource_type, selected_resource_id))
            self.ssm_resource_info_text_block.set_text('Error fetching {} details. {}'.format(resource_type, selected_resource_id))


    def copy_current_parameter_value_to_clipboard(self):
        """Function that copies the current secret value to the clipboard.

        Returns
        -------
        str
            The secret value.
        """
        LOGGER.write('SMConsoleManager - copy_current_secret_value_to_clipboard')
        secret_value = self.ssm_secondary_resource_info_text_block.get()
        pyperclip.copy(secret_value)


    def get_logo_text(self):
        """Generates ascii-art version of pyaws logo

        Returns
        -------
        logo : str
            ascii-art logo
        """

        LOGGER.write('SSMConsoleManager - get_logo_text - Generating logo text')
        logo =  ' _____ __ __ _____ _____ _____ _____  \n'
        logo += '|   __|  |  |   __|     |  _  |   | | \n'
        logo += '|__   |_   _|__   | | | |     | | | | \n'
        logo += '|_____| |_| |_____|_|_|_|__|__|_|___| \n'
        return logo


    def show_help_text(self):
        """Function that shows the help text for the SSM Console screen.
        """

        LOGGER.write('SSMConsoleManager - show_help_text')
        help_text = self.get_help_text()
        self.ssm_resource_info_text_block.clear()
        self.ssm_secondary_resource_info_text_block.clear()
        self.ssm_secondary_resource_info_text_block.set_text(help_text)


    def get_help_text(self):
        """Generates help text for SSM Console screen

        Returns
        -------
        help_text : str
            The help text for the SSM Console screen
        """

        LOGGER.write('SSMConsoleManager - get_help_text')
        help_text = 'Systems Manager Console Help\n\n'
        help_text += 'Use the arrow keys to navigate the resource selection menu.\n\n'
        help_text += 'Shortcuts:\n'
        help_text += 'ENTER - Select Menu Option.\n'
        help_text += 'BACKSPACE - Return to Account Console.\n'
        help_text += 'c - Copy Current Parameter Value to Clipboard\n'
        help_text += 'h - Show Help Text\n'
        help_text += 'm - Open Menu\n'
        help_text += 'q - Exit\n'
        help_text += '\n'
        help_text += 'Inside Resource Selection:\n'
        help_text += 'ENTER - Select Resource.\n'

        return help_text