"""File containing functions used by the EC2 Console CUI screen.

This file is meant to handle the AWS EC2 CUI elements and connections 
to the underlying AWS EC2 commands found in pyaws.aws.ec2.commands.
"""

import py_cui
import pyaws
import pyaws.screen_manager
import pyaws.logger as LOGGER
import pyaws.aws.ec2.ec2_commands as EC2
from pyaws.aws.ec2.ec2_tables import EC2ConsoleTables as EC2Tables


# Helper Functions
def get_instance_name(instance_details):
    """Function to get parse name from Instance details.

    Parameters
    ----------
    instance_details : dict
        The instance_details to get the name from.
    
    Returns
    -------
    name : str
        The name of the instance.
    """

    LOGGER.write('EC2ConsoleManager - get_instance_name')
    for tag in instance_details.get('Tags', []):
        if tag['Key'] == 'Name':
            return tag['Value']
    return 'Unnamed'


class EC2ConsoleManager(pyaws.screen_manager.ScreenManager):
    """Class responsible for managing EC2 Console CUI screen.

    This class provides functions used by pyaws to manage the EC2 Console CUI screen.
    It provides the interface between the EC2 Console CUI screen and the underlying
    aws commands found in pyaws.aws. It inherits from the ScreenManager class, which provides
    the basic functionality for all screen managers in pyaws.

    Attributes
    ----------
    menu_choices : list of str
        Overriden list of menu choices accessible from the account select menu
    """

    def __init__(self, top_manager):
        """Constructor for EC2ConsoleManager class.
        """

        super().__init__(top_manager, 'EC2 Console')
        self.ec2_tables = EC2Tables()
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
        
        LOGGER.write('EC2ConsoleManager - process_menu_selection - Selection: {}'.format(selection))
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
        """Function that initialize the widgets for the EC2 Console screen. Overrides base class function.

        Returns
        -------
        ec2_console_manager_widget_set : py_cui.widget_set.WidgetSet
            Widget set object for EC2 Console screen
        """
        LOGGER.write('EC2ConsoleManager - initialize_screen_elements')

        # EC2 Console Screen Widgets and Keybindings
        ec2_console_manager_widget_set = self.manager.root.create_new_widget_set(12, 9)

        # Base Keyboard Bindings
        ec2_console_manager_widget_set.add_key_command(py_cui.keys.KEY_BACKSPACE, self.manager.open_account_console_window)
        # ec2_console_manager_widget_set.add_key_command(py_cui.keys.KEY_R_LOWER, self.refresh_status)
        ec2_console_manager_widget_set.add_key_command(py_cui.keys.KEY_H_LOWER, self.show_help_text)
        ec2_console_manager_widget_set.add_key_command(py_cui.keys.KEY_M_LOWER, self.show_menu)

        # EC2 Resource Selection List
        self.ec2_resource_menu = ec2_console_manager_widget_set.add_scroll_menu('Menu', 1, 0, row_span=3, column_span=2)
        self.ec2_resource_menu.add_item_list(self.available_ec2_resources())
        self.ec2_resource_menu.add_text_color_rule('.*', py_cui.CYAN_ON_BLACK, rule_type='contains', match_type='line')
        self.ec2_resource_menu.add_key_command(py_cui.keys.KEY_ENTER, self.fetch_ec2_resource_list)
        self.ec2_resource_menu.add_key_command(py_cui.keys.KEY_BACKSPACE, self.manager.open_account_console_window)
        self.ec2_resource_menu.add_key_command(py_cui.keys.KEY_H_LOWER, self.show_help_text)
        self.ec2_resource_menu.add_key_command(py_cui.keys.KEY_Q_LOWER, self.manager.clean_exit)

        # EC2 Resource List from selected resource selection
        self.ec2_resource_list_menu = ec2_console_manager_widget_set.add_scroll_menu('Resources', 4, 0, row_span=8, column_span=2) 
        self.ec2_resource_list_menu.add_text_color_rule('.*', py_cui.RED_ON_BLACK, rule_type='contains', match_type='line')
        self.ec2_resource_list_menu.add_key_command(py_cui.keys.KEY_BACKSPACE, self.manager.open_account_console_window)
        self.ec2_resource_list_menu.add_key_command(py_cui.keys.KEY_H_LOWER, self.show_help_text)
        self.ec2_resource_list_menu.add_key_command(py_cui.keys.KEY_Q_LOWER, self.manager.clean_exit)

        # EC2 Secondary Resource Selection List
        # self.ec2_resource_secondary_menu = ec2_console_manager_widget_set.add_scroll_menu('EC2 - Secondary', 4, 0, row_span=4, column_span=2)

        # EC2 Tertiary Resource Selection List
        # self.ec2_tertiary_resource_menu = ec2_console_manager_widget_set.add_scroll_menu('EC2 - Tertiary', 6, 0, row_span=2, column_span=2)

        # Main Info Text Block
        self.ec2_resource_info_text_block = ec2_console_manager_widget_set.add_text_block('Details', 0, 2, row_span=12, column_span=7)
        # Colorize all text (skips all table formatting). Obviously there is no way I figured this out myself. Thanks GPT!
        self.ec2_resource_info_text_block.add_text_color_rule('│ ([^│]+)', py_cui.GREEN_ON_BLACK, rule_type='contains', match_type='regex')
        # self.ec2_resource_info_text_block.add_text_color_rule('(?<=\│ )[^│]*(?= )', py_cui.GREEN_ON_BLACK, rule_type='contains', match_type='regex') # A more complicated regex pattern that caused failures on tables returning json data.

        # Custom command input box
        # self.custom_command_input_box = ec2_console_manager_widget_set.add_text_box('Custom Command Bar', 11, 0, row_span=1, column_span=9, initial_text='aws ec2 help')

        self.logo_label = ec2_console_manager_widget_set.add_block_label(self.get_logo_text(), 0, 0, row_span=1, column_span=2, center=True)
        self.logo_label.set_color(py_cui.CYAN_ON_BLACK)
        self.logo_label.set_selectable(False)

        return ec2_console_manager_widget_set


    def clear_elements(self):
        """Function that clears the widgets for the EC2 Console screen.
        """

        LOGGER.write('EC2ConsoleManager - clear_elements')
        self.ec2_resource_menu.clear()
        self.ec2_resource_list_menu.clear()
        self.ec2_resource_info_text_block.clear()
        # self.custom_command_input_box.clear()


    def clear_resource_elements(self):
        """Function that clears the Resource widgets for the EC2 Console screen.
        """

        LOGGER.write('EC2ConsoleManager - clear_resource_elements - Clearing EC2 Resource List Menu, Info Text Block and Custom Command Input Box')
        self.ec2_resource_list_menu.clear()
        self.ec2_resource_info_text_block.clear()
        # self.custom_command_input_box.clear()


    # def clear_secondary_resource_elements(self):
    #     """Function that clears the Secondary Resource widgets for the EC2 Console screen.
    #     """

    #     LOGGER.write('EC2ConsoleManager - clear_secondary_resource_elements - Clearing EC2 Secondary Resource Menu')
    #     self.ec2_resource_secondary_menu.clear()


    def set_initial_values(self):
        """Function that sets the initial values for the EC2 Console screen.
        """

        LOGGER.write('EC2ConsoleManager - set_initial_values')
        self.manager.current_screen = 'ec2'
        LOGGER.write('EC2ConsoleManager - set_initial_values - Set current_screen: {}'.format(self.manager.current_screen))
        LOGGER.write('EC2ConsoleManager - set_initial_values - Setting EC2 Session')
        self.session = self.manager.session
        self.ec2_commands = EC2.EC2Commands(self.session)
        LOGGER.write('EC2ConsoleManager - set_initial_values - Clearing screen widgets and setting resource menu.')
        self.current_resource_id = None
        # self.current_secondary_resource_id = None
        self.clear_elements()
        self.ec2_resource_list_menu.set_title(self.manager.default_region)
        self.ec2_resource_menu.add_item_list(self.available_ec2_resources())


    def set_initial_focus(self):
        """Override of base function. Sets initial focus to the resource select box.
        """

        LOGGER.write('EC2ConsoleManager - set_initial_focus - Setting initial focus')
        self.manager.root.move_focus(self.ec2_resource_menu)    


    def refresh_status(self):
        """Function that refreshes the status of the EC2 Console screen.
        """
        LOGGER.write('EC2ConsoleManager - refresh_status - Reloading the screen.')
        # this should call self.manager.open_resource_console_window. However, open_resource_console_window needs to be rewritten to use current_screen for selection choice; this requires a greater rewrite. noted in to-do.
        # self.manager.open_resource_console_window()
        # Edit at later date after removing: Thinking about it, this function may not really be needed on this screen. Once the screen is loaded, we don't really have anything to be refreshed. 
        # The only thing that would need to be refreshed is the resource list, and that would be done by the user selecting a new resource or filtering. 
        # Refreshing the whole page may be the way to go here, but seemingly accomplishs nothing we haven't already achieved in a more specific manner.
        # I'm going to leave this function here for now, but I may remove it later.


    def available_ec2_resources(self):
        """Function that returns a list of available EC2 resources.

        Returns
        -------
        available_resources : list of str
            The list of available EC2 resources
        """
        
        LOGGER.write('EC2ConsoleManager - available_ec2_resources')
        available_resources = ['Instances', 
                                    'Images', 
                                    'Volumes', 
                                    'Snapshots', 
                                    'Security Groups', 
                                    'Key Pairs', 
                                    'Elastic IPs', 
                                    'Load Balancers', 
                                    'Target Groups', 
                                    'Launch Templates',
                                    'Auto Scaling Groups']
        
        return available_resources


    def fetch_ec2_resource_list(self):
        """Function to parse and fetch the EC2 resource list
           associated with the selected resource.
        """

        LOGGER.write('EC2ConsoleManager - fetch_ec2_resource_list')
        selected_resource = self.ec2_resource_menu.get()
        LOGGER.write('EC2ConsoleManager - fetch_ec2_resource_list - Selected Resource: {}'.format(selected_resource))
        # self.clear_resource_elements()
        if selected_resource == 'Instances':
            self.display_resource_menu('Instances', self.ec2_commands.get_instances, self.ec2_commands.get_instance_details, self.ec2_tables.build_instance_details_table)
        elif selected_resource == 'Images':
            self.display_resource_menu('Images', self.ec2_commands.get_images, self.ec2_commands.get_image_details, self.ec2_tables.build_image_details_table)
        elif selected_resource == 'Volumes':
            self.display_resource_menu('Volumes', self.ec2_commands.get_volumes, self.ec2_commands.get_volume_details, self.ec2_tables.build_volume_details_table)
        elif selected_resource == 'Snapshots':
            self.display_resource_menu('Snapshots', self.ec2_commands.get_snapshots, self.ec2_commands.get_snapshot_details, self.ec2_tables.build_snapshot_details_table)
        elif selected_resource == 'Security Groups':
            self.display_resource_menu('Security Groups', self.ec2_commands.get_security_groups, self.ec2_commands.get_security_group_details, self.ec2_tables.build_security_group_details_table)
        elif selected_resource == 'Key Pairs':
            self.display_resource_menu('Key Pairs', self.ec2_commands.get_key_pairs, self.ec2_commands.get_key_pair_details, self.ec2_tables.build_key_pair_details_table)
        elif selected_resource == 'Elastic IPs':
            self.display_resource_menu('Elastic IPs', self.ec2_commands.get_elastic_ips, self.ec2_commands.get_elastic_ip_details, self.ec2_tables.build_elastic_ip_details_table)
        elif selected_resource == 'Load Balancers':
            self.display_resource_menu('Load Balancers', self.ec2_commands.get_load_balancers, self.ec2_commands.get_load_balancer_details, self.ec2_tables.build_load_balancer_details_table)
        elif selected_resource == 'Target Groups':
            self.display_resource_menu('Target Groups', self.ec2_commands.get_target_groups, self.ec2_commands.get_target_group_details, self.ec2_tables.build_target_group_details_table)
        elif selected_resource == 'Launch Templates':
            self.display_resource_menu('Launch Templates', self.ec2_commands.get_launch_templates, self.ec2_commands.get_launch_template_details, self.ec2_tables.build_launch_template_details_table)
        elif selected_resource == 'Auto Scaling Groups':
            self.display_resource_menu('Auto Scaling Groups', self.ec2_commands.get_auto_scaling_groups, self.ec2_commands.get_auto_scaling_group_details, self.ec2_tables.build_auto_scaling_group_details_table)
        else:
            self.manager.open_not_supported_popup(selected_resource)


    def process_resource_menu(self, resources, resource_type, get_resource_details=None, get_instance_name=None):
        """Function to parse the resource menu for resources.

        Parameters
        ----------
        resources : list of dict
            The list of resources to parse
        resource_type : str
            The type of the resources
        get_resource_details : function, optional
            The function to call to fetch the details of the selected resource
        get_instance_name : function, optional
            The function to call to get the name of the instance

        Returns
        -------
        resource_ids : list of str
            The IDs of the resources in the current session
        resource_list : list of str
            The list of resources to display in the menu
        """
        if resource_type == 'Instances':
            resource_ids = [resource.id for resource in resources]
            resource_list = []
            for id in resource_ids:
                id_details = get_resource_details(id)
                id_name = get_instance_name(id_details)
                resource_list.append('{} - {}'.format(id, id_name))
        elif resource_type == 'Security Groups':
            resource_ids = [resource.id for resource in resources]
            resource_list = []
            for resource in resources:
                resource_list.append('{} - {}'.format(resource.id, resource.group_name))
        elif resource_type == 'Key Pairs':
            resource_ids = [resource['KeyName'] for resource in resources]
            resource_list = resource_ids
        elif resource_type == 'Elastic IPs':
            resource_ids = [resource['PublicIp'] for resource in resources]
            resource_list = resource_ids
        elif resource_type == 'Load Balancers':
            resource_ids = [resource['LoadBalancerName'] for resource in resources]
            resource_list = resource_ids
        elif resource_type == 'Target Groups':
            resource_ids = [resource['TargetGroupName'] for resource in resources]
            resource_list = resource_ids
        elif resource_type == 'Launch Templates':
            resource_ids = [resource['LaunchTemplateName'] for resource in resources]
            resource_list = resource_ids
        elif resource_type == 'Auto Scaling Groups':
            resource_ids = [resource['AutoScalingGroupName'] for resource in resources]
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

        LOGGER.write('EC2ConsoleManager - display_{}_menu'.format(resource_type))
        self.clear_resource_elements()
        resources = get_resources()
        if resources == []:
            LOGGER.write('EC2ConsoleManager - display_{}_menu - No {} found.'.format(resource_type, resource_type))
            self.ec2_resource_info_text_block.set_text('No {} found.'.format(resource_type))
            return
        if isinstance(resources, str) and resources.startswith('Error'):
            LOGGER.write('EC2ConsoleManager - display_{}_menu - Error fetching {}.'.format(resource_type, resource_type))
            self.ec2_resource_info_text_block.set_text(resources)
            return
        LOGGER.write('EC2ConsoleManager - display_{}_menu - Fetching {} - {}: {}'.format(resource_type, resource_type, resource_type, resources))
        resource_ids, resource_list = self.process_resource_menu(resources, resource_type, get_resource_details, get_instance_name)
        LOGGER.write('EC2ConsoleManager - display_{}_menu - Parsing {} IDs - {}: {}'.format(resource_type, resource_type, resource_type, resource_ids))
        if resource_ids:
            LOGGER.write('EC2ConsoleManager - display_{}_menu - Adding {} IDs to EC2 Resource List Menu'.format(resource_type, resource_type))
            self.ec2_resource_list_menu.add_item_list(resource_list)
            self.ec2_resource_list_menu.add_key_command(py_cui.keys.KEY_ENTER, lambda: self.set_current_resource_id(resource_type, get_resource_details, build_resource_details_table))
            self.display_resource_details(resource_type, get_resource_details, build_resource_details_table)
        elif resource_ids == []:
            LOGGER.write('EC2ConsoleManager - display_{}_menu - No {} found.'.format(resource_type, resource_type))
            self.ec2_resource_info_text_block.set_text('No {} found.'.format(resource_type))
        else:
            LOGGER.write('EC2ConsoleManager - display_{}_menu - Error fetching {}.'.format(resource_type, resource_type))
            self.ec2_resource_info_text_block.set_text('Error fetching {}.'.format(resource_type))


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

        LOGGER.write('EC2ConsoleManager - set_current_{}_id'.format(resource_type))
        selected_resource = self.ec2_resource_list_menu.get()
        if resource_type == 'Instances':
            selected_resource_id, selected_resource_name = selected_resource.split(' - ', 1)
        elif resource_type == 'Security Groups':
            selected_resource_id, selected_resource_name = selected_resource.split(' - ', 1)
        else:
            selected_resource_id = selected_resource
        LOGGER.write('EC2ConsoleManager - set_current_{}_id - Selected {}: {}'.format(resource_type, resource_type, selected_resource_id))
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

        LOGGER.write('EC2ConsoleManager - display_{}_details'.format(resource_type))
        selected_resource_id = self.current_resource_id
        LOGGER.write('EC2ConsoleManager - display_{}_details - Selected {}: {}'.format(resource_type, resource_type, selected_resource_id))
        resource = get_resource_details(selected_resource_id)
        self.ec2_resource_info_text_block.clear()
        if resource == []:
            LOGGER.write('EC2ConsoleManager - display_{}_details - No details found for {}: {}'.format(resource_type, resource_type, selected_resource_id))
            self.ec2_resource_info_text_block.set_text('{} details not found for {}'.format(resource_type, selected_resource_id))
        elif isinstance(resource, str) and resource.startswith('Error'):
            LOGGER.write('EC2ConsoleManager - display_{}_menu - Error fetching {}.'.format(resource_type, resource_type))
            self.ec2_resource_info_text_block.set_text(resource)
        elif resource:
            LOGGER.write('EC2ConsoleManager - display_{}_details - Adding {} Details to EC2 Resource Info Text Block'.format(resource_type, resource_type))
            resource_details = build_resource_details_table(resource)
            LOGGER.write('EC2ConsoleManager - display_{}_details - {} Details: {}'.format(resource_type, resource_type, resource_details))
            self.ec2_resource_info_text_block.set_text(resource_details)
            # self.process_secondary_resource_menu(resource_type, resource)
        else:
            LOGGER.write('EC2ConsoleManager - display_{}_details - Error fetching {} details: {}'.format(resource_type, resource_type, selected_resource_id))
            self.ec2_resource_info_text_block.set_text('Error fetching {} details. {}'.format(resource_type, selected_resource_id))



    # def process_secondary_resource_menu(self, resource_type, resource):
    #     """Function to fetch the secondary resources for the primary resource in the current session.
    #     """

    #     LOGGER.write('EC2ConsoleManager - display_secondary_{}_menu'.format(resource_type))
    #     self.clear_secondary_resource_elements()


    def get_logo_text(self):
        """Generates ascii-art version of pyaws logo

        Returns
        -------
        logo : str
            ascii-art logo
        """

        LOGGER.write('EC2ConsoleManager - get_logo_text - Generating logo text')
        logo = ' ___  ____/_  ____/_|__ \\ \n'
        logo += '__  __/  _  /    ____/ / \n'
        logo += '_  /___  / /___  _  __/  \n'
        logo += '/_____/ \\____/ /____/  \n'
        return logo


    def show_help_text(self):
        """Function that shows the help text for the EC2 Console screen.
        """

        LOGGER.write('EC2ConsoleManager - show_help_text')
        help_text = self.get_help_text()
        self.ec2_resource_info_text_block.clear()
        self.ec2_resource_info_text_block.set_text(help_text)


    def get_help_text(self):
        """Generates help text for EC2 Console screen

        Returns
        -------
        help_text : str
            The help text for the EC2 Console screen
        """

        LOGGER.write('EC2ConsoleManager - get_help_text')
        help_text = 'EC2 Console Help\n\n'
        help_text += 'Use the arrow keys to navigate the resource selection menu.\n\n'
        help_text += 'Shortcuts:\n'
        help_text += 'ENTER - Select Menu Option.\n'
        help_text += 'BACKSPACE - Return to Account Console.\n'
        help_text += 'h - Show Help Text\n'
        help_text += 'm - Open Menu\n'
        help_text += 'q - Exit\n'
        help_text += '\n'
        help_text += 'Inside Resource Selection:\n'
        help_text += 'ENTER - Select Instance.\n'
        # help_text += 'r - Show Running Instances.\n'
        # help_text += 's - Show Stopped Instances.\n'
        # help_text += 'a - Show All Instances.\n'
        # help_text += 'R - Reboot Instance.\n'
        # help_text += 'T - Terminate Instance.\n'

        return help_text