# Sandbox Account - Serverless solution for ephemeral resources

Em [Português](README_pt_BR.md)

This is a project for enable aws accounts to sandbox creating a lifecycle of resources that will be delete when the countdown reach out the last day.

![state-machine-account](images/account-statemachine-English.png)

# Architecture

This project includes the AWS CloudFormation scripts to create, configure, build and deploy a Service Catalog product.

From this product you can deploy this architecture:
![architecture](images/Architecture.png)


## Quick links

1. [Installation](#Installation)
2. [Using the Solution](#Using-the-solution)
2. [Deploy the Solution](#Deploy-the-solution)
3. [Troubleshoot](#Troubleshoot)
4. [Cleanup](#Cleanup)

## Installation

You can have your sandbox account deployed and running in three automatic steps:
Note: Total time for this setup is around 2-3 minutes. 
Cost of this solution is around US$ 5.60 per account/month (us-east-1 / North Virginia). **You need a region where service CodeBuild is running**

### Deploy the Solution 
  
|Deploy | Region |
|:---:|:---:|
|[![launch stack](/images/launch_stack_button.png)][us-east-1-account-sandbox] | US East (N. Virginia)|
|[![launch stack](/images/launch_stack_button.png)][sa-east-1-account-sandbox] | SA East (São Paulo)|

For fill those parameters to deploy a Service Catalog follow below the description:
|Parameter | Description |
|:---:|:---:|
|ARN IAM Role ServiceCatalogEndUser|This is the ARN of IAM Role provide by ControlTower and belongs to AWS SSO. Use ServiceCatalogEndUser to search in IAM dashboard|
|ARN IAM Role AdministratorAccess|This is the ARN of IAM Role provide by ControlTower and belongs to AWS SSO. Use AdministratorAccess to search in IAM dashboard|

After deploy the solution, a service catalog will be created and from there you can deploy a solution.
The Service Catalog will have a product call "Sandbox Account", you can launch it and fill the parameters required:

|Parameter | Description |
|:---:|:---:|
|Email address | This will be the email address that will receive all the notifications about the lifecycle of this account|
|Budget Name| Budget name for this account that will be available in your organization's master account |
|Budget Amount| Mount in dollars that this account is budgeted for, if it reaches over 90% of the stipulated amount, the email registered in the above parameter will receive an alert notification, as in the image below|
|vCPU EC2| This parameter if you want the already open a ticket to get more vCPU. Generally a new account get only 5 vCPU|
|AWS Account ID| Experimentation Account ID. Note: AWS account has 12 digits, without quotes and without spaces|
|AWS Region| Region where the resources that monitor the account will be deployed, available to N. Virginia and São Paulo|
|Amount days lifecycle| This is the number of days that the account's resources existed before being deleted. This parameter is automatically reduced every day.|

## Using the Solution

## Troubleshoot

## Cleanup

To undo an sandbox account simply log into the Control Tower and / or Organizations / Landing Zone master account and access the CloudFormation service:

1. Access the Service Catalog service using the AWS console from the Control Tower master account and access the newly installed `SandboxAccount` product. Once the product is found, it is necessary to execute the Terminate Product function.
2. Access the Cloudformation service using the AWS console from the Control Tower master account and go to StackSet, click on the stackset that has the name `SandboxStackSet-XXXXXXXXXXXX`, these X being the ID Account of the sandbox account passed as a parameter. until "Actions", then "Delete stacks from StackSet", you will then ask for the number of the AWS Account ID, the region and then click Delete. After making sure that the stack in the sandbox account has been successfully deleted, it will go again in StackSet and delete through the "Actions → Delete StackSet" menu.
3. Access the Organizations service from the master account and enter SCP or Service Control Policies to list the existing policies. In this case, just select the policies `SandboxRegions` and `SandboxGuardrails` and remove the association of these policies with the ephemeral account.


[us-east-1-account-sandbox]: https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=CreateSC-Sandbox&templateURL=https://masterbuilder-account-sandbox.s3.amazonaws.com/sandbox-service-catalog.yaml
[sa-east-1-account-sandbox]: https://console.aws.amazon.com/cloudformation/home?region=sa-east-1#/stacks/new?stackName=CreateSC-Sandbox&templateURL=https://masterbuilder-account-sandbox.s3.amazonaws.com/sandbox-service-catalog.yaml
