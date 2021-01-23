import boto3
import zipfile

'''
Service AWS Clients 
'''
client_events = boto3.client('events')
client_s3 = boto3.clinet('s3')
client_lambda = boto3.client('lammbda')

'''
    Execute List Jobs operation to get the Transform 
   job status  
'''
def CheckTransformJobStatus(TransformJobResponse):
    training_job_info = client_events.describe_training_job(TrainingJobName=TransformJobResponse)
    CreateLambdaFunction(TransformJobName=training_job_info)
    
''' 
    Associate Rule condition to default Event Bus.

    Name : Rule Name
    ScheduleExpression : condition time expressio
    State : Enabled | Disabled
    Description : text description of Rule content
    EventBusName : Event Bus Name already created during AWS account creation.
'''
def PutRuleCondition():
    response = client_events.put_rule(
    Name='TransformJobRule',
    ScheduleExpression='rate(5 minutes)',    
    State='ENABLED',
    Description='test',    
    Tags=[
        {
            'Key': 'Version',
            'Value': '1.0'
        },
    ],
    EventBusName='default'
)
    

def PutTargetCondition(LambdaArn,RuleName):
    response_event = client_events.put_targets(
    Rule= RuleName,
    EventBusName='default',
    Targets=[
        {
            "Id": "LambdaTargetTransformJob", 
            "Arn": LambdaArn 
        }
    ]
)

''' 
    Create Lambda Function associating TransformJob to Environment Variable.
'''
def CreateLambdaFunction(TransformJobName):
    functionPackage = zipfile.ZipFile('function.zip','w')
    functionPackage.write('./index.py')

    client_lambda= boto3.client('lambda')
    client_s3 = boto3.client('s3')

    #Put Object on S3 bucket (Lambda Function)
    with open('function.zip','rb') as zip:    
        client_s3.put_object(Body=zip, Bucket ='cloud-atlas-lambda-function', Key="function.zip")

    response = client_lambda.create_function(
         Code={
        'S3Bucket': 'cloud-atlas-lambda-function',
        'S3Key': "function.zip",
        },
        FunctionName='LambdaFunction',
        Runtime= 'python3.6',
        Role='arn:aws:iam::885248014373:role/service-role/cloud-atlas-twitter-role-k1n1jg7v',
        Handler='LambdaFunction.handler',   
        Description='Lambda Function to check Transform Job Status.',
        Environment={
        'Variables': {
            'TransformJobName': TransformJobName,            
                    },
            },
        Timeout = 10,
        MemorySize = 256,
        Publish=True,       
    )

    PutTargetCondition(response['ResponseMetadata']['FunctionArn'],RuleName="TransformJobRule")


