import setuptools


setuptools.setup(
    name="cdk_ec2",
    version="0.0.1",

    description="Simple EC2 instance stack",

    author="author",

    install_requires=[
        "aws-cdk.core==1.110.1",
        "aws-cdk.aws-ec2",
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
