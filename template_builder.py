# Bucket Creation Template
## A template to create a template
def main():
    logicalName = input("Logical Name for bucket (All spaces will be removed): ")
    logicalName = logicalName.replace(" ", "")
    print(logicalName)
    
    bucketName = input("Actual Bucket Name (Will be converted to lowercase): ")
    bucketName = bucketName.lower()
    print(bucketName)

    dpolicy = input("Deletion Policy [y/n]: ")
    dpolicy = dpolicy.upper()
    if (dpolicy == 'Y'):
        print("[1] Retain")
        deletePolicy = input("Policy Number: ")
        if (deletePolicy == 1):
            deletePolicy = "Retain"
    print(deletePolicy)

    dependency = input("Any dependencies? [y/n]: ")
    dependency = dependency.upper()

    print(dependency)
    if (dependency == 'Y'):
        dependsOn = input("Depends on: ")

    accelerateConfig = input("Accelerate the Configuration [y/n]: ")
    accelerateConfig = accelerateConfig.upper()

    if (accelerateConfig == 'Y'):
        print("[1] Suspended")
        print("[2] Enabled")
        accelerateStatus = input("Acceleration Status number: ")
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
