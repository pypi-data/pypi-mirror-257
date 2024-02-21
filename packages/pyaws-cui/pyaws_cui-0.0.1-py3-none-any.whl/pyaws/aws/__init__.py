"""AWS manager class. Responsible for establishing AWS session.

This module contains the main aws manager class, which is responsible for
esstablishing the AWS session and other AWS related utilities.
"""

# AWS SDK
import boto3

# pyaws imports
import pyaws.logger as LOGGER
import pyaws.utils as UTILS


class AWSManager:
    """Class used to manage AWS session and other AWS related utilities.

    This class provides the interface between the AWS session and the underlying
    AWS SDK. It is responsible for establishing the AWS session, and providing
    the AWS session to other pyaws modules.

    Attributes
    ----------
    session : boto3.session.Session
        The AWS session object.
    region : str
        The AWS region the session is in.
    profile : str
        The AWS profile the session is using.
    """

    def __init__(self, profile, region=None):
        """Constructor for AWSManager class.
        Initializes the AWSManager and establishes the AWS session.

        Returns
        -------
        session : boto3.session.Session
            The AWS session object.
        """
        LOGGER.write('AWSManager - init - Initializing AWS Manager')
        self.session = None
        self.region = region
        LOGGER.write('AWSManager - init - Region: {}'.format(self.region))
        self.profile = profile
        LOGGER.write('AWSManager - init - Profile: {}'.format(self.profile))
        
        # LOGGER.write('AWSManager - init - Establishing AWS Session')
        # connection_established = self.establish_aws_connection()
        # if connection_established:
        #     LOGGER.write('AWSManager - init - AWS Session established')
        #     return
        # elif not connection_established:
        #     LOGGER.write('AWSManager - init - AWS Session not established')
        #     return

    
    def establish_aws_connection(self): 
        """Establishes the AWS session using the AWS profile and region.

        Returns
        -------
        session : boto3.session.Session
            The AWS session object.
        """

        LOGGER.write('AWSManager - establish_aws_connection - Establishing AWS Session')
        self.session = boto3.session.Session(profile_name=self.profile, region_name=self.region)
        return self.check_aws_connection()


    def check_aws_connection(self): 
        """Checks if the AWS session is valid.

        Returns
        -------
        status : bool
            True if session is valid, False otherwise.
        """

        LOGGER.write('AWSManager - check_aws_connection - Checking AWS Session')
        if self.session is None:
            LOGGER.write('AWSManager - check_aws_connection - Session is empty.')
            return False
        try:
            LOGGER.write('AWSManager - check_aws_connection - Checking if session is valid.')
            self.session.client('sts').get_caller_identity()
            LOGGER.write('AWSManager - check_aws_connection - Session is valid.')
            return True
        except:
            LOGGER.write('AWSManager - check_aws_connection - Session is invalid.')
            return False
