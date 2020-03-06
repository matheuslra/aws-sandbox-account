from __future__ import print_function
import boto3
import logging
import json
import time
import cfnresponse
import os
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_client(service):
  client = boto3.client(service)
  return client

def get_template(sourcebucket,accountsandboxtemplate):
    

    '''
        Read a template file and return the contents
    '''
    #print("Reading resources from " + templatefile)
    s3 = boto3.resource('s3')
    #obj = s3.Object('cf-to-create-lambda','5-newbaseline.yml')
    obj = s3.Object(sourcebucket,accountsandboxtemplate)
    return obj.get()['Body'].read().decode('utf-8') 

def deploy_resources(template, stackname, stackregion, accountid, executionrole, administrationrole, accountemail, accountdays, increaseec2):

    '''
        Create a CloudFormation stack of resources within the new account
    '''

    datestamp = time.strftime("%d/%m/%Y")
    client = boto3.client('cloudformation',region_name=stackregion)
    #print("Creating stack " + stackname + " in " + account_id)


    create_stack_response = client.create_stack_set(
                StackSetName=stackname,
                TemplateBody=template,
                Parameters=[
                    {
                        'ParameterKey' : 'DaysForAccount',
                        'ParameterValue' : accountdays
                    },
                    {
                        'ParameterKey' : 'AddrEmail',
                        'ParameterValue' : accountemail
                    },
                    {
                        'ParameterKey' : 'AccountIdSandbox',
                        'ParameterValue' : accountid
                    },
                    {
                        'ParameterKey' : 'IncreaseLimitEC2',
                        'ParameterValue' : increaseec2
                    }
                ],
                Capabilities=[
                    'CAPABILITY_NAMED_IAM',
                ],

                Tags=[
                    {
                        'Key': 'ManagedResource',
                        'Value': 'True'
                    },
                    {
                        'Key': 'DeployDate',
                        'Value': datestamp
                    }
                ],
                AdministrationRoleARN=administrationrole,
                ExecutionRoleName=executionrole
            )
            
    response = client.create_stack_instances(
                StackSetName=stackname,
                Accounts=[accountid],
                Regions=[stackregion]
                )


def main(event, context):
            response_data = {}
            try:
                if event["RequestType"] == "Create" or event["RequestType"] == "Update":
                    print(event)
                    client = get_client('organizations')
                    accountid = os.environ['accountid']
                    accountdays = os.environ['accountdays']
                    accountemail = os.environ['accountemail']
                    #accountrole = os.environ['accountrole']
                    #templatefile = os.environ['templatefile']
                    stackname = os.environ['stackname']
                    stackregion = os.environ['stackregion']
                    administrationrole = os.environ['administrationrole']
                    executionrole = os.environ['executionrole']
                    sourcebucket = os.environ['sourcebucket']
                    accountsandboxtemplate = os.environ['accountsandboxtemplate']
                    increaseec2 = os.environ['increaseec2']

                    template = get_template(sourcebucket,accountsandboxtemplate)
                    stack = deploy_resources(template, stackname, stackregion, accountid, executionrole, administrationrole, accountemail, accountdays, increaseec2)
                    print(stack)

                    logger.info("Response - " + json.dumps(response_data))
                    cfnresponse.send(event, context, cfnresponse.SUCCESS, response_data)

                elif event["RequestType"] == "Delete":
                    logger.info("Event Body - " + json.dumps(event))
                    cfnresponse.send(event, context, cfnresponse.SUCCESS,{})
                else:
                  logger.info("Event Body - " + json.dumps(event))
                  cfnresponse.send(event, context, cfnresponse.FAILED,{})
            except Exception as e:
                  logger.error(e, exc_info=True)
                  response_data = {'Error': str(e)}
                  cfnresponse.send(event, context, cfnresponse.FAILED, response_data)