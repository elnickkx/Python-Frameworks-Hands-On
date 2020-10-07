import os, sys
import logging, inspect
import botocore
from awsClass import awsClass
import argparse
import pprint

# logging proc structure for the valid executable script and throwable exception

logger = logging.getLogger('root')
loggingFormat = "[%(filename)s: %(lineno)s- %(funcName)20s() ]  %(message)s"
logging.basicConfig(format=loggingFormat)
logger.setLevel(logging.DEBUG)


class awsPolling:
  def __init__(self, specificRegion, specificService):
    
    super().__init__()
    self.specificRegion = specificRegion
    self.specificService = specificService
    
  def dirLocation(self):
    
    basedir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, basedir)
    logger.debug("Having base dirname")
    return basedir

  # getting all botocore exceptions for error handling

  def botocoreException(self):
    
    for key, values in botocore.exceptions.__dict__.items():
      if(isinstance(values, type)):
        return (key+ "  " +str(values))

    logger.debug("BotoCore Exceptions ")
  
  # Controller method for "health" aws service api
  
  def healthController(self, apiCall):
    
    try:
      self.statusCodes = ['open', 'upcoming']
      headLookException = self.botocoreException()
      awsObj = awsClass()
      awsObj = awsObj.awshealth(apiCall, self.specificRegion, self.specificService, self.statusCodes)
      logger.debug("Health controller for AWS: "+ str(awsObj))
      return awsObj

    except Exception as err:
      logger.warn("Loggging Health Error: "+ str(err)+ "\n")
      return str(err)
      exit()
  
  # Controller method for "STS rules" aws service api
   
  def stsController(self, apis, arnRole): #, path):
    
    # jsonFile = self.dirLocation() + "/" + path
    
    try:
      headLookException = self.botocoreException()
      awsObj = awsClass(self.specificRegion)
      assumeRole = awsObj.awsSTSRole(apiCall=apis, roleARN=arnRole) #, filePath=jsonFile)
      # awsObj = awsObj.decodeAuthMessage()
      credentials = awsObj.roleDataExtraction(assumeRoleCredentials=assumeRole)
      logger.debug("STS rule controller for AWS ")
      
      
    except Exception as err:
      logger.exception("Loggging STS Error: "+ str(err) + "\n")
      raise
      exit()

    else:
      return credentials

  def instanceController(self, externCall, credentials):
    
    try:
      awsInstance = awsClass(self.specificRegion)
      logger.info("Spinning the AWS Instance with STS Credentials .")
      objStatus = awsInstance.clientSpinStatusCheck(externService=externCall, tmpCredentials=credentials)
      
    except Exception as err:
      logger.exception("Loggging spinned Instance fatal error: "+ str(err) + "\n")
      raise
      exit()
      
    else:
      return objStatus

# implicity call adverable method for inline __main__ instance

if __name__ == '__main__':
  
  # Parsing AWS arguements through command line / terminal
  
  parser = argparse.ArgumentParser(description="Parsing AWS Programatical Arguements", argument_default=argparse.SUPPRESS)
  parser.add_argument('--Region', '-R', action="store", nargs="*", default="", help="Region of the AWS Endpoint")
  parser.add_argument('--Service', '-S', action="store", nargs="*", default="", help="Service issues for AWS Endpoint")
  parser.add_argument('--APIS', '-I', action="store", nargs="*", default="", help="APIs call for targeted AWS Service")
  # parser.add_argument('--Extern', '-E', action="store", nargs="*", default="", help="Call for targeted External AWS Service")
  parser.add_argument('--RoleARN', '-A', action="store", nargs="*", default="", help="AWS Resource Name role index")
  # parser.add_argument('--PolicyJSON', '-P', action="store", nargs="*", default="dumpObj.json", help="Absolute Path to policy JSON for STS role rendering")
  
  args = parser.parse_args()
  
  # Conditional check for the cli arguements parsed based on requirements dependencies
   
  REGION = args.Region
  if len(REGION) > 0:
    REGION = REGION[0]
    logger.debug(REGION)
  else:
    logger.debug(REGION)
    
  services = args.Service
  if len(services) > 0:
    services = services[0]
    logger.debug(services)
  else:  
    logger.debug(services)
  
  apis = args.APIS
  if len(apis) > 0:
    apis = apis[0]
    logger.debug(apis)
  else:
    logger.debug(apis)
  
  # extern = args.Extern
  # if len(extern) > 0:
  #   extern = extern[0]
  #   logger.debug(extern)
  # else:
  #   logger.debug(extern)
  
  arnRole = args.RoleARN
  if len(arnRole) > 0:
    arnRole = arnRole[0]
    logger.debug(arnRole)
  else:  
    logger.debug(arnRole)
  
  # jsonPath = args.PolicyJSON
  # if jsonPath and jsonPath != "/":
  #   jsonPath = jsonPath[0]
  #   logger.debug(jsonPath)
  # else:
  #   logger.debug(jsonPath)
    

  # health dashboard logic for aws polling
  if apis == 'health':
    healthPoller = awsPolling(specificRegion=REGION, specificService=services)
    logger.debug("Logging for Health Poller "+ str(healthPoller.healthController(apiCall=apis))+ "\n")

  # AWS STS logical functionality for assumeRole Feature 
  
  elif apis == 'sts':
    stsPoller = awsPolling(specificRegion=REGION, specificService=services)
    logger.debug("Logging for STS rule Poller "+ str(stsPoller)+ "\n")
    assumeRoleCreds = stsPoller.stsController(apis=apis, arnRole=arnRole)
    # pprint.pprint(assumeRoleCreds)
    serviceStatus = stsPoller.instanceController(externCall=services, credentials=assumeRoleCreds)
    pprint.pprint(serviceStatus)

  else:
    regions = awsClass(REGION=REGION)
    regions = regions.scanRegion(service=services)
    pprint.pprint(regions)
    logger.info("APIs call for targeted AWS service is not Specified or Arguemented ")
    
  # ARN : 179790312905
  # userARN: arn:aws:iam::179790312905:user/Adminstrator
  # role_Lambda: arn:aws:iam::179790312905:role/Ec2_LambdaCheck