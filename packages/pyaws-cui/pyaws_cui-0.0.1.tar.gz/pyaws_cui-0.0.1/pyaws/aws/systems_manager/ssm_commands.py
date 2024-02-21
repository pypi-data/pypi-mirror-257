"""File containing functions used to call the underlying AWS Systems Manager commands

This file is meant to handle the intermediate considerations between the
CUI and the AWS SSM CLI. It is meant to be called by the CUI, and to call the
AWS CLI commands. It is not meant to be called directly by the user.
"""

# pyaws imports
import pyaws.logger as LOGGER
import pyaws.utils as UTILS

@UTILS.HandleAwsError.decorate_all_methods(UTILS.HandleAwsError.handle_aws_error)
class SSMCommands:
    """Class used to manage AWS SSM commands.

    This class provides the interface between the AWS SSM commands. 
    It is responsible for calling the AWS SSM commands, and providing
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
        self.iam_client = self.session.client('ssm')
        LOGGER.write('EC2Commands - init - IAM Commands Initialized')
    
    def get_all_parameters(self):
        """Function to return a list of all SSM parameters.

        Returns
        -------
        list
            A list of SSM parameter objects.
        """
        LOGGER.write('SSMCommands - get_all_parameters - Getting SSM Parameters')
        parameters = self.iam_client.describe_parameters()
        LOGGER.write('SSMCommands - get_all_parameters - SSM Parameters: {}'.format(parameters))
        LOGGER.write('SSMCommands - get_all_parameters - Got SSM Parameters')
        return parameters
    
    def get_parameter(self, name):
        """Function to return the details of a specific SSM parameter.

        Parameters
        ----------
        name : str
            The name of the SSM parameter.
        """
        LOGGER.write('SSMCommands - get_parameter - Getting SSM Parameter: {}'.format(name))
        parameter = self.iam_client.get_parameter(Name=name)
        LOGGER.write('SSMCommands - get_parameter - SSM Parameter: {}'.format(parameter))
        LOGGER.write('SSMCommands - get_parameter - Got SSM Parameter')
        return parameter
