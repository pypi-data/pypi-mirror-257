"""File containing functions used to call the underlying AWS Route53 commands

This file is meant to handle the intermediate considerations between the
CUI and the AWS R53 CLI. It is meant to be called by the CUI, and to call the
AWS CLI commands. It is not meant to be called directly by the user.
"""

# pyaws imports
import pyaws.logger as LOGGER
import pyaws.utils as UTILS

@UTILS.HandleAwsError.decorate_all_methods(UTILS.HandleAwsError.handle_aws_error)
class R53Commands:
    """Class used to manage AWS R53 commands.

    This class provides the interface between the AWS R53 commands. 
    It is responsible for calling the AWS R53 commands, and providing
    the results to other pyaws modules.

    Attributes
    ----------
    session : boto3.session.Session
        The AWS session object.
    """

    def __init__(self, session):
        """Constructor for R53Commands class.

        Parameters
        ----------
        session : boto3.session.Session
            The AWS session object.
        """
        LOGGER.write('EC2Commands - init - Initializing R53 Commands')
        self.session = session
        self.r53_client = self.session.client('route53')
        LOGGER.write('EC2Commands - init - R53 Commands Initialized')


    def get_hosted_zones(self):
        """List all hosted zones.

        This function lists all hosted zones in the current AWS account.

        Returns
        -------
        dict
            The response from the AWS CLI.
        """
        LOGGER.write('R53Commands - list_hosted_zones - Listing all hosted zones')
        response = self.r53_client.list_hosted_zones()
        LOGGER.write('R53Commands - list_hosted_zones - Hosted zones: ' + str(response))
        return response
    
    def get_hosted_zone_details(self, hosted_zone_id):
        """List all resource record sets in a hosted zone.

        This function lists all resource record sets in a hosted zone.

        Parameters
        ----------
        hosted_zone_id : str
            The hosted zone id.

        Returns
        -------
        dict
            The response from the AWS CLI.
        """
        LOGGER.write('R53Commands - list_resource_record_sets - Listing all resource record sets')
        response = self.r53_client.list_resource_record_sets(HostedZoneId=hosted_zone_id)
        LOGGER.write('R53Commands - list_resource_record_sets - Resource record sets: ' + str(response))
        return response