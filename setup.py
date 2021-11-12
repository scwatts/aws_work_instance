import setuptools


setuptools.setup(
    name="aws_work_instance",
    version="0.0.1",
    description="Simple EC2 instance stack",
    install_requires=[
        "aws-cdk.core==1.110.1",
        "aws-cdk.aws-ec2",
    ],
    python_requires=">=3.6",
)
