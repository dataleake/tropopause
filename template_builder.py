from troposphere import sqs, s3
from troposphere import GetAtt, Ref
from troposphere import Template, Parameter
from troposphere.awslambda import Function, Code, Environment, TracingConfig, EventSourceMapping, Permission
from troposphere.sqs import Queue, QueuePolicy, RedrivePolicy
from troposphere.iam import Role, Policy
import regex

# Object that will generate the template
t = Template()

# Gather input and validate correct datatype
def validate_user_input(type, prompt):
    while True:
        response = input(prompt)
        if response is not None:
            if(type == "String" or type = 'y/n'):
                check_for_punc = re.search("[[:punct:]]", response)
                if (check_for_punc):
                    print("Please no punctuation")
                    continue
            elif (type == "int"):
                try:
                    response = int(response)
                except ValueError:
                    print("Please only integers")
                    continue
        return response



# Bucket Creation Template
## A template to create a template
def main():
    logicalName = validate_user_input("String", "Logical Name for bucket (All spaces will be removed): ")
    logicalName = logicalName.replace(" ", "")
    print(logicalName)

    bucketName = validate_user_input("String","Actual Bucket Name (Will be converted to lowercase): ")
    bucketName = bucketName.lower()
    print(bucketName)

    dpolicy = validate_user_input("String","Deletion Policy [y/n]: ")
    dpolicy = dpolicy.upper()

    if (dpolicy == 'Y'):
        print("[1] Retain")
        deletePolicy = validate_user_input("int","Policy Number: ")
        if (deletePolicy == 1):
            deletePolicy = "Retain"
    print(deletePolicy)

    dependency = validate_user_input("String","Any dependencies? [y/n]: ")
    dependency = dependency.upper()
    print(dependency)
    if (dependency == 'Y'):
        dependsOn = validate_user_input("String","Depends on: ")

    accelerateConfig = validate_user_input("String","Accelerate the Configuration [y/n]: ")
    accelerateConfig = accelerateConfig.upper()

    if (accelerateConfig == 'Y'):
        print("[1] Suspended")
        print("[2] Enabled")
        accelerateStatus = validate_user_input("int","Acceleration Status number: ")
        if (accelerateStatus == 1):
            accelerateStatus = "Suspended" 
        else:
            accelerateStatus = "Enabled"

    buildBucket = s3.Bucket(
        logicalName,
        BucketName = bucketName,
        DeletionPolicy = deletePolicy,
        DependsOn = [
            dependsOn
        ],
        AccelerateConfiguration = s3.AccelerateConfiguration(
            AccelerationStatus = accelerateStatus
        )

    )

    t.add_resource(buildBucket)
    print(t.to_yaml())



main()
