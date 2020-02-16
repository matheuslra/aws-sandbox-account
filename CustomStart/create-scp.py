import boto3, json
import cfnresponse
import os
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
def lambda_handler(event, context):
            responseData = {}
            logger.info('event: {}'.format(event))
            logger.info('context: {}'.format(context))
            client = boto3.client('organizations')

            logger.info('Always printing the event: {}'.format(event))
            if event["RequestType"] == "Create" or event["RequestType"] == "Update":
              try:
                  logger.info("Event Body - " + json.dumps(event))
                  accountid = os.environ['accountid']
                  policies = client.list_policies(
                      Filter='SERVICE_CONTROL_POLICY'
                    )
                  policy_deny_name = 'DenyAllOutsideUSandBR'
                  policy_deploy_name = 'ProtectSandboxDeploy'

                  denypolicyname = [name['Name'] for name in policies['Policies']]
                  denypolicyid = [id['Id'] for id in policies['Policies']]

                  deploypolicyname = [name['Name'] for name in policies['Policies']]
                  deploypolicyid = [id['Id'] for id in policies['Policies']]

                  if policy_deny_name in denypolicyname:
                    print ("Policy already exists")
                    for i, (name, id) in enumerate(zip(denypolicyname, denypolicyid)):
                      if policy_deny_name in name:
                      
                        attach = client.attach_policy(
                            PolicyId=id,
                            TargetId=accountid
                            )
                        print("Policy apply in account")
                  else:
                    policy_deny_resources = client.create_policy(
                      Content='{"Version": "2012-10-17","Statement": [{"Sid": "DenyAllOutsideUSandBR","Effect": "Deny","NotAction": ["iam:*","organizations:*","route53:*","budgets:*","waf:*","cloudfront:*","globalaccelerator:*","importexport:*","support:*"],"Resource": "*","Condition": {"StringNotEquals": {"aws:RequestedRegion": ["us-east-1","sa-east-1"]}}}]}',
                      Description='Denny all services outsite N.Virginia and South America',
                      Name='DenyAllOutsideUSandBR',
                      Type='SERVICE_CONTROL_POLICY'
                      )

                    policy_id_deny_resources = policy_deny_resources['Policy']['PolicySummary']['Id']

                    attach_deny_resources = client.attach_policy(
                      PolicyId=policy_id_deny_resources,
                      TargetId=accountid
                      )
                  
                  if  polpolicy_deploy_nameicy_name in denypolicyname:
                    print("Policy already exists")
                    for i, (name, id) in enumerate(zip(denypolicyname, denypolicyid)):
                      if policy_deploy_name in name:
                      
                        attach = client.attach_policy(
                            PolicyId=id,
                            TargetId=accountid
                            )
                        print("Policy apply in account")
                  else:  
                    policy_deploy_resources = client.create_policy(
                      Content='{"Version":"2012-10-17","Statement":[{"Sid":"ProtectStepFunction","Effect":"Deny","Action":["states:*"],"Resource":["arn:aws:states:*:*:stateMachine:StepFunctionMonitoring"],"Condition":{"ArnNotLike":{"aws:PrincipalARN":["arn:aws:iam::*:role/RoleForStepFunctionSandboxAccount","arn:aws:iam::*:role/RoleForLambdaFullAccess"]}}},{"Sid":"ProtectCodeBuild","Effect":"Deny","Action":["codebuild:*"],"Resource":["arn:aws:codebuild:*:*:project/AccountNuker-List","arn:aws:codebuild:*:*:project/AccountNuker-Delete"],"Condition":{"ArnNotLike":{"aws:PrincipalARN":["arn:aws:iam::*:role/RoleForCodeBuildSandbox","arn:aws:iam::*:role/RoleForLambdaFullAccess"]}}},{"Sid":"ProtectSSMParameterStore","Effect":"Deny","Action":["ssm:*"],"Resource":["arn:aws:ssm:*:*:parameter/account_days","arn:aws:ssm:*:*:parameter/account_id"],"Condition":{"ArnNotLike":{"aws:PrincipalARN":["arn:aws:iam::*:role/RoleForLambdaFullAccess","arn:aws:iam::*:role/RoleForCodeBuildSandbox","arn:aws:iam::*:role/RoleForStepFunctionSandboxAccount"]}}}]}',
                      Description='Protect all services deployed by StackSet Account Sandbox',
                      Name='ProtectSandboxDeploy',
                      Type='SERVICE_CONTROL_POLICY'
                      )

                    policy_id_deploy_resources = policy_deploy_resources['Policy']['PolicySummary']['Id']

                    attach_deploy_resources = client.attach_policy(
                      PolicyId=policy_id_deploy_resources,
                      TargetId=accountid
                      )
                    print ("Policy apply sucessfully in account")

                  cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData, 'CustomResourcePhysicalID')
              except Exception as e:
                    logger.error(e, exc_info=True)
                    responseData = {'Error': str(e)}
                    cfnresponse.send(event, context, cfnresponse.FAILED, responseData, 'CustomResourcePhysicalID')
                    
            if event["RequestType"] == "Delete":
                    logger.info("Event Body - " + json.dumps(event))
                    cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData, 'CustomResourcePhysicalID')
               