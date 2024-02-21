"""File containing functions used for creating display tables for ec2 resources.

This file is meant to contain the set of functions used to create display tables
for ec2 resources.
"""

import base64
import binascii

from tabulate import tabulate

import pyaws.aws.ec2 as EC2
import pyaws.logger as LOGGER

class EC2ConsoleTables:
    """Class responsible for creating display tables for ec2 resources.
    
    Attributes
    ----------
    LOGGER : obj
        The logger object used for logging output to the console.

    Methods
    -------
    build_instance_details_table(instance_details)
        Function to display the details of the selected instance.
    build_image_details_table(image_details)
        Function to build the table of image details.
    build_volume_details_table(volume_details)
        Function to build the table of volume details.
    build_snapshot_details_table(snapshot_details)
        Function to build the table of snapshot details.
    build_security_group_details_table(security_group_details)
        Function to build the table of security group details.
    build_key_pair_details_table(key_pair_details)
        Function to build the table of key pair details.
    build_elastic_ip_details_table(elastic_ip_details)
        Function to build the table of elastic IP details.
    build_load_balancer_details_table(load_balancer_details)
        Function to build the table of load balancer details.
    build_target_group_details_table(target_group_details)
        Function to build the table of target group details.
    build_launch_template_details_table(launch_template_details)
        Function to build the table of launch template details.
    """


    def build_instance_details_table(self, instance_details):
        """Function to display the details of the selected instance.

        Parameters
        ----------
        instance_details : dict
            The instance_details to display the details of.
        
        Returns
        -------
        table : str
            The table of instance details.
        """
        self.instance_name = EC2.get_instance_name(instance_details=instance_details) or "Error loading detail."
        LOGGER.write('EC2ConsoleManager - build_instance_details_table - Building Instance Details Table')
        table = [['Attribute',              'Value'],
                    ['Name',                self.instance_name],
                    ['ID',                  instance_details.get('InstanceId', 'Error loading detail.')],
                    ['State',               instance_details.get('State', {}).get('Name', 'Error loading detail.')],
                    ['Type',                instance_details.get('InstanceType', 'Error loading detail.')],
                    ['AMI ID',              instance_details.get('ImageId', 'Error loading detail.')],
                    ['Key Name',            instance_details.get('KeyName', 'Error loading detail.')],
                    ['Security Groups',     instance_details.get('SecurityGroups', 'Error loading detail.')],
                    ['IAM Role',            instance_details.get('IamInstanceProfile', {}).get('Arn', 'Error loading detail.')],
                    ['Architecture',        instance_details.get('Architecture', 'Error loading detail.')],
                    ['Launch Time',         instance_details.get('LaunchTime', 'Error loading detail.')],
                    ['Public DNS Name',     instance_details.get('PublicDnsName', 'Error loading detail.')],
                    ['Public IP',           instance_details.get('PublicIpAddress', 'Error loading detail.')],
                    ['Private IP',          instance_details.get('PrivateIpAddress', 'Error loading detail.')],
                    ['PEM Key Name',        instance_details.get('KeyName', 'Error loading detail.')],
                    ['VPC ID',              instance_details.get('VpcId', 'Error loading detail.')],
                    ['Subnet ID',           instance_details.get('SubnetId', 'Error loading detail.')]]
        return (tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
    

    def build_image_details_table(self, image_details):
        """Function to build the table of image details.

        Parameters
        ----------
        image_details : dict
            The image details to build the table of details for.
        
        Returns
        -------
        table : str
            The table of image details.
        """

        LOGGER.write('EC2ConsoleManager - build_image_details_table - Building Image Details Table')
        table = [['Attribute',              'Value'],
                 ['ID',                     image_details.get('ImageId', 'Error loading detail.')],
                 ['Name',                   image_details.get('Name', 'Error loading detail.')],
                 ['Description',            image_details.get('Description', 'Error loading detail.')],
                 ['Architecture',           image_details.get('Architecture', 'Error loading detail.')],
                 ['Creation Date',          image_details.get('CreationDate', 'Error loading detail.')],
                 ['Image Location',         image_details.get('ImageLocation', 'Error loading detail.')],
                 ['Image Type',             image_details.get('ImageType', 'Error loading detail.')],
                 ['Public',                 image_details.get('Public', 'Error loading detail.')],
                 ['Kernel ID',              image_details.get('KernelId', 'Error loading detail.')],
                 ['Owner ID',               image_details.get('OwnerId', 'Error loading detail.')],
                 ['Ramdisk ID',             image_details.get('RamdiskId', 'Error loading detail.')],
                 ['State',                  image_details.get('State', 'Error loading detail.')],
                 ['Hypervisor',             image_details.get('Hypervisor', 'Error loading detail.')],
                 ['Root Device Name',       image_details.get('RootDeviceName', 'Error loading detail.')],
                 ['Root Device Type',       image_details.get('RootDeviceType', 'Error loading detail.')],
                 ['Virtualization Type',    image_details.get('VirtualizationType', 'Error loading detail.')],
                 ['Tags',                   image_details.get('Tags', 'Error loading detail.')]]
        return tabulate(table, headers='firstrow', tablefmt='fancy_grid')


    def build_volume_details_table(self, volume_details):
        """Function to build the table of volume details.

        Parameters
        ----------
        volume_details : dict
            The volume details to build the table of details for.
        
        Returns
        -------
        table : str
            The table of volume details.
        """

        LOGGER.write('EC2ConsoleManager - build_volume_details_table - Building Volume Details Table')
        table = [['Attribute',              'Value'],
                 ['ID',                     volume_details.get('VolumeId', 'Error loading detail.')],
                 ['Name',                   volume_details.get('Name', 'Error loading detail.')],
                 ['Description',            volume_details.get('Description', 'Error loading detail.')],
                 ['Availability Zone',      volume_details.get('AvailabilityZone', 'Error loading detail.')],
                 ['State',                  volume_details.get('State', 'Error loading detail.')],
                 ['Encrypted',              volume_details.get('Encrypted', 'Error loading detail.')],
                 ['IOPS',                   volume_details.get('Iops', 'Error loading detail.')],
                 ['KMS Key ID',             volume_details.get('KmsKeyId', 'Error loading detail.')],
                 ['Size',                   volume_details.get('Size', 'Error loading detail.')],
                 ['Snapshot ID',            volume_details.get('SnapshotId', 'Error loading detail.')],
                 ['Volume Type',            volume_details.get('VolumeType', 'Error loading detail.')],
                 ['Tags',                   volume_details.get('Tags', '')]]
        return tabulate(table, headers='firstrow', tablefmt='fancy_grid')


    def build_snapshot_details_table(self, snapshot_details):
        """Function to build the table of snapshot details.

        Parameters
        ----------
        snapshot_details : dict
            The snapshot details to build the table of details for.
        
        Returns
        -------
        table : str
            The table of snapshot details.
        """

        LOGGER.write('EC2ConsoleManager - build_snapshot_details_table - Building Snapshot Details Table')
        table = [['Attribute',              'Value'],
                    ['ID',                     snapshot_details.get('SnapshotId', 'Error loading detail.')],
                    ['Description',            snapshot_details.get('Description', 'Error loading detail.')],
                    ['State',                  snapshot_details.get('State', 'Error loading detail.')],
                    ['Volume ID',              snapshot_details.get('VolumeId', 'Error loading detail.')],
                    ['Volume Size',            snapshot_details.get('VolumeSize', 'Error loading detail.')],
                    ['Encrypted',              snapshot_details.get('Encrypted', 'Error loading detail.')],
                    ['Owner ID',               snapshot_details.get('OwnerId', 'Error loading detail.')],
                    ['Progress',               snapshot_details.get('Progress', 'Error loading detail.')],
                    ['Start Time',             snapshot_details.get('StartTime', 'Error loading detail.')],
                    ['Tags',                   snapshot_details.get('Tags', 'Error loading detail.')]]
        return tabulate(table, headers='firstrow', tablefmt='fancy_grid')


    def build_security_group_details_table(self, security_group_details):
        """Function to build the table of security group details.

        Parameters
        ----------
        security_group_details : dict
            The security group details to build the table of details for.
        
        Returns
        -------
        table : str
            The table of security group details.
        """
        LOGGER.write('EC2ConsoleManager - build_security_group_details_table - Building Security Group Details Table')
        table = [['Attribute',              'Value'],
                    ['ID',                     security_group_details.get('GroupId', 'Error loading detail.')],
                    ['Name',                   security_group_details.get('GroupName', 'Error loading detail.')],
                    ['Description',            security_group_details.get('Description', 'Error loading detail.')],
                    ['VPC ID',                 security_group_details.get('VpcId', 'Error loading detail.')],
                    ['Owner ID',               security_group_details.get('OwnerId', 'Error loading detail.')]]
                    # ['Inbound Rules',          security_group_details.get('IpPermissions', 'Error loading detail.')]] # Moved to its own table.
                    # ['Outbound Rules',         security_group_details.get('IpPermissionsEgress', 'Error loading detail.')]] # This is so rarely looked at, removing it for now.
        table = tabulate(table, headers='firstrow', tablefmt='fancy_grid')
        # Special accomodation for inbound rules. This will need to change when the functionality of the manager screen is expanded to include secondary resources.
        inbound_rules = security_group_details.get('IpPermissions', 'Error loading detail.')
        inbound_rules_table = self.build_security_group_inbound_rules_table(inbound_rules=inbound_rules)
        table += '\n\n'
        table += 'Inbound Rules:\n'
        table += inbound_rules_table
        return table
    #
    def build_security_group_inbound_rules_table(self, inbound_rules):
        """Function to build the table of security group inbound rules.

        Parameters
        ----------
        inbound_rules : dict
            The inbound rules to build the table of details for.
        
        Returns
        -------
        table : str
            The table of security group inbound rules.
        """
        inbound_rules_table = [['Protocol', 'Port Range', 'Source', 'Description'],
                                ['--------', '----------', '------', '-----------']]

        for rule in inbound_rules:
            protocol = rule.get('IpProtocol', 'N/A')
            port_range = f"{rule.get('FromPort', 'N/A')}-{rule.get('ToPort', 'N/A')}"
            ip_ranges = rule.get('IpRanges', [])
            source = ip_ranges[0].get('CidrIp') if ip_ranges else 'N/A'
            description = rule.get('Description', 'N/A')

            inbound_rules_table.append([protocol, port_range, source, description])
        return tabulate(inbound_rules_table, headers='firstrow', tablefmt='fancy_grid')


    def build_key_pair_details_table(self, key_pair_details):
        """Function to build the table of key pair details.

        Parameters
        ----------
        key_pair_details : dict
            The key pair details to build the table of details for.
        
        Returns
        -------
        table : str
            The table of key pair details.
        """
        key_pair_details = key_pair_details[0]
        LOGGER.write('EC2ConsoleManager - build_key_pair_details_table - Building Key Pair Details Table')
        table = [['Attribute',              'Value'],
                    ['Name',                   key_pair_details.get('KeyName', 'Error loading detail.')],
                    ['ID',                     key_pair_details.get('KeyPairId', 'Error loading detail.')],
                    ['Type',                   key_pair_details.get('KeyType', 'Error loading detail.')],
                    ['Created Time',           key_pair_details.get('CreateTime', 'Error loading detail.')],
                    ['Fingerprint',            key_pair_details.get('KeyFingerprint', 'Error loading detail.')],
                    ['Tags',                   key_pair_details.get('Tags', 'Error loading detail.')]]
        return tabulate(table, headers='firstrow', tablefmt='fancy_grid')


    # Alternative display for Elastic IP details. Shows one IP per row. More suitable for a table. of all Elastic IPs and their details.
    def build_elastic_ip_table(self, elastic_ip_details_list):
        """Function to build the table of elastic IP details.

        Parameters
        ----------
        elastic_ip_details_list : list
            The list of elastic IP details to build the table of details for.
        
        Returns
        -------
        table : str
            The table of elastic IP details.
        """

        LOGGER.write('EC2ConsoleManager - build_elastic_ip_details_table - Building Elastic IP Details Table')

        # Initialize the table with headers
        table = [['ID', 'Allocation ID', 'Domain', 'Instance ID', 'Network Interface ID', 'Private IP Address', 'Tags']]

        # Add a row to the table for each elastic IP detail
        for elastic_ip_details in elastic_ip_details_list:
            row = [
                elastic_ip_details.get('PublicIp', 'Error loading detail.'),
                elastic_ip_details.get('AllocationId', 'Error loading detail.'),
                elastic_ip_details.get('Domain', 'Error loading detail.'),
                elastic_ip_details.get('InstanceId', 'Error loading detail.'),
                elastic_ip_details.get('NetworkInterfaceId', 'Error loading detail.'),
                elastic_ip_details.get('PrivateIpAddress', 'Error loading detail.'),
                elastic_ip_details.get('Tags', 'Error loading detail.')
            ]
            table.append(row)

        return tabulate(table, headers='firstrow', tablefmt='fancy_grid')


    def build_elastic_ip_details_table(self, elastic_ip_details):
        """Function to build the table of elastic IP details.

        Parameters
        ----------
        elastic_ip_details : dict
            The elastic IP details to build the table of details for.
        
        Returns
        -------
        table : str
            The table of elastic IP details.
        """

        LOGGER.write('EC2ConsoleManager - build_elastic_ip_details_table - Building Elastic IP Details Table')
        elastic_ip_details = elastic_ip_details[0]
        table = [['Attribute',              'Value'],
                    ['ID',                     elastic_ip_details.get('PublicIp', 'Error loading detail.')],
                    ['Allocation ID',          elastic_ip_details.get('AllocationId', 'Error loading detail.')],
                    ['Domain',                 elastic_ip_details.get('Domain', 'Error loading detail.')],
                    ['Instance ID',            elastic_ip_details.get('InstanceId', 'Error loading detail.')],
                    ['Network Interface ID',   elastic_ip_details.get('NetworkInterfaceId', 'Error loading detail.')],
                    ['Private IP Address',     elastic_ip_details.get('PrivateIpAddress', 'Error loading detail.')],
                    ['Tags',                   elastic_ip_details.get('Tags', 'Error loading detail.')]]
        return tabulate(table, headers='firstrow', tablefmt='fancy_grid')


    def build_load_balancer_details_table(self, load_balancer_details):
        """Function to build the table of load balancer details.

        Parameters
        ----------
        load_balancer_details : dict
            The load balancer details to build the table of details for.
        
        Returns
        -------
        table : str
            The table of load balancer details.
        """

        LOGGER.write('EC2ConsoleManager - build_load_balancer_details_table - Building Load Balancer Details Table')
        load_balancer_details = load_balancer_details[0]
        table = [['Attribute',              'Value'],
                    ['Name',                        load_balancer_details.get('LoadBalancerName', 'Error loading detail.')],
                    ['ARN',                         load_balancer_details.get('LoadBalancerArn', 'Error loading detail.')],
                    ['Type',                        load_balancer_details.get('Type', 'Error loading detail.')],
                    ['Scheme',                      load_balancer_details.get('Scheme', 'Error loading detail.')],
                    ['VPC ID',                      load_balancer_details.get('VpcId', 'Error loading detail.')],
                    ['State',                       load_balancer_details.get('State', 'Error loading detail.')],
                    ['DNS Name',                    load_balancer_details.get('DNSName', 'Error loading detail.')],
                    ['Canonical Hosted Zone ID',    load_balancer_details.get('CanonicalHostedZoneId', 'Error loading detail.')],
                    ['Created Time',                load_balancer_details.get('CreatedTime', 'Error loading detail.')],
                    ['Availability Zones',          load_balancer_details.get('AvailabilityZones', 'Error loading detail.')],
                    ['Security Groups',             load_balancer_details.get('SecurityGroups', 'Error loading detail.')],
                    ['AvailabilityZones',           load_balancer_details.get('AvailabilityZones', 'Error loading detail.')],
                    ['IP Address Type',             load_balancer_details.get('IpAddressType', 'Error loading detail.')],
                    ['Tags',                        load_balancer_details.get('Tags', 'Error loading detail.')]]
        return tabulate(table, headers='firstrow', tablefmt='fancy_grid')


    def build_target_group_details_table(self, target_group_details):
        """Function to build the table of target group details.

        Parameters
        ----------
        target_group_details : dict
            The target group details to build the table of details for.
        
        Returns
        -------
        table : str
            The table of target group details.
        """

        LOGGER.write('EC2ConsoleManager - build_target_group_details_table - Building Target Group Details Table')
        target_group_details = target_group_details[0]
        table = [['Attribute',              'Value'],
                    ['Name',                   target_group_details.get('TargetGroupName', 'Error loading detail.')],
                    ['ARN',                    target_group_details.get('TargetGroupArn', 'Error loading detail.')],
                    ['Protocol',               target_group_details.get('Protocol', 'Error loading detail.')],
                    ['Port',                   target_group_details.get('Port', 'Error loading detail.')],
                    ['VPC ID',                 target_group_details.get('VpcId', 'Error loading detail.')],
                    ['Health Check Protocol',  target_group_details.get('HealthCheckProtocol', 'Error loading detail.')],
                    ['Health Check Port',      target_group_details.get('HealthCheckPort', 'Error loading detail.')],
                    ['Health Check Enabled',   target_group_details.get('HealthCheckEnabled', 'Error loading detail.')],
                    ['Health Check Interval',  target_group_details.get('HealthCheckIntervalSeconds', 'Error loading detail.')],
                    ['Health Check Timeout',   target_group_details.get('HealthCheckTimeoutSeconds', 'Error loading detail.')],
                    ['Healthy Threshold',      target_group_details.get('HealthyThresholdCount', 'Error loading detail.')],
                    ['Unhealthy Threshold',    target_group_details.get('UnhealthyThresholdCount', 'Error loading detail.')],
                    ['Health Check Path',      target_group_details.get('HealthCheckPath', 'Error loading detail.')],
                    ['Matcher',                target_group_details.get('Matcher', 'Error loading detail.')],
                    ['Load Balancer ARN',      target_group_details.get('LoadBalancerArns', 'Error loading detail.')],
                    ['Target Type',            target_group_details.get('TargetType', 'Error loading detail.')],
                    ['Tags',                   target_group_details.get('Tags', 'Error loading detail.')]]
        return tabulate(table, headers='firstrow', tablefmt='fancy_grid')


    def build_launch_template_details_table(self, launch_template_details):
        """Function to build the table of launch template details.

        Parameters
        ----------
        launch_template_details : dict
            The launch template details to build the table of details for.
        
        Returns
        -------
        table : str
            The table of launch template details.
        """

        LOGGER.write('EC2ConsoleManager - build_launch_template_details_table - Building Launch Template Details Table')
        launch_template_details = launch_template_details[0]
        table = [['Attribute',              'Value'],
                    ['ID',                     launch_template_details.get('LaunchTemplateId', 'Error loading detail.')],
                    ['Name',                   launch_template_details.get('LaunchTemplateName', 'Error loading detail.')],
                    ['Created Time',           launch_template_details.get('CreateTime', 'Error loading detail.')],
                    ['Created By',             launch_template_details.get('CreatedBy', 'Error loading detail.')],
                    ['Version Number',         launch_template_details.get('VersionNumber', 'Error loading detail.')],
                    ['Default Version',    str(launch_template_details.get('DefaultVersion', 'Error loading detail.'))]] # Convert boolean value to string
        table = tabulate(table, headers='firstrow', tablefmt='fancy_grid')
        # Special accommodation for instance details. This will need to change when the functionality of the manager screen is expanded to include secondary resources.
        instance_details_table = self.build_launch_template_instance_details_table(launch_template_details=launch_template_details)
        table += '\n\n'
        table += 'Instance Details:\n'
        table += instance_details_table
        return table


    def build_launch_template_instance_details_table(self, launch_template_details):
        """Function to build the table of launch template versions instance details.

        Parameters
        ----------
        launch_template_details : dict
            The launch template versions to build the table of details for.
        
        Returns
        -------
        table : str
            The table of launch template versions instance details.
        """
        launch_template_details = launch_template_details['LaunchTemplateData']
        LOGGER.write('EC2ConsoleManager - build_launch_template_versions_instance_details_table - Building Launch Template Versions Instance Details Table')
        table = [['Attribute',              'Value'],
                    ['AMI ID',                 launch_template_details.get('ImageId', 'Error loading detail.')],
                    ['Key Name',               launch_template_details.get('KeyName', 'Error loading detail.')],
                    ['Instance Type',          launch_template_details.get('InstanceType', 'Error loading detail.')],
                    ['Security Groups',        launch_template_details.get('SecurityGroupIds', 'Error loading detail.')]
                    ]
        table = tabulate(table, headers='firstrow', tablefmt='fancy_grid')
        table += '\n\n'
        userdata = launch_template_details.get('UserData', None)
        if userdata is not None:
            try:
                userdata_decoded = base64.b64decode(userdata).decode('utf-8')
            except binascii.Error:
                userdata_decoded = 'Error: UserData is not a valid base64 string.'
        else:
            userdata_decoded = 'Error loading detail.'

        table += 'Userdata:\n\n'
        table += userdata_decoded
        return table


    def build_auto_scaling_group_details_table(self, auto_scaling_group_details):
        """Function to build the table of auto scaling group details.

        Parameters
        ----------
        auto_scaling_group_details : dict
            The auto scaling group details to build the table of details for.
        
        Returns
        -------
        table : str
            The table of auto scaling group details.
        """

        auto_scaling_group_details = auto_scaling_group_details[0]
        LOGGER.write('EC2ConsoleManager - build_auto_scaling_group_details_table - Building Auto Scaling Group Details Table')
        table = [['Attribute',              'Value'],
                    ['Name',                   auto_scaling_group_details.get('AutoScalingGroupName', 'Error loading detail.')],
                    ['ARN',                    auto_scaling_group_details.get('AutoScalingGroupARN', 'Error loading detail.')],
                    ['Min Size',               auto_scaling_group_details.get('MinSize', 'Error loading detail.')],
                    ['Max Size',               auto_scaling_group_details.get('MaxSize', 'Error loading detail.')],
                    ['Desired Capacity',       auto_scaling_group_details.get('DesiredCapacity', 'Error loading detail.')],
                    ['Health Check Grace Period', auto_scaling_group_details.get('HealthCheckGracePeriod', 'Error loading detail.')],
                    ['Launch Configuration Name', auto_scaling_group_details.get('LaunchConfigurationName', 'Error loading detail.')],
                    ['Launch Template ID', auto_scaling_group_details.get('LaunchTemplate', {}).get('LaunchTemplateId', 'Error loading detail.')],
                    ['Launch Template Name', auto_scaling_group_details.get('LaunchTemplate', {}).get('LaunchTemplateName', 'Error loading detail.')],
                    ['Launch Template Version', auto_scaling_group_details.get('LaunchTemplate', {}).get('Version', 'Error loading detail.')],
                    ['Load Balancer Names',    auto_scaling_group_details.get('LoadBalancerNames', 'Error loading detail.')],
                    ['Target Group ARNs',      auto_scaling_group_details.get('TargetGroupARNs', 'Error loading detail.')],
                    ['Default Cooldown',       auto_scaling_group_details.get('DefaultCooldown', 'Error loading detail.')],
                    ['Health Check Type',      auto_scaling_group_details.get('HealthCheckType', 'Error loading detail.')],
                    ['VPC Zone Identifier',    auto_scaling_group_details.get('VPCZoneIdentifier', 'Error loading detail.')],
                    ['Availability Zones',      auto_scaling_group_details.get('AvailabilityZones', 'Error loading detail.')],
                    # ['New Instances Protected From Scale In', auto_scaling_group_details.get('NewInstancesProtectedFromScaleIn', 'Error loading detail.')],
                    ['Tags',                   auto_scaling_group_details.get('Tags', 'Error loading detail.')]]
        table = tabulate(table, headers='firstrow', tablefmt='fancy_grid')
        return table