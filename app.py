#!/usr/bin/env python3
import os
import pathlib


from aws_cdk import (
    aws_ec2,
    aws_iam,
    aws_s3,
    aws_s3_assets,
    core as cdk
)


class EC2InstanceStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # Networking
        #  - use main VPC managed by terraform
        #  - allow only outbound traffic
        vpc = aws_ec2.Vpc.from_lookup(
            self,
            'MainVPC',
            tags={'Name': 'main-vpc', 'Stack': 'networking'},
        )
        security_group = aws_ec2.SecurityGroup.from_security_group_id(
            self,
            'OutBoundOnlySG',
            'sg-0e4269cd9c7c1765a',
        )
        # Role
        #   - SSM for interactive sessions (AmazonSSMManagedInstanceCore)
        #   - ro on all S3 buckets (AmazonS3ReadOnlyAccess)
        #   - grant rw on research data dev bucket for specific prefix
        role = aws_iam.Role(
            self,
            'InstanceRole',
            role_name='WorkInstanceRole',
            assumed_by=aws_iam.ServicePrincipal('ec2.amazonaws.com'),
            managed_policies=[
                aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSSMManagedInstanceCore'),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3ReadOnlyAccess'),
            ]
        )

        umccr_temp_dev_bucket = aws_s3.Bucket.from_bucket_name(
            self,
            'UmccrTempDevBucket',
            bucket_name='umccr-research-dev',
        )
        umccr_temp_dev_bucket.grant_read_write(
            role,
            objects_key_pattern='stephen/gpl_output/*'
        )

        # Instance
        #  - machine image
        #  - attached block device
        #  - instance itself
        machine_image = aws_ec2.MachineImage.latest_amazon_linux(
            cpu_type=aws_ec2.AmazonLinuxCpuType.X86_64,
            edition=aws_ec2.AmazonLinuxEdition.STANDARD,
            generation=aws_ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            storage=aws_ec2.AmazonLinuxStorage.GENERAL_PURPOSE,
            virtualization=aws_ec2.AmazonLinuxVirt.HVM,
        )
        block_devices = [
            aws_ec2.BlockDevice(
                device_name='/dev/sdb',
                volume=aws_ec2.BlockDeviceVolume.ebs(
                    1024,
                    encrypted=True,
                    delete_on_termination=True,
                    volume_type=aws_ec2.EbsDeviceVolumeType.GP2,
                )
            ),
        ]
        instance = aws_ec2.Instance(
            self,
            'WorkInstance',
            # 4 vCPUS; 30GB memory
            instance_type=aws_ec2.InstanceType('r5a.xlarge'),
            # 2 vCPUS; 8GB memory
            #instance_type=aws_ec2.InstanceType('m5a.large'),
            # 4 vCPUS; 16GB memory
            #instance_type=aws_ec2.InstanceType('m5a.xlarge'),
            machine_image=machine_image,
            vpc=vpc,
            block_devices=block_devices,
            role=role,
            security_group=security_group,
            vpc_subnets=aws_ec2.SubnetSelection(
                subnet_type=aws_ec2.SubnetType.PUBLIC
            )
        )
        # Instance config script
        #   - create Asset and attach to Instance object
        #   - set Instance to execute the configure script
        asset = aws_s3_assets.Asset(
            self,
            'ConfigScriptAsset',
            path=str(pathlib.Path(__file__).parent / 'configure.sh'),
        )
        local_path = instance.user_data.add_s3_download_command(
            bucket=asset.bucket,
            bucket_key=asset.s3_object_key,
        )
        instance.user_data.add_execute_file_command(
            file_path=local_path,
        )
        asset.grant_read(instance.role)


app = cdk.App()
stack = EC2InstanceStack(
    app,
    'swatts-work-ec2-instance',
    env=cdk.Environment(
        account=os.getenv('CDK_DEFAULT_ACCOUNT'),
        region=os.getenv('CDK_DEFAULT_REGION')
    ),
)
cdk.Tags.of(stack).add('Creator', 'cdk')
cdk.Tags.of(stack).add('Owner', 'swatts')
app.synth()
