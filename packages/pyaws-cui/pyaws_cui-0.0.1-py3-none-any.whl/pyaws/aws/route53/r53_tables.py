"""File containing functions used for creating display tables for Systems Manager resources.

This file is meant to contain the set of functions used to create display tables
for Systems Manager resources.
"""

import json
from tabulate import tabulate
import pyaws.logger as LOGGER
from pyaws.utils import DateTimeEncoder

class R53ConsoleTables:
    """Class responsible for creating display tables for Systems Manager resources.

    This class is responsible for creating display tables for Systems Manager resources.

    Attributes
    ----------
    LOGGER : pyaws.logger.Logger
        The pyaws logger object.
    """

    def build_hosted_zone_details_table(self, resource_record_sets):
        """Create a display table for hosted zone details.

        This function creates a display table for hosted zone details.

        Parameters
        ----------
        resource_record_sets : dict
            The resource record sets in the hosted zone.

        Returns
        -------
        str
            The display table.
        """
        LOGGER.write('R53ConsoleTables - display_hosted_zone_details_table - Creating display table for hosted zone details')
        resource_record_sets = resource_record_sets['ResourceRecordSets'] # This really shouldn't be done here, but it's a quick fix for now.
        table = []
        for record_set in resource_record_sets:
            table.append([record_set['Name'], record_set['Type'], record_set['TTL'], json.dumps(record_set['ResourceRecords'], cls=DateTimeEncoder)])
        table = tabulate(table, headers=['Name', 'Type', 'TTL', 'Resource Records'], tablefmt='grid')
        return table
