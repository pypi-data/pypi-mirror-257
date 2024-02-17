import os
import boto3
from botocore.config import Config

from typing import List
from datetime import datetime, timedelta

from kypo.cloud_commons import (
    KypoCloudClientBase,
    TransformationConfiguration,
    TopologyInstance,
    HardwareUsage,
    Image,
    QuotaSet,
    Quota,
    Limits,
)

from .exceptions import ImageDoesNotExist, KeyPairDoesNotExist

from .aws_cdktf import cdktf_create_template


AWS_CREDENTIALS_FILE_TEMPLATE = '''[default]
aws_access_key_id = {}
aws_secret_access_key = {}
'''

AWS_CONFIG_FILE_TEMPLATE = '''[default]
region = {}
'''


class KypoAwsClient(KypoCloudClientBase):
    """
    TODO
    """
    AWS_BASE_DIR = '~/.aws'
    AWS_CREDENTIALS_FILE = f'{AWS_BASE_DIR}/credentials'
    AWS_CONFIG_FILE = f'{AWS_BASE_DIR}/config'

    def __init__(self, aws_access_key: str, aws_secret_key: str, region: str, availability_zone: str,
                 trc: TransformationConfiguration, ca_bundle: str = '/etc/ssl/certs/ca-certificates.crt'):
        """
        TODO
        """
        self.region = region
        self.availability_zone = availability_zone
        self.access_key = aws_access_key
        self.secret_key = aws_secret_key
        boto_client_config = Config(region_name=region, client_cert=ca_bundle)
        self.ec2_client = boto3.client(
            'ec2', aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            config=boto_client_config
        )
        self.cloadwatch_client = boto3.client(
            'cloudwatch', aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            config=boto_client_config
        )
        self.service_quotas_client = boto3.client(
            'service-quotas', aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            config=boto_client_config
        )

    @classmethod
    def _aws_cli_auth(cls, aws_access_key: str, aws_secret_key: str):
        """
        Authenticate AWS CLI tool.
        The AWS CLI tool reads '~/.aws/credentials' file.
        TODO: deprecate
        """
        os_path = os.path.expanduser(cls.AWS_CREDENTIALS_FILE)
        dir = os.path.dirname(os_path)
        os.makedirs(dir, exist_ok=True)
        with open(os_path, 'w') as cred_file:
            cred_file.write(AWS_CREDENTIALS_FILE_TEMPLATE.format(aws_access_key, aws_secret_key))
            cred_file.flush()

    @classmethod
    def _aws_cli_region(cls, region: str):
        """
        Configure AWS region.
        AWS checks '~/.aws/config' file for region setting.
        TODO: deprecate
        """
        os_path = os.path.expanduser(cls.AWS_CONFIG_FILE)
        dir = os.path.dirname(os_path)
        os.makedirs(dir, exist_ok=True)
        with open(os_path, 'w') as config_file:
            config_file.write(AWS_CONFIG_FILE_TEMPLATE.format(region))
            config_file.flush()

    def get_terraform_provider(self) -> str:
        """
        Provider is included in the terraform template (created by cdktf).
        """
        return ''

    def create_terraform_template(self, topology_instance: TopologyInstance, *args, **kwargs):
        """
        Create terraform template that will be deployed.

        :param topology_instance: TopologyInstance used to create template
        :keyword key_pair_name_ssh: The name of SSH key pair in the cloud
        :keyword key_pair_name_cert: The name of certificate key pair in the cloud
        :keyword resource_prefix: The prefix of all resources
        :return: Terraform template as a string
        """
        return cdktf_create_template(topology_instance, self.region, self.access_key,
                                     self.secret_key, self.availability_zone, *args, **kwargs)

    @staticmethod
    def _map_aws_image(image_raw: dict) -> Image:
        return Image(os_distro=None, os_type=image_raw['PlatformDetails'], disk_format=None,
                     container_format=None, visibility=image_raw['Public'], size=0,
                     status=image_raw['State'], min_ram=0, min_disk=0,
                     created_at=image_raw['CreationDate'], updated_at=None, tags=[],
                     default_user=None, name=image_raw['Name'], owner_specified={})

    def list_images(self, public_images: bool = False) -> List[Image]:
        """
        List all available images on the cloud project.

        :return: List of Image objects.
        """
        owners = ['self']
        if public_images:
            owners.append('amazon')

        images_raw = self.ec2_client.describe_images(Owners=owners)['Images']
        return [self._map_aws_image(image_raw) for image_raw in images_raw]

    def get_image(self, image_id: str) -> Image:
        """
        Get Image object based on its ID.

        :param image_id: The ID of image on the cloud
        :return: Image object
        """
        image_raw = self.ec2_client.describe_images(ImageIds=[image_id])['Images']
        if not image_raw:
            raise ImageDoesNotExist(image_id)

        return self._map_aws_image(image_raw[0])

    def resume_node(self, node_id: str):
        """
        TODO
        """
        raise NotImplementedError

    def start_node(self, node_id: str):
        """
        TODO
        """
        raise NotImplementedError

    def reboot_node(self, node_id: str):
        """
        TODO
        """
        raise NotImplementedError

    def get_console_url(self, node_id: str, console_type: str):
        """
        TODO
        Actually, not sure if this is possible with AWS
        """
        return ''

    def create_keypair(self, name: str, public_key: str, key_type: str = 'ssh'):
        """
        Create key pair in cloud.

        :param name: Name of the key pair
        :param public_key: SSH public key or certificate, it None new is created
        :param key_type: IGNORED -- AWS will detect correct format
        :return: None
        """
        public_base64 = public_key.encode()
        self.ec2_client.import_key_pair(KeyName=name, PublicKeyMaterial=public_base64)

    def get_keypair(self, name: str) -> dict:
        """
        Get KeyPair instance from cloud.

        :param name: The name of key pair
        :return: Key pair information
        :raise KeyPairDoesNotExist: Key pair does not exist
        """
        key_pair = self.ec2_client.describe_key_pairs(KeyNames=[name])['KeyPairs']
        if not key_pair:
            raise KeyPairDoesNotExist(name)

        return key_pair[0]

    def delete_keypair(self, name: str) -> None:
        """
        Delete key pair.

        :param name: The name of key pair
        :return: None
        """
        self.ec2_client.delete_key_pair(KeyName=name)

    def _get_service_quota(self, service_code: str, quota_code: str) -> float:
        return self.service_quotas_client.get_service_quota(
            ServiceCode=service_code,
            QuotaCode=quota_code
        )['Quota']['Value']

    def _get_vcpu_quota(self) -> Quota:
        vcpu_usage = self.cloadwatch_client.get_metric_statistics(
                MetricName='ResourceCount',
                Namespace='AWS/Usage',
                Dimensions=[{'Name': 'Type', 'Value': 'Resource'},
                            {'Name': 'Resource', 'Value': 'vCPU'},
                            {'Name': 'Service', 'Value': 'EC2'},
                            {'Name': 'Class', 'Value': 'Standard/OnDemand'}],
                StartTime=datetime.utcnow() - timedelta(seconds=300),
                EndTime=datetime.utcnow(),
                Period=60,
                Statistics=[
                    'Maximum'
                ],
                )

        vcpu_usage = vcpu_usage['Datapoints'][0]['Maximum']
        vcpu_limit = self._get_service_quota(
            service_code='ec2',
            quota_code='L-1216C47A'
        )
        vcpu_quota = Quota(limit=vcpu_limit, in_use=vcpu_usage)
        return vcpu_quota

    def _get_network_quota(self) -> Quota:
        vpcs_usage = len(self.ec2_client.describe_vpcs()['Vpcs'])
        vpcs_limit = self._get_service_quota(
            service_code='vpc',
            quota_code='L-F678F1CE',
        )

        return Quota(limit=vpcs_limit, in_use=vpcs_usage)

    def _get_ports_quota(self) -> Quota:
        ports_usage = len(self.ec2_client.describe_network_interfaces()['NetworkInterfaces'])
        ports_limit = self._get_service_quota(
            service_code='vpc',
            quota_code='L-DF5E4CA3',
        )

        return Quota(limit=ports_limit, in_use=ports_usage)

    def get_quota_set(self) -> QuotaSet:
        """
        Get quota set of cloud project.
        Note, AWS does not keep track of 'subnet'??, 'ram', 'instances'. The main problem
        is getting limits.

        :return: QuotaSet object
        """
        not_defined = Quota(-1, -1)
        vcpus = self._get_vcpu_quota()
        networks = self._get_network_quota()
        ports = self._get_ports_quota()
        quota_set = QuotaSet(vcpu=vcpus, port=ports, network=networks, subnet=not_defined,
                             ram=not_defined, instances=not_defined)
        return quota_set

    def get_project_name(self):
        """
        TODO
        """
        return 'paluba-aws'

    def get_hardware_usage(self, topology_instance: TopologyInstance) -> HardwareUsage:
        """
        Get hardware usage of a single sandbox.

        :param topology_instance: Topology instance from which the sandbox is created
        :return: HardwareUsage object
        """
        flavors = self.get_flavors_dict()
        used_vcpu, used_ram, used_instances = 0, 0, 0

        for node in topology_instance.get_nodes():
            flavor = flavors[node.flavor]
            used_vcpu += flavor['vcpu']
            used_ram += flavor['ram']
            used_instances += 1

        networks = [network for network in topology_instance.get_networks()]
        used_network = len(networks)
        used_subnet = len(networks)
        used_port = len([link for link in topology_instance.get_links()])

        return HardwareUsage(used_vcpu, used_ram, used_instances, used_network, used_subnet,
                             used_port)

    def get_flavors_dict(self) -> dict:
        """
        Gets flavors defined in OpenStack project with their vcpu and ram usage as dictionary
        Boto3 does not support 'no-paggination' parameter yet.
        Hence, to get all flavors, we need paginator (iterator over pages).
        """
        flavors_pages = self.ec2_client.get_paginator('describe_instance_types')\
            .paginate(InstanceTypes=[],
                      Filters=[{
                          'Name': 'instance-type',
                          'Values': ['t*'],
                          }])
        return {flavor['InstanceType']: {'vcpu': flavor['VCpuInfo']['DefaultCores'],
                                         'ram': flavor['MemoryInfo']['SizeInMiB']}
                for flavor_list in flavors_pages for flavor in flavor_list['InstanceTypes']}

    def get_project_limits(self) -> Limits:
        """
        Get resources limits of cloud project.
        AWS does not specify limits for all attributes. For such attributes it is suitable
        to specify arbitrary max value as it is used to compute how many sandboxes
        can be build.
        :return: Limits object
        """
        vcpu_limit = self._get_service_quota(
            service_code='ec2',
            quota_code='L-1216C47A'
        )
        ports_limit = self._get_service_quota(
            service_code='vpc',
            quota_code='L-DF5E4CA3',
        )
        vpcs_limit = self._get_service_quota(
            service_code='vpc',
            quota_code='L-F678F1CE',
        )

        return Limits(vcpu=vcpu_limit, ram=999999.0, instances=999999, network=vpcs_limit,
                      subnet=999999, port=ports_limit)
