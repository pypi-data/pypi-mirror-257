from typing import Dict, List
from kypo.cloud_commons import TopologyInstance, SecurityGroups
from kypo.topology_definition.models import Protocol
from kypo_aws_commons.security_groups.construct import SecurityGroupsConstruct

from constructs import Construct
from cdktf import App, TerraformStack

from cdktf_cdktf_provider_aws.provider import AwsProvider
from cdktf_cdktf_provider_aws.vpc import Vpc
from cdktf_cdktf_provider_aws.data_aws_vpc import DataAwsVpc
from cdktf_cdktf_provider_aws.subnet import Subnet
from cdktf_cdktf_provider_aws.data_aws_subnet import DataAwsSubnet
from cdktf_cdktf_provider_aws.instance import Instance, InstanceNetworkInterface
from cdktf_cdktf_provider_aws.network_interface import NetworkInterface
from cdktf_cdktf_provider_aws.data_aws_security_group import DataAwsSecurityGroup


CDKTF_OUTPU_DIR = '/tmp'
CDKTF_STACK_NAME = 'sandbox'
CDKTF_TEMPLATE_FILE_NAME = 'cdk.tf.json'
CDKTF_OUTPUT_FILE = f'{CDKTF_OUTPU_DIR}/stacks/{CDKTF_STACK_NAME}/{CDKTF_TEMPLATE_FILE_NAME}'


class AwsNetwork:

    def __init__(self, stack: TerraformStack, topology_instance: TopologyInstance,
                 availability_zone: str, resource_prefix: str):
        _name = f'{resource_prefix}-'
        network_name = _name + 'network-{}'
        self.networks = {net.name:
                         Vpc(stack, network_name.format(net.name), cidr_block=net.cidr,
                             tags={'Name': network_name.format(net.name)})
                         for net in topology_instance.get_networks()}

        base_net = DataAwsVpc(stack, 'base-net', tags={'Name': 'Base Net'})

        self.security_groups = {SecurityGroups.SANDBOX_ACCESS.value:
                                DataAwsSecurityGroup(stack, 'data-sg', vpc_id=base_net.id,
                                                     name='kypo-sandbox-access-sg')}

        for net_name, vpc in self.networks.items():
            sec_group_cons = SecurityGroupsConstruct.from_file(stack, net_name, vpc.id,
                                                               'kypo/aws_driver/config/security_groups.yaml')
            self.security_groups[net_name] = sec_group_cons.aws_groups_dict

        subnet_name = _name + 'subnet-{}'
        self.subnets = {net_name:
                        Subnet(stack, subnet_name.format(net_name), vpc_id=vpc.id,
                               cidr_block=vpc.cidr_block,
                               map_public_ip_on_launch=False,
                               availability_zone=availability_zone,
                               tags={'Name': subnet_name.format(net_name)})
                        for net_name, vpc in self.networks.items()}


class AwsInstance:
    """
    TODO: create link from MAN to Base-Net
    """

    def __init__(self, stack: TerraformStack, topology_instance: TopologyInstance,
                 aws_networks: AwsNetwork, key_pair_name_ssh, key_pair_name_cert,
                 resource_prefix: str):
        _name = f'{resource_prefix}-'
        instance_name = _name + 'instance-{}'
        interface_name = _name + 'int-{}'
        self.instances: Dict[str, Instance] = {}
        base_sb = DataAwsSubnet(stack, 'base-sb',
                                tags={'Name': 'Base Subnet'})  # TODO: read name of subnet from TRC
        interfaces: Dict[str, List[NetworkInterface]] = {
            'man': [NetworkInterface(stack, interface_name.format('base'),
                                     subnet_id=base_sb.id,
                                     security_groups=[aws_networks.security_groups[SecurityGroups.SANDBOX_ACCESS.value].id])]
        }

        for link in topology_instance.get_links():
            sec_group = aws_networks.security_groups[link.network.name][link.security_group]
            interface = NetworkInterface(stack, interface_name.format(link.name),
                                         subnet_id=aws_networks.subnets[link.network.name].id,
                                         security_groups=[sec_group.id])
            if interfaces.get(link.node.name):
                interfaces[link.node.name].append(interface)
            else:
                interfaces[link.node.name] = [interface]

        for node in topology_instance.get_nodes():
            instance_ints = [InstanceNetworkInterface(device_index=i,
                                                      network_interface_id=int.id)
                             for i, int in enumerate(interfaces[node.name])]
            key_pair = key_pair_name_ssh if node.base_box.mgmt_protocol == Protocol.SSH \
                else key_pair_name_cert
            self.instances[link.node.name] = Instance(stack, instance_name.format(node.name),
                                                      ami=node.base_box.image,
                                                      instance_type=node.flavor,
                                                      key_name=key_pair,
                                                      network_interface=instance_ints,
                                                      tags={'Name': instance_name.format(node.name)})


class AwsStack(TerraformStack):  # Possibly create a cdktf interface (or abstract class)

    def __init__(self, scope: Construct, id: str, topology_instance: TopologyInstance,
                 region: str, access_key: str, secret_key: str, availability_zone: str,
                 key_pair_name_ssh, key_pair_name_cert, resource_prefix: str):
        super().__init__(scope, id)
        AwsProvider(self, 'aws', region=region, access_key=access_key,
                    secret_key=secret_key)

        aws_networks = AwsNetwork(self, topology_instance, availability_zone, resource_prefix)
        AwsInstance(self, topology_instance, aws_networks, key_pair_name_ssh,
                    key_pair_name_cert, resource_prefix)


def read_template():
    with open(CDKTF_OUTPUT_FILE) as file:
        return file.read()


def cdktf_create_template(topology_instance: TopologyInstance, region: str, access_key: str,
                          secret_key: str, availability_zone: str,
                          key_pair_name_ssh: str = 'kypo-dummy-ssh-key-pair',
                          key_pair_name_cert: str = 'kypo-dummy-cert-key-pair',
                          resource_prefix: str = 'stack-name'):
    app = App(outdir=CDKTF_OUTPU_DIR)  # do not forget to set skip check and validation
    AwsStack(app, CDKTF_STACK_NAME, topology_instance, region, access_key, secret_key,
             availability_zone, key_pair_name_ssh, key_pair_name_cert, resource_prefix)
    app.synth()
    return read_template()
