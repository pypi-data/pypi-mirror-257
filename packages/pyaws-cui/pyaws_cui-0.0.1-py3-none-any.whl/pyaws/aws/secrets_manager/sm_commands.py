"""File containing functions for the secrets manager commands.

This file is meant to handle the intermediate considerations between the
CUI and the AWS CLI. It is meant to be called by the CUI, and to call the
AWS CLI commands. It is not meant to be called directly by the user.
"""

# pyaws imports
import pyaws.logger as LOGGER
import pyaws.utils as UTILS


@UTILS.HandleAwsError.decorate_all_methods(UTILS.HandleAwsError.handle_aws_error)
class SecretsManagerCommands:
    """Class used to use manager AWS Secrets Manager commands.

    This class provides the interface between the AWS SecretsManager commands and the underlying
    AWS SDK. It is responsible for calling the AWS SecretsManager commands, and providing
    the results to other pyaws modules.

    Attributes
    ----------
    session : boto3.session.Session
        The AWS session object.
    """

    def __init__(self, session):
        """Initialize the SecretsManagerCommands class.

        Parameters
        ----------
        session : boto3.session.Session
            The AWS session object.
        """

        LOGGER.write('EC2Commands - init - Initializing EC2 Commands')
        self.session = session
        self.secrets_manager_client = self.session.client('secretsmanager')
        # self.secrets_manager_resource = self.session.resource('secretsmanager')
        LOGGER.write('EC2Commands - init - EC2 Client: {}'.format(self.secrets_manager_client))
        # LOGGER.write('EC2Commands - init - EC2 Resource: {}'.format(self.secrets_manager_resource))
        LOGGER.write('EC2Commands - init - EC2 Commands initialized')


    def get_secret_names(self):
        """Get the secrets from the AWS Secrets Manager.

        Returns
        -------
        list
            A list of the secret names.
        """

        LOGGER.write('SecretsManagerCommands - get_secrets - Getting secrets')
        secrets = self.secrets_manager_client.list_secrets()
        secrets = secrets['SecretList']
        secrets = [secret['Name'] for secret in secrets]
        LOGGER.write('SecretsManagerCommands - get_secrets - Secrets: {}'.format(secrets))
        return secrets


    def get_all_secret_versions(self, secret_name):
        """Get all the secret versions in the AWS Secrets Manager.

        Parameters
        ----------
        secret_name : str
            The name of the secret to get the versions of.

        Returns
        -------
        list
            The secret versions.
        """

        LOGGER.write('SecretsManagerCommands - get_all_secret_versions - Getting secret versions')
        secret_versions = self.secrets_manager_client.list_secret_version_ids(SecretId=secret_name, IncludeDeprecated=True, MaxResults=100)
        secret_versions = secret_versions['Versions']
        # secret_versions = [secret_version['VersionId'] for secret_version in secret_versions]

        # Get full metadata for each version
        for version in secret_versions:
            version_id = version['VersionId']
            version_metadata = self.secrets_manager_client.get_secret_value(SecretId=secret_name, VersionId=version_id)
            version['CreatedDate'] = version_metadata['CreatedDate']
        
        # Sort versions by CreatedDate
        secret_versions.sort(key=lambda version: version['CreatedDate'], reverse=True)

        # Ensure AWSCURRENT and AWSPREVIOUS are first and second
        secret_versions.sort(key=lambda version: 'AWSPREVIOUS' in version['VersionStages'] and 'AWSCURRENT' not in version['VersionStages'], reverse=True)
        secret_versions.sort(key=lambda version: 'AWSCURRENT' in version['VersionStages'], reverse=True)

        secret_versions = [secret_version['VersionId'] for secret_version in secret_versions]
        LOGGER.write('SecretsManagerCommands - get_all_secret_versions - Secret versions: {}'.format(secret_versions))
        return secret_versions


    def get_secret_version_data(self, secret_name, version_id):
        """Get the secret version in the AWS Secrets Manager.

        Parameters
        ----------
        secret_name : str
            The name of the secret to get the version of.
        version_id : str
            The version of the secret to get.

        Returns
        -------
        dict
            The secret version.
        """

        if secret_name == '':
            LOGGER.write('SecretsManagerCommands - get_secret_version_data - No secret name provided.')
            return None
        
        if version_id == '':
            LOGGER.write('SecretsManagerCommands - get_secret_version_data - No version id provided.')
            return None

        LOGGER.write('SecretsManagerCommands - get_secret_version_data - Getting secret version')
        secret_value = self.secrets_manager_client.get_secret_value(SecretId=secret_name, VersionId=version_id)
        if secret_value == '':
            LOGGER.write('SecretsManagerCommands - get_secret_version_data - No secret value data found.')
        # Intentionally not logging secret data.
        LOGGER.write('SecretsManagerCommands - get_secret_version_data - Fetched secret value data.')
        return secret_value


    def create_secret(self, secret_name, secret_value):
        """Create the secret in the AWS Secrets Manager.

        Parameters
        ----------
        secret_name : str
            The name of the secret to create.
        secret_value : str
            The value of the secret to create.

        Returns
        -------
        dict
            The secret.
        """

        LOGGER.write('SecretsManagerCommands - create_secret - Creating secret')
        secret = self.secrets_manager_client.create_secret(Name=secret_name, SecretString=secret_value)
        LOGGER.write('SecretsManagerCommands - create_secret - Secret: {}'.format(secret))
        return secret
    
    def delete_secret(self, secret_name):
        """Delete the secret in the AWS Secrets Manager.

        Parameters
        ----------
        secret_name : str
            The name of the secret to delete.

        Returns
        -------
        dict
            The secret.
        """

        LOGGER.write('SecretsManagerCommands - delete_secret - Deleting secret')
        secret = self.secrets_manager_client.delete_secret(SecretId=secret_name)
        LOGGER.write('SecretsManagerCommands - delete_secret - Secret: {}'.format(secret))
        return secret


    def update_secret(self, secret_name, secret_value):
        """Update the secret in the AWS Secrets Manager.

        Parameters
        ----------
        secret_name : str
            The name of the secret to update.
        secret_value : str
            The value of the secret to update.

        Returns
        -------
        dict
            The secret.
        """

        LOGGER.write('SecretsManagerCommands - update_secret - Updating secret')
        secret = self.secrets_manager_client.update_secret(SecretId=secret_name, SecretString=secret_value)
        LOGGER.write('SecretsManagerCommands - update_secret - Secret: {}'.format(secret))
        return secret