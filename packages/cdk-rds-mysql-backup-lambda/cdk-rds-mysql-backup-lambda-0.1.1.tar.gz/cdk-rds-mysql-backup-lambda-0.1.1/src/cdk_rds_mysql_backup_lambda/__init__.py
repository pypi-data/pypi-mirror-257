'''
# RDSMySQLBackupLambda

![GitHub](https://img.shields.io/github/license/ilkrklc/cdk-rds-mysql-backup-lambda) ![npm version](https://img.shields.io/npm/v/cdk-rds-mysql-backup-lambda) [![Maven Central](https://maven-badges.herokuapp.com/maven-central/io.github.ilkrklc/cdk.rds.mysql.backup.lambda/badge.svg)](https://maven-badges.herokuapp.com/maven-central/io.github.ilkrklc/cdk.rds.mysql.backup.lambda) [![NuGet latest version](https://badgen.net/nuget/v/CDK.RDS.MySQL.Backup.Lambda/latest)](https://nuget.org/packages/CDK.RDS.MySQL.Backup.Lambda) [![PyPi version](https://badgen.net/pypi/v/cdk-rds-mysql-backup-lambda/)](https://pypi.org/project/cdk-rds-mysql-backup-lambda) [![Go Reference](https://pkg.go.dev/badge/github.com/ilkrklc/cdk-rds-mysql-backup-lambda/cdkrdsmysqlbackuplambda.svg)](https://pkg.go.dev/github.com/ilkrklc/cdk-rds-mysql-backup-lambda/cdkrdsmysqlbackuplambda)

The `RDSMySQLBackupLambda` is an AWS CDK Construct that provides an automated solution for backing up RDS MySQL databases to an S3 bucket using a Lambda function. It is designed for developers who need a flexible and cost-effective method to back up their RDS MySQL databases outside of the default RDS backup capabilities.

## Table of Contents

* [Features](#features)
* [How It Works](#how-it-works)
* [Installation](#installation)
* [Usage](#usage)
* [Documentation](#documentation)
* [Contributing](#contributing)
* [Pull Request Guidelines](#pull-request-guidelines)
* [License](#license)

## Features

* Automated backups of RDS MySQL databases.
* Backup scheduling using a cron expression.
* Backups stored securely in an S3 bucket with encryption.
* Customizable Lambda function name, timeout, and S3 bucket name.
* Built-in VPC and security group configurations for secure access to RDS instances.

## How It Works

The RDSMySQLBackupLambda AWS CDK Construct automates the process of backing up RDS MySQL databases to S3, leveraging AWS Lambda and other AWS services. Here’s an overview of its operation:

### Architecture and Flow:

**1. Lambda Function:**

* A Lambda function is the core component that performs the database backup. It's triggered based on the specified schedule (defaulting to daily at 00:00 UTC).
* The function connects to the specified RDS MySQL database instance using the provided credentials and performs a mysqldump.

**2. VPC and Subnet Configuration:**

* The Lambda function is deployed within the same VPC and subnet group as the RDS instance. This ensures a secure and direct connection to the RDS instance, as typically, RDS instances are placed in private subnets without direct internet access.

**3. Security Group Settings:**

* The security group of the Lambda function is configured to allow outbound connections to the RDS instance on the specified port (default 3306 for MySQL).
* The RDS instance's security group is updated to allow inbound connections from the Lambda function's security group.

**4. S3 Bucket for Backup Storage:**

* An S3 bucket is created and configured with server-side encryption (SSE-S3) for secure storage of the backup files.

**5. S3 VPC Endpoint:**

* To address scenarios where the RDS instance and Lambda function reside in a subnet without internet access, the construct utilizes an S3 VPC endpoint.
* This endpoint provides private connectivity to S3, allowing the Lambda function to upload backup files to the S3 bucket without needing internet access.

**6. Backup Process:**

* When triggered, the Lambda function initiates a backup of the specified database, generating a dump file.
* The dump file is then securely uploaded to the S3 bucket via the S3 VPC endpoint.

## Installation

To install `RDSMySQLBackupLambda` construct library using npm, run the following command:

```bash
npm i cdk-rds-mysql-backup-lambda
```

## Usage

To initialize the `RDSMySQLBackupLambda` construct you can use the following code:

```python
import * as cdk from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as events from 'aws-cdk-lib/aws-events';
import { Construct } from 'constructs';
import { RDSMySQLBackupLambda } from 'cdk-rds-mysql-backup-lambda';

export class TestStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: TestStackProps) {
    super(scope, id, props);

    // Get VPC and Subnets where the RDS instance is located
    const vpc = ec2.Vpc.fromVpcAttributes(this, 'TestVpc', {
      vpcId: props.vpcId,
      availabilityZones: ['eu-central-1a', 'eu-central-1b', 'eu-central-1c'],
      publicSubnetIds: props.vpcSubnetIds,
    });
    const vpcSubnets = vpc.selectSubnets({
      subnetType: ec2.SubnetType.PUBLIC,
    });

    const mysqlBackup = new RDSMySQLBackupLambda(this, 'RDSMySQLBackupLambda', {
      rdsVpc: vpc,
      rdsVpcSubnets: vpcSubnets,
      rdsInstanceName: 'rdsInstanceName',
      rdsInstancePort: 3306, // optional
      rdsInstanceEndpointAddress: 'rdsInstanceEndpointAddress',
      rdsSecurityGroupId: 'rdsSecurityGroupId',
      dbName: 'db_name',
      dbUser: 'user',
      dbPassword: 'pass',
      lambdaFunctionName: 'RDSMySQLBackupLambdaFunction', // optional
      lambdaFunctionTimeout: cdk.Duration.minutes(15), // optional
      s3BucketName: 'rds-mysql-backups', // optional
      backupSchedule: events.Schedule.cron({ hour: '0', minute: '0' }), // optional
    });

    // exported properties
    console.log(mysqlBackup.s3Bucket); // S3 bucket where the backups are stored
    console.log(mysqlBackup.lambdaFunction); // Lambda function that backs up the RDS MySQL database
  }
}
```

## Documentation

To initialize the `RDSMySQLBackupLambda` construct you can use the following props:

```python
/**
 * Properties for the RDSMySQLBackupLambda construct.
 */
export interface RDSMySQLBackupLambdaProps extends ResourceProps {
  /**
   * VPC used by the RDS instance.
   */
  readonly rdsVpc: ec2.IVpc;

  /**
   * VPC subnet group used by the RDS instance.
   */
  readonly rdsVpcSubnets: ec2.SelectedSubnets;

  /**
   * Name of RDS instance to backup.
   */
  readonly rdsInstanceName: string;

  /**
   * Endpoint address of the RDS instance.
   */
  readonly rdsInstanceEndpointAddress: string;

  /**
   * Port of the RDS instance.
   */
  readonly rdsInstancePort?: number;

  /**
   * Security group ID for the RDS instance.
   */
  readonly rdsSecurityGroupId: string;

  /**
   * User to connect to the RDS instance.
   */
  readonly dbUser: string;

  /**
   * Password to connect to the RDS instance.
   */
  readonly dbPassword: string;

  /**
   * Name of the database to backup.
   */
  readonly dbName: string;

  /**
   * Name of the lambda function that will be created.
   *
   * @default - [db-instance-identifier]-rds-backup-lambda
   */
  readonly lambdaFunctionName?: string;

  /**
   * Timeout value for the backup lambda function.
   *
   * @default - 5 minutes
   */
  readonly lambdaTimeout?: Duration;

  /**
   * Name of the S3 bucket to store the RDS backups.
   *
   * @default - [db-instance-identifier]-rds-backup
   */
  readonly s3BucketName?: string;

  /**
   * Schedule for the lambda function to run.
   *
   * @default - Every day at 00:00 UTC
   */
  readonly scheduleRule?: events.Schedule;
}
```

## Contributing

We welcome contributions! Please review [code of conduct](.github/CODE_OF_CONDUCT.md) and [contributing guide](.github/CONTRIBUTING.md) so that you can understand what actions will and will not be tolerated.

### Pull Request Guidelines

* The `main` branch is just a snapshot of the latest stable release. All development should be done in development branches. **Do not submit PRs against the `main` branch.**
* Work in the `src` folder and **DO NOT** checkin `dist` in the commits.
* It's OK to have multiple small commits as you work on the PR
* If adding a new feature add accompanying test case.
* If fixing bug,

  * Add accompanying test case if applicable.
  * Provide a detailed description of the bug in the PR.
  * If you are resolving an opened issue add issue number in your PR title.

## License

`RDSMySQLBackupLambda` is [MIT licensed](./LICENSE).
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_events as _aws_cdk_aws_events_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import constructs as _constructs_77d1e7e8


class RDSMySQLBackupLambda(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-rds-mysql-backup-lambda.RDSMySQLBackupLambda",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        db_name: builtins.str,
        db_password: builtins.str,
        db_user: builtins.str,
        rds_instance_endpoint_address: builtins.str,
        rds_instance_name: builtins.str,
        rds_security_group_id: builtins.str,
        rds_vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        rds_vpc_subnets: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SelectedSubnets, typing.Dict[builtins.str, typing.Any]],
        lambda_function_name: typing.Optional[builtins.str] = None,
        lambda_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        rds_instance_port: typing.Optional[jsii.Number] = None,
        s3_bucket_name: typing.Optional[builtins.str] = None,
        schedule_rule: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param db_name: (experimental) Name of the database to backup.
        :param db_password: (experimental) Password to connect to the RDS instance.
        :param db_user: (experimental) User to connect to the RDS instance.
        :param rds_instance_endpoint_address: (experimental) Endpoint address of the RDS instance.
        :param rds_instance_name: (experimental) Name of RDS instance to backup.
        :param rds_security_group_id: (experimental) Security group ID for the RDS instance.
        :param rds_vpc: (experimental) VPC used by the RDS instance.
        :param rds_vpc_subnets: (experimental) VPC subnet group used by the RDS instance.
        :param lambda_function_name: (experimental) Name of the lambda function that will be created. Default: - [db-instance-identifier]-rds-backup-lambda
        :param lambda_timeout: (experimental) Timeout value for the backup lambda function. Default: - 5 minutes
        :param rds_instance_port: (experimental) Port of the RDS instance.
        :param s3_bucket_name: (experimental) Name of the S3 bucket to store the RDS backups. Default: - [db-instance-identifier]-rds-backup
        :param schedule_rule: (experimental) Schedule for the lambda function to run. Default: - Every day at 00:00 UTC
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3e1741df07d5be7fee408eca17a31e1a8cd8bfc86eac580c06a2499f4bdfe44)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RDSMySQLBackupLambdaProps(
            db_name=db_name,
            db_password=db_password,
            db_user=db_user,
            rds_instance_endpoint_address=rds_instance_endpoint_address,
            rds_instance_name=rds_instance_name,
            rds_security_group_id=rds_security_group_id,
            rds_vpc=rds_vpc,
            rds_vpc_subnets=rds_vpc_subnets,
            lambda_function_name=lambda_function_name,
            lambda_timeout=lambda_timeout,
            rds_instance_port=rds_instance_port,
            s3_bucket_name=s3_bucket_name,
            schedule_rule=schedule_rule,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="lambdaFunction")
    def lambda_function(self) -> _aws_cdk_aws_lambda_ceddda9d.Function:
        '''(experimental) The lambda function to backup the RDS instance.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.Function, jsii.get(self, "lambdaFunction"))

    @builtins.property
    @jsii.member(jsii_name="s3Bucket")
    def s3_bucket(self) -> _aws_cdk_aws_s3_ceddda9d.Bucket:
        '''(experimental) The S3 bucket created to store the RDS backups.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.Bucket, jsii.get(self, "s3Bucket"))


@jsii.data_type(
    jsii_type="cdk-rds-mysql-backup-lambda.RDSMySQLBackupLambdaProps",
    jsii_struct_bases=[_aws_cdk_ceddda9d.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "db_name": "dbName",
        "db_password": "dbPassword",
        "db_user": "dbUser",
        "rds_instance_endpoint_address": "rdsInstanceEndpointAddress",
        "rds_instance_name": "rdsInstanceName",
        "rds_security_group_id": "rdsSecurityGroupId",
        "rds_vpc": "rdsVpc",
        "rds_vpc_subnets": "rdsVpcSubnets",
        "lambda_function_name": "lambdaFunctionName",
        "lambda_timeout": "lambdaTimeout",
        "rds_instance_port": "rdsInstancePort",
        "s3_bucket_name": "s3BucketName",
        "schedule_rule": "scheduleRule",
    },
)
class RDSMySQLBackupLambdaProps(_aws_cdk_ceddda9d.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        db_name: builtins.str,
        db_password: builtins.str,
        db_user: builtins.str,
        rds_instance_endpoint_address: builtins.str,
        rds_instance_name: builtins.str,
        rds_security_group_id: builtins.str,
        rds_vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        rds_vpc_subnets: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SelectedSubnets, typing.Dict[builtins.str, typing.Any]],
        lambda_function_name: typing.Optional[builtins.str] = None,
        lambda_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        rds_instance_port: typing.Optional[jsii.Number] = None,
        s3_bucket_name: typing.Optional[builtins.str] = None,
        schedule_rule: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule] = None,
    ) -> None:
        '''(experimental) Properties for the RDSMySQLBackupLambda construct.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param db_name: (experimental) Name of the database to backup.
        :param db_password: (experimental) Password to connect to the RDS instance.
        :param db_user: (experimental) User to connect to the RDS instance.
        :param rds_instance_endpoint_address: (experimental) Endpoint address of the RDS instance.
        :param rds_instance_name: (experimental) Name of RDS instance to backup.
        :param rds_security_group_id: (experimental) Security group ID for the RDS instance.
        :param rds_vpc: (experimental) VPC used by the RDS instance.
        :param rds_vpc_subnets: (experimental) VPC subnet group used by the RDS instance.
        :param lambda_function_name: (experimental) Name of the lambda function that will be created. Default: - [db-instance-identifier]-rds-backup-lambda
        :param lambda_timeout: (experimental) Timeout value for the backup lambda function. Default: - 5 minutes
        :param rds_instance_port: (experimental) Port of the RDS instance.
        :param s3_bucket_name: (experimental) Name of the S3 bucket to store the RDS backups. Default: - [db-instance-identifier]-rds-backup
        :param schedule_rule: (experimental) Schedule for the lambda function to run. Default: - Every day at 00:00 UTC

        :stability: experimental
        '''
        if isinstance(rds_vpc_subnets, dict):
            rds_vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SelectedSubnets(**rds_vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__162b25b325ea1d383cf0949aa726b74ea3ccc50f3ecf4ac4a76a2c5036177cde)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument db_name", value=db_name, expected_type=type_hints["db_name"])
            check_type(argname="argument db_password", value=db_password, expected_type=type_hints["db_password"])
            check_type(argname="argument db_user", value=db_user, expected_type=type_hints["db_user"])
            check_type(argname="argument rds_instance_endpoint_address", value=rds_instance_endpoint_address, expected_type=type_hints["rds_instance_endpoint_address"])
            check_type(argname="argument rds_instance_name", value=rds_instance_name, expected_type=type_hints["rds_instance_name"])
            check_type(argname="argument rds_security_group_id", value=rds_security_group_id, expected_type=type_hints["rds_security_group_id"])
            check_type(argname="argument rds_vpc", value=rds_vpc, expected_type=type_hints["rds_vpc"])
            check_type(argname="argument rds_vpc_subnets", value=rds_vpc_subnets, expected_type=type_hints["rds_vpc_subnets"])
            check_type(argname="argument lambda_function_name", value=lambda_function_name, expected_type=type_hints["lambda_function_name"])
            check_type(argname="argument lambda_timeout", value=lambda_timeout, expected_type=type_hints["lambda_timeout"])
            check_type(argname="argument rds_instance_port", value=rds_instance_port, expected_type=type_hints["rds_instance_port"])
            check_type(argname="argument s3_bucket_name", value=s3_bucket_name, expected_type=type_hints["s3_bucket_name"])
            check_type(argname="argument schedule_rule", value=schedule_rule, expected_type=type_hints["schedule_rule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "db_name": db_name,
            "db_password": db_password,
            "db_user": db_user,
            "rds_instance_endpoint_address": rds_instance_endpoint_address,
            "rds_instance_name": rds_instance_name,
            "rds_security_group_id": rds_security_group_id,
            "rds_vpc": rds_vpc,
            "rds_vpc_subnets": rds_vpc_subnets,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if lambda_function_name is not None:
            self._values["lambda_function_name"] = lambda_function_name
        if lambda_timeout is not None:
            self._values["lambda_timeout"] = lambda_timeout
        if rds_instance_port is not None:
            self._values["rds_instance_port"] = rds_instance_port
        if s3_bucket_name is not None:
            self._values["s3_bucket_name"] = s3_bucket_name
        if schedule_rule is not None:
            self._values["schedule_rule"] = schedule_rule

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_name(self) -> builtins.str:
        '''(experimental) Name of the database to backup.

        :stability: experimental
        '''
        result = self._values.get("db_name")
        assert result is not None, "Required property 'db_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def db_password(self) -> builtins.str:
        '''(experimental) Password to connect to the RDS instance.

        :stability: experimental
        '''
        result = self._values.get("db_password")
        assert result is not None, "Required property 'db_password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def db_user(self) -> builtins.str:
        '''(experimental) User to connect to the RDS instance.

        :stability: experimental
        '''
        result = self._values.get("db_user")
        assert result is not None, "Required property 'db_user' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rds_instance_endpoint_address(self) -> builtins.str:
        '''(experimental) Endpoint address of the RDS instance.

        :stability: experimental
        '''
        result = self._values.get("rds_instance_endpoint_address")
        assert result is not None, "Required property 'rds_instance_endpoint_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rds_instance_name(self) -> builtins.str:
        '''(experimental) Name of RDS instance to backup.

        :stability: experimental
        '''
        result = self._values.get("rds_instance_name")
        assert result is not None, "Required property 'rds_instance_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rds_security_group_id(self) -> builtins.str:
        '''(experimental) Security group ID for the RDS instance.

        :stability: experimental
        '''
        result = self._values.get("rds_security_group_id")
        assert result is not None, "Required property 'rds_security_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rds_vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''(experimental) VPC used by the RDS instance.

        :stability: experimental
        '''
        result = self._values.get("rds_vpc")
        assert result is not None, "Required property 'rds_vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def rds_vpc_subnets(self) -> _aws_cdk_aws_ec2_ceddda9d.SelectedSubnets:
        '''(experimental) VPC subnet group used by the RDS instance.

        :stability: experimental
        '''
        result = self._values.get("rds_vpc_subnets")
        assert result is not None, "Required property 'rds_vpc_subnets' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.SelectedSubnets, result)

    @builtins.property
    def lambda_function_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the lambda function that will be created.

        :default: - [db-instance-identifier]-rds-backup-lambda

        :stability: experimental
        '''
        result = self._values.get("lambda_function_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lambda_timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) Timeout value for the backup lambda function.

        :default: - 5 minutes

        :stability: experimental
        '''
        result = self._values.get("lambda_timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def rds_instance_port(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Port of the RDS instance.

        :stability: experimental
        '''
        result = self._values.get("rds_instance_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def s3_bucket_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the S3 bucket to store the RDS backups.

        :default: - [db-instance-identifier]-rds-backup

        :stability: experimental
        '''
        result = self._values.get("s3_bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule_rule(self) -> typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule]:
        '''(experimental) Schedule for the lambda function to run.

        :default: - Every day at 00:00 UTC

        :stability: experimental
        '''
        result = self._values.get("schedule_rule")
        return typing.cast(typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RDSMySQLBackupLambdaProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "RDSMySQLBackupLambda",
    "RDSMySQLBackupLambdaProps",
]

publication.publish()

def _typecheckingstub__a3e1741df07d5be7fee408eca17a31e1a8cd8bfc86eac580c06a2499f4bdfe44(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    db_name: builtins.str,
    db_password: builtins.str,
    db_user: builtins.str,
    rds_instance_endpoint_address: builtins.str,
    rds_instance_name: builtins.str,
    rds_security_group_id: builtins.str,
    rds_vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    rds_vpc_subnets: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SelectedSubnets, typing.Dict[builtins.str, typing.Any]],
    lambda_function_name: typing.Optional[builtins.str] = None,
    lambda_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    rds_instance_port: typing.Optional[jsii.Number] = None,
    s3_bucket_name: typing.Optional[builtins.str] = None,
    schedule_rule: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__162b25b325ea1d383cf0949aa726b74ea3ccc50f3ecf4ac4a76a2c5036177cde(
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    db_name: builtins.str,
    db_password: builtins.str,
    db_user: builtins.str,
    rds_instance_endpoint_address: builtins.str,
    rds_instance_name: builtins.str,
    rds_security_group_id: builtins.str,
    rds_vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    rds_vpc_subnets: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SelectedSubnets, typing.Dict[builtins.str, typing.Any]],
    lambda_function_name: typing.Optional[builtins.str] = None,
    lambda_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    rds_instance_port: typing.Optional[jsii.Number] = None,
    s3_bucket_name: typing.Optional[builtins.str] = None,
    schedule_rule: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule] = None,
) -> None:
    """Type checking stubs"""
    pass
