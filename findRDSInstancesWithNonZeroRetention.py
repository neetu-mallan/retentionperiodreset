import boto3
import os
import json

def lambda_handler(event, context):
    # TODO implement
    rdsClient=boto3.client('rds')
    print('In lambda handler')
    dbInstances= rdsClient.describe_db_instances()
    print('RDS Instances Size: '+str(len(dbInstances)))
    index=0

    rdsInstanceDict={}
    finalJSON={}
    while index < len(dbInstances['DBInstances']):
        dbInstance=dbInstances['DBInstances'][index]
        retentionPeriod=dbInstance["BackupRetentionPeriod"]
        dbName=dbInstance["DBInstanceIdentifier"]
        status=dbInstance["DBInstanceStatus"]
        if retentionPeriod>0:
            rdsInstanceDict[dbName]=status
            
        index=index+1
    array = [ {'key' : i, 'value' : rdsInstanceDict[i]} for i in rdsInstanceDict]
    finalJSON["RDSInstances"]=array
    print('RDS Instances With Retention: '+str(len(rdsInstanceDict)))
    return finalJSON
    
