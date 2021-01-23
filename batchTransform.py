import os
import boto3
import EventBridge as eb

# Get Configs to Execute job
role = config.get("deploy").get("role")
codename = config.get("deploy").get("codename")
instance_type = config.get("deploy").get("instance_type")
instance_count = config.get("deploy").get("instance_count")
training_job_name = config.get("deploy").get("training_job_name")

#Instance and describe job
client = boto3.client("sagemaker")

#Create transform job and get Response Code
response_tranform_job  = client.create_transform_job(
    TransformJobName='string3',
    ModelName='sagemaker-pytorch-2021-01-17-19-45-55-738',
    MaxConcurrentTransforms=1,
    ModelClientConfig={
        'InvocationsTimeoutInSeconds': 123,
        'InvocationsMaxRetries': 1
    },
    MaxPayloadInMB=10,
    BatchStrategy='SingleRecord',
    Environment={
        'SAGEMAKER_PROGRAM': 'train.py',
        'SAGEMAKER_SUBMIT_DIRECTORY': "s3://sagemaker-us-east-1-885248014373/sagemaker-pytorch-2021-01-17-19-45-55-738/source/sourcedir.tar.gz"
    },
    TransformInput={
        'DataSource': {
            'S3DataSource': {
                'S3DataType': 'S3Prefix',
                'S3Uri': 's3://cloud-atlas-twitter-885248014373-us-east-1/newfile.json'
            }
        },
        'ContentType': 'text/plain',
        'CompressionType': 'None',
        'SplitType': 'None'
    },
    TransformOutput={
        'S3OutputPath': 's3://cloud-atlas-twitter-885248014373-us-east-1/output',
        'Accept': 'text/plain'
    },
    TransformResources={
        'InstanceType': 'ml.m4.xlarge',
        'InstanceCount': 1
    }
)
#Send Transform Job ARN
eb.CheckTransformJobStatus(response_tranform_job)


