"""File containing functions used to call the underlying AWS IAM commands.

This file is meant to handle the intermediate considerations between the
CUI and the AWS IAM CLI. It is meant to be called by the CUI, and to call the
AWS CLI commands. It is not meant to be called directly by the user.
"""

# pyaws imports
import pyaws.logger as LOGGER
import pyaws.utils as UTILS

@UTILS.HandleAwsError.decorate_all_methods(UTILS.HandleAwsError.handle_aws_error)
class IAMCommands:
    """Class used to manage AWS IAM commands.

    This class provides the interface between the AWS IAM commands. 
    It is responsible for calling the AWS IAM commands, and providing
    the results to other pyaws modules.

    Attributes
    ----------
    session : boto3.session.Session
        The AWS session object.
    """

    def __init__(self, session):
        """Constructor for IAMCommands class.

        Parameters
        ----------
        session : boto3.session.Session
            The AWS session object.
        """
        LOGGER.write('EC2Commands - init - Initializing IAM Commands')
        self.session = session
        self.iam_client = self.session.client('iam')
        self.iam_resource = self.session.resource('iam')
        LOGGER.write('EC2Commands - init - IAM Commands Initialized')


    def get_users(self):
        """Function to return a list of IAM users.

        Returns
        -------
        list
            A list of IAM user objects.
        """
        LOGGER.write('IAMCommands - get_users - Getting IAM Users')
        users = self.iam_client.list_users()
        LOGGER.write('IAMCommands - get_users - IAM Users: {}'.format(users))
        LOGGER.write('IAMCommands - get_users - Got IAM Users')
        return users


    def get_user_details(self, user_name):
        """Function to return the details of a specific IAM user.

        Parameters
        ----------
        user_name : str
            The name of the IAM user.

        Returns
        -------
        dict
            A dictionary containing the details of the IAM user.
        """
        LOGGER.write('IAMCommands - get_user_details - Getting IAM User Details')
        user = self.iam_client.get_user(UserName=user_name)
        if user == None:
            LOGGER.write('IAMCommands - get_user_details - IAM User: {}'.format(user))
        LOGGER.write('IAMCommands - get_user_details - IAM User: {}'.format(user))
        LOGGER.write('IAMCommands - get_user_details - Got IAM User Details')
        return user


    def get_groups(self):
        """Function to return a list of IAM groups.

        Returns
        -------
        list
            A list of IAM group objects.
        """
        LOGGER.write('IAMCommands - get_groups - Getting IAM Groups')
        groups = self.iam_client.list_groups()
        LOGGER.write('IAMCommands - get_groups - IAM Groups: {}'.format(groups))
        LOGGER.write('IAMCommands - get_groups - Got IAM Groups')
        return groups


    def get_group_details(self, group_name):
        """Function to return the details of a specific IAM group.

        Parameters
        ----------
        group_name : str
            The name of the IAM group.

        Returns
        -------
        dict
            A dictionary containing the details of the IAM group.
        """
        LOGGER.write('IAMCommands - get_group_details - Getting IAM Group Details')
        group = self.iam_client.get_group(GroupName=group_name)
        if group == None:
            LOGGER.write('IAMCommands - get_group_details - IAM Group: {}'.format(group))
        LOGGER.write('IAMCommands - get_group_details - IAM Group: {}'.format(group))
        LOGGER.write('IAMCommands - get_group_details - Got IAM Group Details')
        return group


    def get_policies(self):
        """Function to return a list of user-created IAM policies.

        Returns
        -------
        list
            A list of user-created IAM policy objects.
        """
        LOGGER.write('IAMCommands - get_policies - Getting user-created IAM Policies')
        policies = self.iam_client.list_policies(Scope='Local')
        LOGGER.write('IAMCommands - get_policies - User-created IAM Policies: {}'.format(policies))
        LOGGER.write('IAMCommands - get_policies - Got user-created IAM Policies')
        return policies


    def get_policy_details(self, policy_name):
        """Function to return the details of a specific IAM policy.

        Parameters
        ----------
        policy_name : str
            The name of the IAM policy.

        Returns
        -------
        dict
            A dictionary containing the details of the IAM policy.
        """
        LOGGER.write('IAMCommands - get_policy_details - Getting IAM Policy Details')
        policy = self.iam_client.get_policy(PolicyArn=policy_name)
        policy = policy['Policy']
        if policy == None:
            LOGGER.write('IAMCommands - get_policy_details - IAM Policy: {}'.format(policy))
        LOGGER.write('IAMCommands - get_policy_details - IAM Policy: {}'.format(policy))
        LOGGER.write('IAMCommands - get_policy_details - Got IAM Policy Details')
        return policy


    def get_roles(self):
        """Function to return a list of IAM roles.

        Returns
        -------
        list
            A list of IAM role objects.
        """
        LOGGER.write('IAMCommands - get_roles - Getting IAM Roles')
        roles = self.iam_client.list_roles()
        LOGGER.write('IAMCommands - get_roles - IAM Roles: {}'.format(roles))
        LOGGER.write('IAMCommands - get_roles - Got IAM Roles')
        return roles


    def get_role_details(self, role_name):
        """Function to return the details of a specific IAM role.

        Parameters
        ----------
        role_name : str
            The name of the IAM role.

        Returns
        -------
        dict
            A dictionary containing the details of the IAM role.
        """
        LOGGER.write('IAMCommands - get_role_details - Getting IAM Role Details')
        role = self.iam_client.get_role(RoleName=role_name)
        if role == None:
            LOGGER.write('IAMCommands - get_role_details - IAM Role: {}'.format(role))
        LOGGER.write('IAMCommands - get_role_details - IAM Role: {}'.format(role))
        LOGGER.write('IAMCommands - get_role_details - Got IAM Role Details')
        return role


    def get_attached_role_policies(self, role_name):
        """Function to return the policies attached to a specific IAM role.

        Parameters
        ----------
        role_name : str
            The name of the IAM role.

        Returns
        -------
        list
            A list of IAM policy objects attached to the role.
        """
        LOGGER.write('IAMCommands - get_role_policies - Getting IAM Role Policies')
        policies = self.iam_client.list_attached_role_policies(RoleName=role_name)
        LOGGER.write('IAMCommands - get_role_policies - IAM Role Policies: {}'.format(policies))
        LOGGER.write('IAMCommands - get_role_policies - Got IAM Role Policies')
        return policies