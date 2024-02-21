"""Subscreen used to display information about the program.
"""

import py_cui
import pyaws
import pyaws.screen_manager
import pyaws.logger as LOGGER

class AboutScreenManager(pyaws.screen_manager.ScreenManager):
    """Class containing the about screen.
    """

    def __init__(self, top_manager):
        """Constructor for SettingsScreen
        """

        super().__init__(top_manager, 'settings screen')
        self.current_info_log = ''
        self.show_settings_log = True
    
    def initialize_screen_elements(self):
        """Override of base class function. Initializes widgets, and returns widget set

        Returns
        -------
        settings_widget_set : py_cui.widget_set.WidgetSet
            Widget set object for rsettings screen
        """

        about_widget_set = self.manager.root.create_new_widget_set(5, 4)
        about_widget_set.add_key_command(py_cui.keys.KEY_BACKSPACE, self.manager.open_account_select_window)
        about_widget_set.add_key_command(py_cui.keys.KEY_ESCAPE, self.manager.open_account_select_window)
        about_widget_set.add_key_command(py_cui.keys.KEY_ENTER, self.manager.open_account_select_window)
        about_widget_set.add_key_command(py_cui.keys.KEY_Q_LOWER,  self.manager.clean_exit)

        logo_label = about_widget_set.add_block_label(self.manager.get_logo_text(), 0, 1, row_span=2, column_span=2, center=True)
        logo_label.set_color(py_cui.WHITE_ON_BLACK)

        self.about_box = about_widget_set.add_text_block('About', 1, 1, row_span=3, column_span=2)
        self.about_box.set_selectable(False)

        link_label = about_widget_set.add_label('v{} - https://github.com/j-lavender/pyaws_cui'.format(pyaws.__version__), 4, 1, row_span=1, column_span=2)
        link_label.add_text_color_rule('https://.*', py_cui.CYAN_ON_BLACK, 'contains', match_type='regex')

        # about_widget_set.add_widget('about_title', 0, 0, rowspan=1, columnspan=4, title='About', widget_type=py_cui.widgets.Widget, center_title=True)
        # about_widget_set.add_widget('about_text', 1, 0, rowspan=3, columnspan=4, title='About', widget_type=py_cui.widgets.ScrollTextBox, center_title=True)

        # about_widget_set.get_widget('about_text').set_text(self.current_info_log)

        return about_widget_set

    def set_initial_values(self):
        """Override of base class, sets initial values for widgets
        """

        LOGGER.write('AboutScreenManager - set_initial_values - Setting initial values')
        self.manager.current_screen = 'about'
        LOGGER.write('AboutScreenManager - set_initial_values - Set current_screen: {}'.format(self.manager.current_screen))
        if self.manager.metadata_manager.first_time:
            self.about_box.set_text(self.manager.get_welcome_message())
            self.manager.metadata_manager.first_time = False
        else:
            self.about_box.set_text(self.manager.get_about_info(with_logo = False))