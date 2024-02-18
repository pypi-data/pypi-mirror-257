import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-rds-mysql-backup-lambda",
    "version": "0.1.1",
    "description": "A flexible AWS CDK construct for scheduled RDS MySQL backups to S3.",
    "license": "MIT",
    "url": "https://github.com/ilkrklc/cdk-rds-mysql-backup-lambda",
    "long_description_content_type": "text/markdown",
    "author": "Ilker Kilic<ilkrklc@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/ilkrklc/cdk-rds-mysql-backup-lambda"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_rds_mysql_backup_lambda",
        "cdk_rds_mysql_backup_lambda._jsii"
    ],
    "package_data": {
        "cdk_rds_mysql_backup_lambda._jsii": [
            "cdk-rds-mysql-backup-lambda@0.1.1.jsii.tgz"
        ],
        "cdk_rds_mysql_backup_lambda": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib==2.128.0",
        "constructs>=10.3.0, <11.0.0",
        "jsii>=1.94.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
