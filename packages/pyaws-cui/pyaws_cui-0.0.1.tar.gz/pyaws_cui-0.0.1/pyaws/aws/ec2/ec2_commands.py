"""File containing functions used to call the underlying AWS EC2 commands.

This file is meant to handle the intermediate considerations between the
CUI and the AWS EC2 CLI. It is meant to be called by the CUI, and to call the
AWS CLI commands. It is not meant to be called directly by the user.
"""

# pyaws logger
import pyaws.logger as LOGGER
import pyaws.utils as UTILS

@UTILS.HandleAwsError.decorate_all_methods(UTILS.HandleAwsError.handle_aws_error)
class EC2Commands:
    """Class used to manage AWS EC2 commands.

    This class provides the interface between the AWS EC2 commands. 
    It is responsible for calling the AWS EC2 commands, and providing
    the results to other pyaws modules.

    Attributes
    ----------
    session : boto3.session.Session
        The AWS session object.
    """

    def __init__(self, session):
        """Constructor for EC2Commands class.
        Initializes the EC2Commands and establishes the AWS session.

        Parameters
        -------
        session : boto3.session.Session
            The AWS session object.
        """
        LOGGER.write('EC2Commands - init - Initializing EC2 Commands')
        self.session = session
        self.ec2_client = self.session.client('ec2')
        self.ec2_resource = self.session.resource('ec2')
        self.asg_client = self.session.client('autoscaling')
        self.elbv2_client = self.session.client('elbv2')
        # LOGGER.write('EC2Commands - init - EC2 Client: {}'.format(self.ec2_client))
        # LOGGER.write('EC2Commands - init - EC2 Resource: {}'.format(self.ec2_resource))
        LOGGER.write('EC2Commands - init - EC2 Commands initialized')

    
    # Instances
    def get_instances(self):
        """Gets the instances in the current session.

        Returns
        -------
        instances : list of dict
            The instances in the current session.
        """

        LOGGER.write('EC2Commands - get_instances - Fetching instances')
        instances = self.ec2_resource.instances.all()
        instances = list(instances)
        LOGGER.write('EC2Commands - get_instances - Got instances: {}'.format(instances))
        LOGGER.write('EC2Commands - get_instances - Got instances')
        return instances


    def get_instance_details(self, instance_id):
        """Gets the instance with the given instance id.

        Parameters
        ----------
        instance_id : str
            The instance id of the instance to get.

        Returns
        -------
        instance_details : dict
            The instance with the given instance id.
        """

        LOGGER.write('EC2Commands - get_instance_details - Instance ID: {}'.format(instance_id))
        instance = self.ec2_resource.Instance(instance_id)
        instance.load()
        if instance is None:
            LOGGER('EC2Commands - get_instance_details - No instance with ID: {}'.format(instance_id))
        instance_details = instance.meta.data
        LOGGER.write('EC2Commands - get_instance_details - Instance Details: {}'.format(instance_details))
        return instance_details


    # Images
    def get_images(self):
        """Gets the private images in the current session.

        Returns
        -------
        private_images : list of dict
            The private images in the current session.
        """
        LOGGER.write('EC2Commands - get_images - Getting private images')
        images = self.ec2_resource.images.filter(Owners=['self'])
        images = list(images)
        LOGGER.write('EC2Commands - get_images - Got private images')
        return images
    

    def get_image_details(self, image_id):
        """Gets the image with the given image id.

        Parameters
        ----------
        image_id : str
            The image id of the image to get.

        Returns
        -------
        image_details : dict
            The image with the given image id.
        """
        LOGGER.write('EC2Commands - get_image_details - Image ID: {}'.format(image_id))
        image = self.ec2_resource.Image(image_id)
        image.load()
        if image is None:
            LOGGER('EC2Commands - get_image_details - No image with ID: {}'.format(image_id))
        image_details = image.meta.data
        LOGGER.write('EC2Commands - get_image_details - Image Details: {}'.format(image_details))
        return image_details


    # Volumes
    def get_volumes(self):
        """Gets the volumes in the current session.

        Returns
        -------
        volumes : list of dict
            The volumes in the current session.
        """
        LOGGER.write('EC2Commands - get_volumes - Getting volumes')
        volumes = self.ec2_resource.volumes.all()
        volumes = list(volumes)
        LOGGER.write('EC2Commands - get_volumes - Got volumes')
        return volumes
    
    def get_volume_details(self, volume_id):
        """Gets the volume with the given volume id.

        Parameters
        ----------
        volume_id : str
            The volume id of the volume to get.

        Returns
        -------
        volume_details : dict
            The volume with the given volume id.
        """
        LOGGER.write('EC2Commands - get_volume_details - Volume ID: {}'.format(volume_id))
        volume = self.ec2_resource.Volume(volume_id)
        volume.load()
        if volume is None:
            LOGGER('EC2Commands - get_volume_details - No volume with ID: {}'.format(volume_id))
        volume_details = volume.meta.data
        LOGGER.write('EC2Commands - get_volume_details - Volume Details: {}'.format(volume_details))
        return volume_details


    # Snapshots
    def get_snapshots(self):
        """Gets the snapshots in the current session.

        Returns
        -------
        snapshots : list of dict
            The snapshots in the current session.
        """
        LOGGER.write('EC2Commands - get_snapshots - Getting snapshots')
        snapshots = self.ec2_resource.snapshots.filter(OwnerIds=['self'])
        LOGGER.write('EC2Commands - get_snapshots - Got snapshots')
        return snapshots
    
    def get_snapshot_details(self, snapshot_id):
        """Gets the snapshot details of the given snapshot id.

        Parameters
        ----------
        snapshot_id : str
            The snapshot id to get details for.

        Returns
        -------
        snapshot_details : dict
            The snapshot details of the given snapshot id.
        """
        LOGGER.write('EC2Commands - get_snapshot_details - Snapshot ID: {}'.format(snapshot_id))
        snapshot = self.ec2_resource.Snapshot(snapshot_id)
        snapshot.load()
        if snapshot is None:
            LOGGER('EC2Commands - get_snapshot_details - No snapshot with ID: {}'.format(snapshot_id))
        snapshot_details = snapshot.meta.data
        LOGGER.write('EC2Commands - get_snapshot_details - Snapshot Details: {}'.format(snapshot_details))
        return snapshot_details
    
    # Security Groups
    def get_security_groups(self):
        """Gets the security groups in the current session.

        Returns
        -------
        security_groups : list of dict
            The security groups in the current session.
        """
        LOGGER.write('EC2Commands - get_security_groups - Getting security groups')
        security_groups = self.ec2_resource.security_groups.all()
        LOGGER.write('EC2Commands - get_security_groups - Got security groups')
        return security_groups
    
    def get_security_group_details(self, security_group_id):
        """Gets the security group details of the given security group id.

        Parameters
        ----------
        security_group_id : str
            The security group id to get details for.

        Returns
        -------
        security_group_details : dict
            The security group details of the given security group id.
        """
        LOGGER.write('EC2Commands - get_security_group_details - Security Group ID: {}'.format(security_group_id))
        security_group = self.ec2_resource.SecurityGroup(security_group_id)
        security_group.load()
        if security_group is None:
            LOGGER('EC2Commands - get_security_group_details - No security group with ID: {}'.format(security_group_id))
        security_group_details = security_group.meta.data
        LOGGER.write('EC2Commands - get_security_group_details - Security Group Details: {}'.format(security_group_details))
        return security_group_details
    
    # Key Pairs
    def get_key_pairs(self):
        """Gets the key pairs in the current session.

        Returns
        -------
        key_pairs : list of dict
            The key pairs in the current session.
        """
        LOGGER.write('EC2Commands - get_key_pairs - Getting key pairs')
        key_pairs = self.ec2_client.describe_key_pairs()
        key_pairs = key_pairs['KeyPairs']
        LOGGER.write('EC2Commands - get_key_pairs - Got key pairs: {}'.format(key_pairs))
        return key_pairs
    
    def get_key_pair_details(self, key_pair_name):
        """Gets the key pair details of the given key pair id.

        Parameters
        ----------
        key_pair_id : str
            The key pair id to get details for.

        Returns
        -------
        key_pair_details : dict
            The key pair details of the given key pair id.
        """
        LOGGER.write('EC2Commands - get_key_pair_details - Key Pair ID: {}'.format(key_pair_name))
        key_pair = self.ec2_client.describe_key_pairs(KeyNames=[key_pair_name])
        key_pair = key_pair['KeyPairs']
        if key_pair is None:
            LOGGER('EC2Commands - get_key_pair_details - No key pair details with ID: {}'.format(key_pair_name))
        LOGGER.write('EC2Commands - get_key_pair_details - Key Pair Details: {}'.format(key_pair))
        return key_pair
    
    # Elastic IPs
    def get_elastic_ips(self):
        """Gets the elastic ips in the current session.

        Returns
        -------
        elastic_ips : list of dict
            The elastic ips in the current session.
        """
        LOGGER.write('EC2Commands - get_elastic_ips - Getting elastic ips')
        response = self.ec2_client.describe_addresses()
        elastic_ips = response['Addresses']
        LOGGER.write('EC2Commands - get_elastic_ips - Got elastic ips')
        return elastic_ips
    
    def get_elastic_ip_details(self, elastic_ip_id):
        """Gets the elastic ip details of the given elastic ip id.

        Parameters
        ----------
        elastic_ip_id : str
            The elastic ip id to get details for.

        Returns
        -------
        elastic_ip_details : dict
            The elastic ip details of the given elastic ip id.
        """
        LOGGER.write('EC2Commands - get_elastic_ip_details - Elastic IP ID: {}'.format(elastic_ip_id))
        elastic_ip = self.ec2_client.describe_addresses(PublicIps=[elastic_ip_id])
        if elastic_ip is None:
            LOGGER('EC2Commands - get_elastic_ip_details - No elastic ip with ID: {}'.format(elastic_ip_id))
        elastic_ip_details = elastic_ip['Addresses']
        LOGGER.write('EC2Commands - get_elastic_ip_details - Elastic IP Details: {}'.format(elastic_ip_details))
        return elastic_ip_details
    
    # Load Balancers
    def get_load_balancers(self):
        """Gets the load balancers in the current session.

        Returns
        -------
        load_balancers : list of dict
            The load balancers in the current session.
        """
        LOGGER.write('EC2Commands - get_load_balancers - Getting load balancers')
        response = self.elbv2_client.describe_load_balancers()
        load_balancers = response['LoadBalancers']
        LOGGER.write('EC2Commands - get_load_balancers - Got load balancers: {}'.format(load_balancers))
        return load_balancers
    
    def get_load_balancer_details(self, load_balancer_name):
        """Gets the load balancer details of the given load balancer id.

        Parameters
        ----------
        load_balancer_name : str
            The load balancer name to get details for.

        Returns
        -------
        load_balancer_details : dict
            The load balancer details of the given load balancer id.
        """
        LOGGER.write('EC2Commands - get_load_balancer_details - Load Balancer Name: {}'.format(load_balancer_name))
        response = self.elbv2_client.describe_load_balancers(Names=[load_balancer_name])
        if response is None:
            LOGGER('EC2Commands - get_load_balancer_details - No load balancer with Name: {}'.format(load_balancer_name))
        load_balancer_details = response['LoadBalancers']
        LOGGER.write('EC2Commands - get_load_balancer_details - Load Balancer Details: {}'.format(load_balancer_details))
        return load_balancer_details
    
    # Target Groups
    def get_target_groups(self):
        """Gets the target groups in the current session.

        Returns
        -------
        target_groups : list of dict
            The target groups in the current session.
        """
        LOGGER.write('EC2Commands - get_target_groups - Getting target groups')
        response = self.elbv2_client.describe_target_groups()
        target_groups = response['TargetGroups']
        LOGGER.write('EC2Commands - get_target_groups - Got target groups: {}'.format(target_groups))
        return target_groups

    def get_target_group_details(self, target_group_name):
        """Gets the target group details of the given target group id.

        Parameters
        ----------
        target_group_name : str
            The target group id to get details for.

        Returns
        -------
        target_group_details : dict
            The target group details of the given target group id.
        """
        LOGGER.write('EC2Commands - get_target_group_details - Target Group Name: {}'.format(target_group_name))
        response = self.elbv2_client.describe_target_groups(Names=[target_group_name])
        if response is None:
            LOGGER('EC2Commands - get_load_balancer_details - No target group with Name: {}'.format(target_group_name))
        target_group_details = response['TargetGroups']
        LOGGER.write('EC2Commands - get_target_group_details - Target Group Details: {}'.format(target_group_details))
        return target_group_details


    # Launch Templates
    def get_launch_templates(self):
        """Gets the launch templates in the current session.

        Returns
        -------
        launch_templates : list of dict
            The launch templates in the current session.
        """

        LOGGER.write('EC2Commands - get_launch_templates - Getting launch templates')
        response = self.ec2_client.describe_launch_templates()
        launch_templates = response['LaunchTemplates']
        LOGGER.write('EC2Commands - get_launch_templates - Got launch templates')
        return launch_templates


    def get_launch_template_details(self, launch_template_id):
        """Gets the launch template details of the given launch template id.

        Parameters
        ----------
        launch_template_id : str
            The launch template id to get details for.

        Returns
        -------
        launch_template_details : dict
            The launch template details of the given launch template id.
        """
        LOGGER.write('EC2Commands - get_launch_template_details - Launch Template ID: {}'.format(launch_template_id))
        launch_template = self.ec2_client.describe_launch_template_versions(LaunchTemplateName=launch_template_id, Versions=['$Default'])
        if launch_template is None:
            LOGGER('EC2Commands - get_launch_template_details - No launch template with ID: {}'.format(launch_template_id))
        launch_template_details = launch_template['LaunchTemplateVersions']
        LOGGER.write('EC2Commands - get_launch_template_details - Launch Template Details: {}'.format(launch_template_details))
        return launch_template_details


    # Auto Scaling Groups
    def get_auto_scaling_groups(self):
        """Gets the auto scaling groups in the current session.

        Returns
        -------
        auto_scaling_groups : list of dict
            The auto scaling groups in the current session.
        """
        LOGGER.write('EC2Commands - get_auto_scaling_groups - Getting auto scaling groups')
        response = self.asg_client.describe_auto_scaling_groups()
        auto_scaling_groups = response['AutoScalingGroups']
        LOGGER.write('EC2Commands - get_auto_scaling_groups - Got auto scaling groups: {}'.format(auto_scaling_groups))
        return auto_scaling_groups


    def get_auto_scaling_group_details(self, auto_scaling_group_name):
        """Gets the auto scaling group details of the given auto scaling group name.

        Parameters
        ----------
        auto_scaling_group_name : str
            The auto scaling group name to get details for.

        Returns
        -------
        auto_scaling_group_details : dict
            The auto scaling group details of the given auto scaling group name.
        """
        LOGGER.write('EC2Commands - get_auto_scaling_group_details - Auto Scaling Group Name: {}'.format(auto_scaling_group_name))
        auto_scaling_group = self.asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=[auto_scaling_group_name])
        if auto_scaling_group is None:
            LOGGER('EC2Commands - get_auto_scaling_group_details - No auto scaling group with Name: {}'.format(auto_scaling_group_name))
        auto_scaling_group_details = auto_scaling_group['AutoScalingGroups']
        LOGGER.write('EC2Commands - get_auto_scaling_group_details - Auto Scaling Group Details: {}'.format(auto_scaling_group_details))
        return auto_scaling_group_details