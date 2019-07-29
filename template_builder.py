from troposphere import sqs, s3
from troposphere import GetAtt, Ref
from troposphere import Template, Parameter
from troposphere.awslambda import Function, Code, Environment, TracingConfig, EventSourceMapping, Permission
from troposphere.sqs import Queue, QueuePolicy, RedrivePolicy
from troposphere.iam import Role, Policy
import regex
import time

# Object that will generate the template
t = Template()

# Gather input and validate correct datatype
def validate_user_input(type, prompt, max_ = 0, min_ = 1): # pick int between min_ and max_
    # Loop until user submits a valid response
    while True:
        # Collect users input to custom questions
        response = input(prompt)
        # If there actually is a response then validate
        if (response is not None or response is not ''):
            # If the answer is a string or the response to a yes or no then...
            if(type == "String" or type == 'y/n'):
                # Check the response for any special characters as they are usually not allowed
                ## In the cases that they are, have user input a code that refers to that character
                check_for_punc = re.search("[[:punct:]]", response)
                # If there is punctuation, return to collecting input
                if (check_for_punc):
                    print("Please no punctuation")
                    continue
                # If there is no punctuation and the response is yes/no
                if (type == 'y/n'):
                    response = response.upper()
                    check_for_yn = re.search("[YN]", response)
                    # If the user didnt enter a "Y" or "N"
                    if not check_for_yn:
                        print("Please select either \n[y] yes \n[n] no")
                        continue
            # If the response should be an integer, validate here
            elif (type == "int"):
                try:
                    # Attempt to convert input to integer
                    response = int(response)
                    if (response > max_):
                        print("Please pick a value between {} and {}".format(min_, max_))
                        continue
                except ValueError:
                    print("Please only integers")
                    continue
        else:
            # If the input is blank or None type return to prompt
            print("Please enter a value")
            continue
        return response



# Bucket Creation Template
## A template to create a template
def main():
    # Collect logical name
    logicalName = validate_user_input("String", "Logical Name for bucket (No space|spec.char): ")
    logicalName = logicalName.replace(" ", "")
    print(logicalName)

    bucketName = validate_user_input("String","Actual Bucket Name (No space|spec.char|upper): ")
    bucketName = bucketName.lower()
    bucketName = bucketName.replace(" ", "")
    print(bucketName)

    dpolicy = validate_user_input("y/n","Set Deletion Policy [y/n]: ")

    if (dpolicy == 'Y'):
        print("[1] Retain")
        deletePolicy = validate_user_input("int","Policy Number: ", 1)
        if (deletePolicy == 1):
            deletePolicy = "Retain"
    else:
        deletePolicy = "No Policy"
    print(deletePolicy)

    dependency = validate_user_input("y/n","Any dependencies? [y/n]: ")
    print(dependency)
    if (dependency == 'Y'):
        dependsOn = validate_user_input("String","Depends on: ")
    else:
        print("No Dependency")

    accelerateConfig = validate_user_input("y/n","Accelerate the Configuration [y/n]: ")

    if (accelerateConfig == 'Y'):
        print("Which configuration?")
        print("[1] Suspended")
        print("[2] Enabled")
        accelerateStatus = validate_user_input("int","Acceleration Status number: ", 2)
        if (accelerateStatus == 1):
            accelerateStatus = "Suspended" 
        else:
            accelerateStatus = "Enabled"
    else:
        # Must have a value for the time being
        accelerateStatus = "Suspended" 

    print("\nBuilding Template Now...\n")
    # Pause for effect
    time.sleep(2)
    
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


