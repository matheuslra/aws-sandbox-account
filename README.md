# Sandbox Account - Serverless solution for ephemeral resources

Em [Português](README_pt_BR.md)

This is a project for enable aws accounts to sandbox

# Architecture

This project includes the AWS CloudFormation scripts to create, configure, build and deploy a Service Catalog product.

From this product you can deploy this architecture:
![architecture](images/Architecture.png)


## Quick links

1. [Installation](#Installation)
2. [Using the Solution](#Using-the-container)
3. [Troubleshoot](#Troubleshoot)
4. [Cleanup](#Cleanup)

## Installation

You can have your microservice deployed and running in three automatic steps:
Note: Total time for this setup is around 2-3 minutes. 
Cost of this solution is around US$ 5.60 per account/month (us-east-1 / North Virginia). **You need a region where service CodeBuild is running**

### Deploy The Solution
  
|Deploy | Region |
|:---:|:---:|
|[![launch stack](/images/launch_stack_button.png)][us-east-1-account-sandbox] | US East (N. Virginia)|
|[![launch stack](/images/launch_stack_button.png)][sa-east-1-account-sandbox] | SA East (São Paulo)|


[us-east-1-account-sandbox]: https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=CreateSC-Sandbox&templateURL=https://masterbuilder-account-sandbox.s3.amazonaws.com/sandbox-service-catalog.yaml
[sa-east-1-account-sandbox]: https://console.aws.amazon.com/cloudformation/home?region=sa-east-1#/stacks/new?stackName=CreateSC-Sandbox&templateURL=https://masterbuilder-account-sandbox.s3.amazonaws.com/sandbox-service-catalog.yaml
