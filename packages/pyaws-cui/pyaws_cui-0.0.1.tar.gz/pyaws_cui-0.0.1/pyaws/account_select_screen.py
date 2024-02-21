"""Manager implementation for CUI screen for selecting different profiles.
"""

import datetime

import py_cui
import pyaws
import pyaws.screen_manager
import pyaws.logger as LOGGER


class AccountSelectManager(pyaws.screen_manager.ScreenManager):
    """Class representing the manager for the account select screen

    Attributes
    ----------
    menu_choices : list of str
        Overriden attribute from base class with expanded menu choices.
    """

    def __init__(self, top_manager):
        """Constructor for repo select manager
        """
        
        super().__init__(top_manager, 'Account Selection')
        self.menu_choices = ['Open Directory',
                                'Settings',
                                'Exit']

    def process_menu_selection(self, selection):
        """Override of base class, executes depending on menu selection


        Parameters
        ----------
        selection : str
            The user's menu selection
        """

        LOGGER.write('AccountSelectManager - process_menu_selection - Processing menu selection: {}'.format(selection))
        if selection == 'Open Directory':
            # This will be implemented once py_cui adds a filemanager popup.
            self.manager.open_not_supported_popup(selection)
            pass
        elif selection == 'Settings':
            self.manager.open_settings_window()
        elif selection == 'Exit':
            self.manager.close_cleanup()
            exit()
        else:
            self.manager.open_not_supported_popup(selection)

    def initialize_screen_elements(self):
        """Override of base function. Initializes widgets, returns screen widget set

        Returns
        -------
        account_select_widget_set : py_cui.widget_set.WidgetSet
            Widget set object for repo select screen
        """

        LOGGER.write('AccountSelectManager - initialize_screen_elements - Initializing widgets')
        account_select_widget_set = self.manager.root.create_new_widget_set(5,4)

        logo_label = account_select_widget_set.add_block_label(self.manager.get_logo_text(), 0, 0, row_span=1, column_span=1, center=True)
        logo_label.set_color(py_cui.CYAN_ON_BLACK)

        # This should be replaced with a get_copyright_text function?
        # link_label = account_select_widget_set.add_label('v{} - https://github.com/j-lavender/pyaws_cui'.format(pyaws.__version__), 4, 0, row_span=1, column_span=2)
        # link_label.add_text_color_rule('https://.*', py_cui.CYAN_ON_BLACK, 'contains', match_type='regex')

        # self.about_box = account_select_widget_set.add_text_block('About', 1, 0, row_span=3, column_span=2)
        # self.about_box.set_selectable(False)
        # self.about_box.add_text_color_rule('Welcome', py_cui.RED_ON_BLACK, 'startswith', match_type='line')

        self.current_status_box = account_select_widget_set.add_text_block('Current Status', 0, 1, row_span=1, column_span=2)
        self.current_status_box.add_text_color_rule('.*', py_cui.MAGENTA_ON_BLACK, rule_type='contains', match_type='line')
        self.current_status_box.set_selectable(False)

        self.account_menu = account_select_widget_set.add_scroll_menu('Profiles', 1, 1, row_span=3, column_span=2)
        self.account_menu.add_item_list(self.manager.profiles)
        self.account_menu.add_text_color_rule('.*', py_cui.RED_ON_BLACK, rule_type='contains', match_type='line')
        self.account_menu.add_key_command(py_cui.keys.KEY_ENTER,    self.update_default_profile)
        self.account_menu.add_key_command(py_cui.keys.KEY_D_UPPER,  self.ask_delete_account)
        self.account_menu.add_key_command(py_cui.keys.KEY_R_LOWER,  self.refresh_status)
        self.account_menu.add_key_command(py_cui.keys.KEY_M_LOWER,  self.show_menu)
        self.account_menu.add_key_command(py_cui.keys.KEY_Q_LOWER,  self.manager.clean_exit)
        self.account_menu.add_key_command(py_cui.keys.KEY_S_LOWER,  self.manager.open_settings_window)
        self.account_menu.add_key_command(py_cui.keys.KEY_A_LOWER,  self.manager.open_about_window)
        self.account_menu.add_key_command(py_cui.keys.KEY_L_LOWER,  self.manager.open_account_console_window)
        self.account_menu.set_focus_text('Quit - q | Set Profile - Enter | Refresh - r | Delete Account - Del | Settings - s | Menu - m | About - a')

        # self.region_menu = account_select_widget_set.add_scroll_menu('Regions', 1, 2, row_span=3, column_span=1)
        # self.region_menu.add_item_list(self.manager.regions)
        # self.region_menu.add_text_color_rule('.*', py_cui.RED_ON_BLACK, rule_type='contains', match_type='line')
        # self.region_menu.add_key_command(py_cui.keys.KEY_ENTER,    self.manager.update_default_region)
        # self.region_menu.add_key_command(py_cui.keys.KEY_R_LOWER,  self.refresh_status)
        # self.region_menu.add_key_command(py_cui.keys.KEY_M_LOWER,  self.show_menu)
        # self.region_menu.add_key_command(py_cui.keys.KEY_Q_LOWER,  self.manager.clean_exit)
        # self.region_menu.add_key_command(py_cui.keys.KEY_S_LOWER,  self.manager.open_settings_window)
        # self.region_menu.add_key_command(py_cui.keys.KEY_A_LOWER,  self.manager.open_about_window)
        # self.region_menu.add_key_command(py_cui.keys.KEY_L_LOWER,  self.manager.open_account_console_window)
        # self.region_menu.set_focus_text('Quit - q | Set Region - Enter | Menu - m | Refresh - r | Settings - s')

        self.login_button = account_select_widget_set.add_button('Login', 4, 1, row_span=1, column_span=2, command=self.manager.open_account_console_window)

        account_select_widget_set.add_key_command(py_cui.keys.KEY_S_LOWER, self.manager.open_settings_window)
        account_select_widget_set.add_key_command(py_cui.keys.KEY_R_LOWER, self.refresh_status)
        account_select_widget_set.add_key_command(py_cui.keys.KEY_M_LOWER, self.show_menu)
        account_select_widget_set.add_key_command(py_cui.keys.KEY_A_LOWER, self.manager.open_about_window)
        account_select_widget_set.add_key_command(py_cui.keys.KEY_L_LOWER, self.manager.open_account_console_window)
        # account_select_widget_set.add_key_command(py_cui.keys.KEY_H_LOWER, lambda : self.about_box.set_text(self.manager.get_welcome_message()))

        # self.info_panel = self.about_box

        # self.refresh_status()
        return account_select_widget_set
    
    def clear_elements(self):
        """Override of base class, clears text widgets
        """

        LOGGER.write('AccountSelectManager - clear_elements - Clearing widgets')
        self.current_status_box.clear()
        self.account_menu.clear()


    def set_initial_values(self):
        """Override of base class, sets initial values for widgets
        """

        LOGGER.write('AccountSelectManager - set_initial_values - Setting initial values')
        self.manager.current_screen = 'select'
        LOGGER.write('AccountSelectManager - set_initial_values - Set current_screen: {}'.format(self.manager.current_screen))
        self.manager.root.set_status_bar_text('Quit - q | Refresh - r | Quick Login - l | Settings - s | About - a | Menu - m | Help - h')
        self.refresh_status()
        # if self.manager.metadata_manager.first_time:
        #     self.about_box.set_text(self.manager.get_welcome_message())
        #     self.manager.metadata_manager.first_time = False
        # else:
        #     self.about_box.set_text(self.manager.get_about_info(with_logo = False))


    def set_initial_focus(self):
        """Override of base function. Sets initial focus to the resource select box.
        """

        LOGGER.write('AccountSelectManager - set_initial_focus - Setting initial focus')
        self.manager.root.move_focus(self.account_menu)


    def refresh_status(self):
        """Function that refreshes the list of profiles and the current status
        """

        LOGGER.write('AccountSelectManager - refresh_status - Refreshing account list and status')
        self.manager.profiles = pyaws.get_aws_profiles(self)
        self.manager.profile_path = pyaws.get_aws_credentials_path(self)
        self.clear_elements()
        self.account_menu.add_item_list(self.manager.profiles)

        status_message = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n'
        status_message = status_message + 'Current directory:\n {}\n'.format(self.manager.workspace_path)
        status_message = status_message + 'Profile path:\n {}\n'.format(self.manager.profile_path)
        if len(self.manager.profiles) == 0:
            status_message = status_message + 'No profiles found\n'
        else:
            status_message = status_message + '# of Profiles: {}\n'.format(len(self.manager.profiles))
        self.current_status_box.set_text(status_message)


    def update_default_profile(self):
        """Function that updates the default profile
        """

        LOGGER.write('AccountSelectManager - update_default_profile - Updating default profile')
        selected_account = self.account_menu.get()
        if selected_account == None:
            self.manager.root.show_error_popup('Update Profile Error', 'No account selected.')
            return
        LOGGER.write('AccountSelectManager - update_default_profile - Updating default profile to {}'.format(selected_account))
        self.manager.update_default_profile(profile=selected_account)
        self.refresh_status()
        self.manager.root.show_message_popup('Profile Updated', 'Default profile updated to {}'.format(selected_account))


    def ask_delete_account(self):
        """Function that asks user if they want to delete an account
        """

        LOGGER.write('AccountSelectManager - ask_delete_account - Asking user if they want to delete an account')
        if len(self.manager.profiles) == 0:
            self.manager.root.show_error_popup('Delete Account Error', 'No accounts to delete')
            return
        selected_account = self.account_menu.get()
        if selected_account == None:
            self.manager.root.show_error_popup('Delete Account Error', 'No account selected.')
            return
        self.manager.root.show_yes_no_popup('Delete Account {}?'.format(selected_account), self.delete_account)

    
    def delete_account(self, to_delete):
        """Function that deletes an account

        Parameters
        ----------
        to_delete : bool
            True if user selected yes, False if user selected no
        """

        LOGGER.write('AccountSelectManager - delete_account')
        if to_delete == True:
            selected_account = self.account_menu.get()
            LOGGER.write('AccountSelectManager - delete_account  - Deleting account {}'.format(selected_account))
            self.delete_aws_profile(selected_account)
            self.refresh_status()
            self.manager.root.show_message_popup('Account Deleted', 'Account {} deleted'.format(selected_account))
        elif to_delete == False:
            LOGGER.write('AccountSelectManager - delete_account - User selected cancel')
            self.manager.root.show_message_popup('Delete Account Cancelled', 'Account delete action was cancelled.')
        else:
            LOGGER.write('AccountSelectManager - delete_account - Unable to delete account, or user selected no')
            self.manager.root.show_error_popup('Delete Account Error', 'Account delete action unable to be completed.')


    def delete_aws_profile(self, profile):
        """Deletes an AWS profile from the AWS credentials file

        Parameters
        ----------
        profile : str
            Name of the profile to delete
        """

        LOGGER.write('PyAWS - Deleting profile: {}'.format(profile))

        with open(self.manager.profile_path, 'r') as cred_file:
            lines = cred_file.readlines()

        with open(self.manager.profile_path, 'w') as cred_file:
            delete_mode = False
            for line in lines:
                if line.strip().startswith('[' + profile + ']'):
                    delete_mode = True
                elif line.startswith('[') and delete_mode:
                    delete_mode = False
                    cred_file.write(line)
                elif not delete_mode:
                    cred_file.write(line)
        LOGGER.write('PyAWS - Deleted profile: {}'.format(profile))
