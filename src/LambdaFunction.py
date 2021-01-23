import boto3
import os

def lambda_handler(event, context):
    
    client = boto3.client('events')

    training_job_info = client.describe_training_job(TrainingJobName=os.environ(['TransformJobId']))
    
    #Get Job Status
    if training_job_info["TrainingJobStatus"] != "Completed":
        return False
    else:
        return True

