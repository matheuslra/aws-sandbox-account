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
            accountid = os.environ['accountid']
            logger.info('Always printing the event: {}'.format(event))
            if event["RequestType"] == "Create" or event["RequestType"] == "Update":
              try:
                  logger.info("Event Body - " + json.dumps(event))
                  
                  policies = client.list_policies(
                      Filter='SERVICE_CONTROL_POLICY'
                    )
                  
                  policy_deploy_name = 'ProtectSandboxDeploy'

                  deploypolicyname = [name['Name'] for name in policies['Policies']]
                  deploypolicyid = [id['Id'] for id in policies['Policies']]
                  
                  if  policy_deploy_name in deploypolicyname:
                    print("Policy already exists")
                    for i, (name, id) in enumerate(zip(deploypolicyname, deploypolicyid)):
                      if policy_deploy_name in name:
                      
                        attach = client.attach_policy(
                            PolicyId=id,
                            TargetId=accountid
                            )
                        print("Policy apply in account")
                  else:  
                    policy_deploy_resources = client.create_policy(
                      Content='{"Version":"2012-10-17","Statement":[{"Sid":"ProtectStepFunction","Effect":"Deny","Action":["states:*"],"Resource":["arn:aws:states:*:*:stateMachine:StepFunctionMonitoring"],"Condition":{"ArnNotLike":{"aws:PrincipalARN":["arn:aws:iam::*:role/RoleForStepFunctionSandboxAccount","arn:aws:iam::*:role/RoleForLambdaAccessResources","arn:aws:iam::*:role/AWSControlTowerExecution"]}}},{"Sid":"ProtectCodeBuild","Effect":"Deny","Action":["codebuild:*"],"Resource":["arn:aws:codebuild:*:*:project/AccountNuker-List","arn:aws:codebuild:*:*:project/AccountNuker-Delete"],"Condition":{"ArnNotLike":{"aws:PrincipalARN":["arn:aws:iam::*:role/RoleForCodeBuildSandbox","arn:aws:iam::*:role/RoleForLambdaAccessResources","arn:aws:iam::*:role/AWSControlTowerExecution"]}}},{"Sid":"ProtectSSMParameterStore","Effect":"Deny","Action":["ssm:*"],"Resource":["arn:aws:ssm:*:*:parameter/account_days","arn:aws:ssm:*:*:parameter/account_id","arn:aws:ssm:*:*:parameter/account_initial","arn:aws:ssm:*:*:parameter/ec2_limit"],"Condition":{"ArnNotLike":{"aws:PrincipalARN":["arn:aws:iam::*:role/RoleForLambdaAccessResources","arn:aws:iam::*:role/RoleForCodeBuildSandbox","arn:aws:iam::*:role/RoleForStepFunctionSandboxAccount","arn:aws:iam::*:role/AWSControlTowerExecution"]}}},{"Sid":"ProtectLambda","Effect":"Deny","Action":["lambda:*"],"Resource":["arn:aws:lambda:*:*:function:MonitoringFuction","arn:aws:lambda:*:*:function:DeleteAccount","arn:aws:lambda:*:*:function:MissingDaysFunction","arn:aws:lambda:*:*:function:ListResources","arn:aws:lambda:*:*:function:ExecuteCWE"],"Condition":{"ArnNotLike":{"aws:PrincipalARN":["arn:aws:iam::*:role/RoleForLambdaAccessResources","arn:aws:iam::*:role/RoleForCodeBuildSandbox","arn:aws:iam::*:role/RoleForStepFunctionSandboxAccount","arn:aws:iam::*:role/AWSControlTowerExecution"]}}},{"Sid":"ProtectIAMRoles","Effect":"Deny","Action":["iam:*"],"Resource":["arn:aws:iam::*:role/RoleForLambdaAccessResources","arn:aws:iam::*:role/RoleForCodeBuildSandbox","arn:aws:iam::*:role/RoleForStepFunctionSandboxAccount","arn:aws:iam::*:role/RoleForCloudWatchLambda"],"Condition":{"ArnNotLike":{"aws:PrincipalARN":["arn:aws:lambda:*:*:function:MonitoringFuction","arn:aws:lambda:*:*:function:DeleteAccount","arn:aws:lambda:*:*:function:MissingDaysFunction","arn:aws:lambda:*:*:function:ListResources","arn:aws:lambda:*:*:function:ExecuteCWE","arn:aws:codebuild:*:*:project/AccountNuker-List","arn:aws:codebuild:*:*:project/AccountNuker-Delete","arn:aws:states:*:*:stateMachine:StepFunctionMonitoring","arn:aws:iam::*:role/AWSControlTowerExecution","arn:aws:sns:*:*:Sandbox-SNSTopic","arn:aws:ssm:*:*:parameter/account_days","arn:aws:ssm:*:*:parameter/account_id","arn:aws:ssm:*:*:parameter/account_initial","arn:aws:ssm:*:*:parameter/ec2_limit","arn:aws:servicequotas:*::ec2/L-1216C47A"]}}},{"Sid":"ProtectCloudWatchEventRule","Effect":"Deny","Action":["events:*"],"Resource":["arn:aws:events:*:*:rule/Sandbox-MonitoringEventRule"],"Condition":{"ArnNotLike":{"aws:PrincipalARN":["arn:aws:lambda:*:*:function:ExecuteCWE","arn:aws:iam::*:role/AWSControlTowerExecution"]}}}]}',
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
               