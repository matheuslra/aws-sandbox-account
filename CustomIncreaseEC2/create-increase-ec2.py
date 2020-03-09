import boto3, json, traceback, time
import cfnresponse
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
def lambda_handler(event, context):
  response_data = {}
  try:
    if event["RequestType"] == "Create" or event["RequestType"] == "Update":
      logger.info("Event Body - " + json.dumps(event))
      client = boto3.client('service-quotas')
      ssm = boto3.client('ssm')
      
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
    elif event["RequestType"] == "Delete":
            logger.info("Event Body - " + json.dumps(event))
            cfnresponse.send(event, context, cfnresponse.SUCCESS,{})
    else:
            logger.info("Event Body - " + json.dumps(event))
            cfnresponse.send(event, context, cfnresponse.FAILED,{})
  except Exception as e:
        msg = 'See details in CloudWatch Log Stream: ' + context.log_stream_name
        response_data['exception'] = str(e)[0:255] + '... ' + msg
        cfnresponse.send(event, context, cfnresponse.FAILED, response_data)