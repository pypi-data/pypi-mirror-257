"""File containing functions used for creating display tables for IAM resources.

This file is meant to contain the set of functions used to create display tables
for IAM resources.
"""

import json
from tabulate import tabulate
import pyaws.logger as LOGGER
from pyaws.utils import DateTimeEncoder


class IAMConsoleTables:
    """Class responsible for creating display tables for IAM resources.

    This class is responsible for creating display tables for IAM resources.

    Attributes
    ----------
    LOGGER : pyaws.logger.Logger
        The pyaws logger object.
    """

    def build_roles_details_table(self, role_details):
        """Function to build a display table for IAM roles.

        Parameters
        ----------
        role_details : list
            A list of IAM role objects.

        Returns
        -------
        str
            A string containing the display table for IAM roles.
        """
        LOGGER.write('IAMConsoleTables - build_roles_details_table - Building IAM Roles Details Table')
        table = [['Attribute', 'Value'],
                    ['Name', role_details.get('Role', {}).get('RoleName')],
                    ['ARN', role_details.get('Role', {}).get('Arn')],
                    ['Created', role_details.get('Role', {}).get('CreateDate')],
                    ['Last Used', role_details.get('Role', {}).get('RoleLastUsed')],
                    ['ID', role_details.get('Role', {}).get('RoleId')],
                    ['Path', role_details.get('Role', {}).get('Path')],
                    ['Assume Role Policy', role_details.get('Role', {}).get('AssumeRolePolicyDocument')]]
        table = tabulate(table, headers='firstrow', tablefmt='fancy_grid')
        # table = json.dumps(role_details, indent=4, cls=DateTimeEncoder)
        # attached_policies = self.build_role_policies_table(role_name=role_details.get('Role', {}).get('RoleName'))
        # table += '\n\n'
        # table += 'Attached Policies:\n'
        # table += attached_policies
        return table

    # This is part of above commented out code. This doesn't work. It requires calling back to the iam_commands to get the attached role policies.
    # This isn't really possible at this location with the current design. This feature is going to wait until secondary and tertiary widgets are implemented.
    # At that time we'll be able to make the necessary calls to the iam_commands to get the attached role policies.
    # def build_role_policies_table(self, role_name):
    #     """Function to build a display table for IAM role policies.

    #     Parameters
    #     ----------
    #     role_policies : list
    #         A list of IAM role policy objects.

    #     Returns
    #     -------
    #     str
    #         A string containing the display table for IAM role policies.
    #     """
    #     role_policies = get_attached_role_policies(RoleName=role_name)['AttachedPolicies']
    #     LOGGER.write('IAMConsoleTables - build_role_policies_table - Building IAM Role Policies Table')
    #     table = [['Policy Name', 'Policy ARN']]
    #     for policy in role_policies:
    #         policy_name = policy.get('PolicyName', 'N/A')
    #         policy_arn = policy.get('PolicyArn', 'N/A')
    #         table.append([policy_name, policy_arn])
    #     table = tabulate(table, headers='firstrow', tablefmt='fancy_grid')
    #     return table


    def build_users_details_table(self, user_details):
        """Function to build a display table for IAM users.

        Parameters
        ----------
        user_details : list
            A list of IAM user objects.

        Returns
        -------
        str
            A string containing the display table for IAM users.
        """
        LOGGER.write('IAMConsoleTables - build_users_details_table - Building IAM Users Details Table')
        table = [['Attribute', 'Value'],
                    ['Name', user_details.get('User', {}).get('UserName')],
                    ['ARN', user_details.get('User', {}).get('Arn')],
                    ['Created', user_details.get('User', {}).get('CreateDate')],
                    ['ID', user_details.get('User', {}).get('UserId')],
                    ['Path', user_details.get('User', {}).get('Path')],
                    ['Tags', user_details.get('User', {}).get('Tags')]]
        # table = json.dumps(user_details, indent=4, cls=DateTimeEncoder)
        table = tabulate(table, headers='firstrow', tablefmt='fancy_grid')
        return table
    

    def build_groups_details_table(self, group_details):
        """Function to build a display table for IAM groups.

        Parameters
        ----------
        group_details : list
            A list of IAM group objects.

        Returns
        -------
        str
            A string containing the display table for IAM groups.
        """
        LOGGER.write('IAMConsoleTables - build_groups_details_table - Building IAM Groups Details Table')
        table = [['Attribute', 'Value'],
                    ['Name', group_details.get('Group', {}).get('GroupName')],
                    ['ARN', group_details.get('Group', {}).get('Arn')],
                    ['Created', group_details.get('Group', {}).get('CreateDate')],
                    ['ID', group_details.get('Group', {}).get('GroupId')],
                    ['Path', group_details.get('Group', {}).get('Path')]]
                    # ['Users', group_details.get('Users')]]
        # table = json.dumps(group_details, indent=4, cls=DateTimeEncoder)
        table = tabulate(table, headers='firstrow', tablefmt='fancy_grid')
        # Special handling for attached users. This will change when screen functionality is expanded.
        attached_users = group_details.get('Users', [])
        if attached_users:
            attached_users_table = self.build_attached_users_details_table(attached_user_details=attached_users)
        table += '\n\n' 
        table += 'Attached Users:\n'
        table += attached_users_table
        return table
    
    def build_attached_users_details_table(self, attached_user_details):
        """Function to build a display table for IAM Users attached to a group.
        
        Parameters
        ----------
        group_details : list
            A list of IAM group objects.
        
        Returns
        -------
        str
            A string containing the display table for IAM users attached to a group.
        """
        LOGGER.write('IAMConsoleTables - build_attached_users_details_table - Building IAM Users Attached to Group Details Table')
        attached_users_table = [['Name', 'ARN']]
        for user in attached_user_details:
            name = user.get('UserName', 'N/A')
            arn = user.get('Arn', 'N/A')
            attached_users_table.append([name, arn])      
        table = tabulate(attached_users_table, headers='firstrow', tablefmt='fancy_grid')
        return table


    def build_policies_details_table(self, policy_details):
        """Function to build a display table for IAM policies.

        Parameters
        ----------
        policy_details : list
            A list of IAM policy objects.

        Returns
        -------
        str
            A string containing the display table for IAM policies.
        """
        LOGGER.write('IAMConsoleTables - build_policy_details_table - Building IAM Policies Details Table')
        table = [['Attribute', 'Value'],
                    ['Name', policy_details.get('PolicyName')],
                    ['ARN', policy_details.get('Arn')],
                    ['Created', policy_details.get('CreateDate')],
                    ['Path', policy_details.get('Path')]]
        # table = json.dumps(policy_details, indent=4, cls=DateTimeEncoder)
        table = tabulate(table, headers='firstrow', tablefmt='fancy_grid')
        return table