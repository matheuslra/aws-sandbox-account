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
                  #accountid = os.environ['accountid']
                  policies = client.list_policies(
                      Filter='SERVICE_CONTROL_POLICY'
                    )
                  policy_name = 'SandboxRegions'
                  denypolicyname = [name['Name'] for name in policies['Policies']]
                  denypolicyid = [id['Id'] for id in policies['Policies']]

                  if policy_name in denypolicyname:
                    print ("Policy already exists")
                    for i, (name, id) in enumerate(zip(denypolicyname, denypolicyid)):
                      if policy_name in name:
                        attach = client.attach_policy(
                            PolicyId=id,
                            TargetId=accountid
                            )
                        print("Policy apply in account")
                  else:
                    policy = client.create_policy(
                      Content='{"Version":"2012-10-17","Statement":[{"Sid":"SandboxRegions","Effect":"Deny","NotAction":["iam:*","organizations:*","route53:*","budgets:*","waf:*","cloudfront:*","globalaccelerator:*","importexport:*","support:*","servicequotas:*","directconnect:*"],"Resource":["*"],"Condition":{"StringNotEquals":{"aws:RequestedRegion":["us-east-1","sa-east-1"]}}}]}',
                      Description='Denny all services outsite N.Virginia and South America',
                      Name='SandboxRegions',
                      Type='SERVICE_CONTROL_POLICY'
                      )
    
                    policy_id = policy['Policy']['PolicySummary']['Id']
                  
                    attach = client.attach_policy(
                      PolicyId=policy_id,
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
               