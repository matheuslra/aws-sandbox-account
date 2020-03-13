import boto3, json
import cfnresponse
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
def lambda_handler(event, context):
  responseData = {}
  logger.info('event: {}'.format(event))
  logger.info('context: {}'.format(context))
  client = boto3.client('service-quotas')
  ssm = boto3.client('ssm')
  logger.info('Always printing the event: {}'.format(event))
  if event["RequestType"] == "Create" or event["RequestType"] == "Update":
    try:
      logger.info("Event Body - " + json.dumps(event))
      limit_ec2 = ssm.get_parameter(
          Name='ec2_limit'
          )
      value_limit_ec2 = limit_ec2['Parameter']['Value']
      print(value_limit_ec2)
      
      get_quota = client.get_service_quota(
            ServiceCode='ec2',
            QuotaCode='L-1216C47A'
        )
      value_service_quota = get_quota['Quota']['Value']
      print(value_service_quota)

      if float(value_limit_ec2) > value_service_quota :
          response = client.request_service_quota_increase(
            ServiceCode='ec2',
            QuotaCode='L-1216C47A',
            DesiredValue=float(value_limit_ec2)
            )
      else:
          print("Parameter is diferent then current service quota value")
      cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData, 'CustomResourcePhysicalID')   
    except Exception as e:
      logger.error(e, exc_info=True)
      responseData = {'Error': str(e)}
      cfnresponse.send(event, context, cfnresponse.FAILED, responseData, 'CustomResourcePhysicalID')

  if event["RequestType"] == "Delete":
    logger.info("Event Body - " + json.dumps(event))
    cfnresponse.send(event, context, cfnresponse.SUCCESS,{})