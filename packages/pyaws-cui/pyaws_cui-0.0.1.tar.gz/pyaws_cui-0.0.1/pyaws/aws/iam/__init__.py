"""File containing functions used by the IAM Console CUI screen.

This file is meant to handle the AWS IAM CUI elements and connections 
to the underlying AWS IAM commands found in pyaws.aws.iam.commands.
"""

import py_cui
import pyaws
import pyaws.screen_manager
import pyaws.logger as LOGGER
import pyaws.aws.iam.iam_commands as IAM
from pyaws.aws.iam.iam_tables import IAMConsoleTables as IAMTables


class IAMConsoleManager(pyaws.screen_manager.ScreenManager):
    """Class responsible for managing IAM Console CUI screen.

    This class provides functions used by pyaws to manage the IAM Console CUI screen.
    It provides the interface between the IAM Console CUI screen and the underlying
    aws commands found in pyaws.aws. It inherits from the ScreenManager class, which provides
    the basic functionality for all screen managers in pyaws.

    Attributes
    ----------
    menu_choices : list of str
        Overriden list of menu choices accessible from the account select menu
    """

    def __init__(self, top_manager):
        """Constructor for IAMConsoleManager class.
        """

        super().__init__(top_manager, 'IAM Console')
        self.iam_tables = IAMTables()
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
        
        LOGGER.write('IAMConsoleManager - process_menu_selection - Selection: {}'.format(selection))
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
        """Function that initialize the widgets for the IAM Console Screen. Overrides base class function.

        Returns
        -------
        iam_console_manager_widget_set : py_cui.widget_set.WidgetSet
            The widget set for the IAM Console Screen
        """
        
        LOGGER.write('IAMConsoleManager - initialize_screen_elements')
        iam_console_manager_widget_set = self.manager.root.create_new_widget_set(12, 9)

        # Base Keyboard Bindings
        iam_console_manager_widget_set.add_key_command(py_cui.keys.KEY_BACKSPACE, self.manager.open_account_console_window)
        # iam_console_manager_widget_set.add_key_command(py_cui.keys.KEY_R_LOWER, self.refresh_status)
        # iam_console_manager_widget_set.add_key_command(py_cui.keys.KEY_S_LOWER, self.manager.open_settings_window)
        iam_console_manager_widget_set.add_key_command(py_cui.keys.KEY_H_LOWER, self.show_help_text)
        iam_console_manager_widget_set.add_key_command(py_cui.keys.KEY_M_LOWER, self.show_menu)
        iam_console_manager_widget_set.add_key_command(py_cui.keys.KEY_Q_LOWER, self.manager.clean_exit)

        # IAM Console Menu
        self.iam_resource_menu = iam_console_manager_widget_set.add_scroll_menu('Menu', 1, 0, row_span=3, column_span=2)
        self.iam_resource_menu.add_key_command(py_cui.keys.KEY_ENTER, self.fetch_iam_resource_list)
        self.iam_resource_menu.add_key_command(py_cui.keys.KEY_BACKSPACE, self.manager.open_account_console_window)
        self.iam_resource_menu.add_key_command(py_cui.keys.KEY_H_LOWER, self.show_help_text)
        self.iam_resource_menu.add_key_command(py_cui.keys.KEY_Q_LOWER, self.manager.clean_exit)
        self.iam_resource_menu.add_item_list(self.available_resources())
        self.iam_resource_menu.add_text_color_rule('.*', py_cui.CYAN_ON_BLACK, rule_type='contains', match_type='line')

        # IAM Resource List from selected resource selection
        self.iam_resource_list_menu = iam_console_manager_widget_set.add_scroll_menu('Resources', 4, 0, row_span=8, column_span=2)
        self.iam_resource_list_menu.add_key_command(py_cui.keys.KEY_H_LOWER, self.show_help_text)
        self.iam_resource_list_menu.add_key_command(py_cui.keys.KEY_Q_LOWER, self.manager.clean_exit)
        self.iam_resource_list_menu.add_text_color_rule('.*', py_cui.MAGENTA_ON_BLACK, rule_type='contains', match_type='line')

        # Main Info Text Block
        self.iam_resource_info_text_block = iam_console_manager_widget_set.add_text_block('Details', 0, 2, row_span=12, column_span=7)
        # Colorize all text (skips all table formatting). Obviously there is no way I figured this out myself. Thanks GPT!
        self.iam_resource_info_text_block.add_text_color_rule('│ ([^│]+)', py_cui.GREEN_ON_BLACK, rule_type='contains', match_type='regex')
        # self.iam_resource_info_text_block.add_text_color_rule('(?<=\│ )[^│]*(?= )', py_cui.GREEN_ON_BLACK, rule_type='contains', match_type='regex')

        # self.custom_command_input_box = iam_console_manager_widget_set.add_text_box('Custom Command Bar', 11, 0, row_span=1, column_span=9, initial_text='aws iam help')

        self.logo_label = iam_console_manager_widget_set.add_block_label(self.get_logo_text(), 0, 0, row_span=1, column_span=2, center=True)
        self.logo_label.set_color(py_cui.CYAN_ON_BLACK)
        self.logo_label.set_selectable(False)

        return iam_console_manager_widget_set


    def available_resources(self):
        """Function to return a list of available IAM resources.

        Returns
        -------
        list
            A list of available IAM resources.
        """
        
        LOGGER.write('IAMConsoleManager - available_resources')
        available_resources = ['Users', 
                                'Groups', 
                                'Roles', 
                                'Policies']
        return available_resources


    def refresh_status(self):
        """Function that refreshes the status of the IAM Console screen.
        """

        LOGGER.write('IAMConsoleManager - refresh_status')
        # this should call self.manager.open_resource_console_window. However, open_resource_console_window needs to be rewritten to use current_state for selection choice; this requires a greater rewrite. noted in to-do.
        # self.manager.open_resource_console_window()


    def clear_elements(self):
        """Function that clears the widgets for the IAM Console screen.
        """

        LOGGER.write('IAMConsoleManager - clear_elements')
        self.iam_resource_menu.clear()
        self.iam_resource_list_menu.clear()
        self.iam_resource_info_text_block.clear()
        # self.custom_command_input_box.clear()


    def clear_resource_elements(self):
        """Function that clears the widgets for the IAM Console screen.
        """

        LOGGER.write('IAMConsoleManager - clear_resource_elements')
        self.iam_resource_list_menu.clear()
        self.iam_resource_info_text_block.clear()
        # self.custom_command_input_box.clear()


    def set_initial_values(self):
        """Function that sets the initial values for the IAM Console screen.
        """

        LOGGER.write('IAMConsoleManager - set_initial_values')
        self.manager.current_screen = 'iam'
        LOGGER.write('IAMConsoleManager - set_initial_values - Set current_screen: {}'.format(self.manager.current_screen))
        self.session = self.manager.session
        self.iam_commands = IAM.IAMCommands(self.session)
        self.current_resource_id = None
        self.clear_elements()
        self.iam_resource_menu.add_item_list(self.available_resources())
        self.iam_resource_list_menu.set_title(self.manager.default_region)
        # self.clear_resource_elements()


    def set_initial_focus(self):
        """Override of base function. Sets initial focus to the resource select box.
        """

        LOGGER.write('EC2ConsoleManager - set_initial_focus - Setting initial focus')
        self.manager.root.move_focus(self.iam_resource_menu)    


    def fetch_iam_resource_list(self):
        """Function to parse and fetch teh IAM resource list associated
            with the selected IAM resource.
        """

        LOGGER.write('IAMConsoleManager - fetch_iam_resource_list')
        selected_resource = self.iam_resource_menu.get()
        LOGGER.write('IAMConsoleManager - fetch_iam_resource_list - Selected Resource: {}'.format(selected_resource))
        if selected_resource == 'Users':
            self.display_resource_menu('Users', self.iam_commands.get_users, self.iam_commands.get_user_details, self.iam_tables.build_users_details_table)
        elif selected_resource == 'Groups':
            self.display_resource_menu('Groups', self.iam_commands.get_groups, self.iam_commands.get_group_details, self.iam_tables.build_groups_details_table)
        elif selected_resource == 'Roles':
            self.display_resource_menu('Roles', self.iam_commands.get_roles, self.iam_commands.get_role_details, self.iam_tables.build_roles_details_table)
        elif selected_resource == 'Policies':
            self.display_resource_menu('Policies', self.iam_commands.get_policies, self.iam_commands.get_policy_details, self.iam_tables.build_policies_details_table)
        else:
            self.manager.open_not_supported_popup(selected_resource)
    

    def process_resource_menu(self, resources, resource_type):
        """Function to parse the resource menu for resources.

        Parameters
        ----------
        resources : list of dict
            The list of resources to parse
        resource_type : str
            The type of the resourcess

        Returns
        -------
        resource_ids : list of str
            The IDs of the resources in the current session
        resource_list : list of str
            The list of resources to display in the menu
        """

        if resource_type == 'Policies':
            policies = resources['Policies']
            resource_ids = [policy['Arn'] for policy in policies]
            resource_list = []
            for policy in policies:
                policy_name = policy['PolicyName']
                policy_arn = policy['Arn']
                resource_list.append('{} - {}'.format(policy_name, policy_arn))
        elif resource_type == 'Roles':
            roles = resources['Roles']
            resource_ids = [role['RoleName'] for role in roles]
            resource_list = resource_ids
        elif resource_type == 'Groups':
            groups = resources['Groups']
            resource_ids = [group['GroupName'] for group in groups]
            resource_list = resource_ids
        elif resource_type == 'Users':
            users = resources['Users']
            resource_ids = [user['UserName'] for user in users]
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

        LOGGER.write('IAMConsoleManager - display_resource_menu')
        self.clear_resource_elements()
        resources = get_resources()
        if resources == []:
            LOGGER.write('IAMConsoleManager - display_resource_menu - No {} Found'.format(resource_type))
            self.iam_resource_info_text_block.set_text('No {} Found'.format(resource_type))
            return
        if isinstance(resources, str) and resources.startswith('Error'):
            LOGGER.write('IAMConsoleManager - display_{}_menu - Error fetching {}.'.format(resource_type, resource_type))
            self.iam_resource_info_text_block.set_text(resources)
            return
        LOGGER.write('IAMConsoleManager - display_{}_menu - Fetching {} - {}: {}'.format(resource_type, resource_type, resource_type, resources))
        resource_ids, resource_list = self.process_resource_menu(resources, resource_type)
        if resource_ids:
            LOGGER.write('IAMConsoleManager - display_{}_menu - Adding {} IDs to IAM Resource List Menu'.format(resource_type, resource_type))
            self.iam_resource_list_menu.add_item_list(resource_list)
            self.iam_resource_list_menu.add_key_command(py_cui.keys.KEY_ENTER, lambda: self.set_current_resource_id(resource_type, get_resource_details, build_resource_details_table))
            self.display_resource_details(resource_type, get_resource_details, build_resource_details_table)
        elif resource_ids == []:
            LOGGER.write('IAMConsoleManager - display_{}_menu - No {} found.'.format(resource_type, resource_type))
            self.iam_resource_info_text_block.set_text('No {} found.'.format(resource_type))
        else:
            LOGGER.write('IAMConsoleManager - display_{}_menu - Error fetching {}.'.format(resource_type, resource_type))
            self.iam_resource_info_text_block.set_text('Error fetching {}.'.format(resource_type))
    

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

        LOGGER.write('IAMConsoleManager - set_current_{}_id'.format(resource_type))
        selected_resource = self.iam_resource_list_menu.get()
        if resource_type == 'Policies':
            selected_resource_id = selected_resource.split(' - ')[1]
        else:
            selected_resource_id = selected_resource
        LOGGER.write('IAMConsoleManager - set_current_{}_id - Selected {}: {}'.format(resource_type, resource_type, selected_resource_id))
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

        LOGGER.write('IAMConsoleManager - display_{}_details'.format(resource_type))
        selected_resource_id = self.current_resource_id
        LOGGER.write('IAMConsoleManager - display_{}_details - Selected {}: {}'.format(resource_type, resource_type, selected_resource_id))
        resource = get_resource_details(selected_resource_id)
        self.iam_resource_info_text_block.clear()
        if resource == []:
            LOGGER.write('IAMConsoleManager - display_{}_details - No details found for {}: {}'.format(resource_type, resource_type, selected_resource_id))
            self.iam_resource_info_text_block.set_text('{} details not found for {}'.format(resource_type, selected_resource_id))
        elif isinstance(resource, str) and resource.startswith('Error'):
            LOGGER.write('IAMConsoleManager - display_{}_menu - Error fetching {}.'.format(resource_type, resource_type))
            self.iam_resource_info_text_block.set_text(resource)
        elif resource:
            LOGGER.write('IAMConsoleManager - display_{}_details - Adding {} Details to IAM Resource Info Text Block'.format(resource_type, resource_type))
            resource_details = build_resource_details_table(resource)
            LOGGER.write('IAMConsoleManager - display_{}_details - {} Details: {}'.format(resource_type, resource_type, resource_details))
            self.iam_resource_info_text_block.set_text(resource_details)
        else:
            LOGGER.write('IAMConsoleManager - display_{}_details - Error fetching {} details: {}'.format(resource_type, resource_type, selected_resource_id))
            self.iam_resource_info_text_block.set_text('Error fetching {} details. {}'.format(resource_type, selected_resource_id))
    

    def get_logo_text(self):
        """Generates ascii-art version of pyaws logo

        Returns
        -------
        logo : str
            ascii-art logo
        """

        LOGGER.write('IAMConsoleManager - get_logo_text - Generating logo text')
        logo =  ' _|_|_|    _|_|    _|      _|  \n'
        logo += '   _|    _|    _|  _|_|  _|_|  \n'
        logo += '   _|    _|_|_|_|  _|  _|  _|  \n'
        logo += ' _|_|_|  _|    _|  _|      _|  \n'
        return logo


    def show_help_text(self):
        """Function that shows the help text for the IAM Console screen.
        """

        LOGGER.write('IAMConsoleManager - show_help_text')
        help_text = self.get_help_text()
        self.iam_resource_info_text_block.clear()
        self.iam_resource_info_text_block.set_text(help_text)


    def get_help_text(self):
        """Generates help text for IAM Console screen

        Returns
        -------
        help_text : str
            The help text for the IAM Console screen
        """

        LOGGER.write('IAMConsoleManager - get_help_text')
        help_text = 'IAM Console Help\n\n'
        help_text += 'Use the arrow keys to navigate the resource selection menu.\n\n'
        help_text += 'Shortcuts:\n'
        help_text += 'ENTER - Select Menu Option.\n'
        help_text += 'BACKSPACE - Return to Account Console.\n'
        help_text += 'h - Show Help Text\n'
        help_text += 'm - Open Menu\n'
        help_text += 'q - Exit\n'
        help_text += '\n'
        help_text += 'Inside Resource Selection:\n'
        help_text += 'ENTER - Select Resource.\n'

        return help_text