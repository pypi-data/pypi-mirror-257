"""File containing functions used for creating display tables for Systems Manager resources.

This file is meant to contain the set of functions used to create display tables
for Systems Manager resources.
"""

import json
from tabulate import tabulate
import pyaws.logger as LOGGER
from pyaws.utils import DateTimeEncoder

class SSMConsoleTables:
    """Class responsible for creating display tables for Systems Manager resources.

    This class is responsible for creating display tables for Systems Manager resources.

    Attributes
    ----------
    LOGGER : pyaws.logger.Logger
        The pyaws logger object.
    """

    def build_parameters_details_table(self, parameter_details):
        """Function to build a display table for SSM parameters.

        Parameters
        ----------
        parameter_details : list
            A list of SSM parameter objects.

        Returns
        -------
        str
            A string containing the display table for SSM parameters.
        """
        LOGGER.write('SSMConsoleTables - build_parameters_details_table - Building SSM Parameters Details Table')
        table = [['Name', parameter_details.get('Parameter', {}).get('Name')],
                    ['ARN', parameter_details.get('Parameter', {}).get('ARN')],
                    ['Type', parameter_details.get('Parameter', {}).get('Type')],
                    ['Last Modified', parameter_details.get('Parameter', {}).get('LastModifiedDate')],
                    ['Last Modified User', parameter_details.get('Parameter', {}).get('LastModifiedUser')],
                    ['Description', parameter_details.get('Parameter', {}).get('Description')]]
                    # ['Value', parameter_details.get('Parameter', {}).get('Value')]]
        table = tabulate(table, headers='firstrow', tablefmt='fancy_grid')
        return table