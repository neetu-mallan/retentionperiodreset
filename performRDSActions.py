import json
import boto3
import botocore
import os
import botocore.exceptions
import time

def lambda_handler(event, context):
    # TODO implement
    rdsClient=boto3.client('rds')
    sfnClient=boto3.client("stepfunctions")
    print('In lambda handler'+event['DBInstanceIdentifier'])
    dbName=event['DBInstanceIdentifier']
    print('In lambda handler TT'+event['TaskToken'])
    sfnToken=event['TaskToken']
    action=event['Action']
   
    
    if action=="Start" :
        dbInstances = rdsClient.start_db_instance(DBInstanceIdentifier=dbName)
    elif action =="Modify" :
        backupRetention=event['BackupRetentionPeriod']
        applyTime=event["ApplyImmediately"]
        print("backupRetention: "+str(backupRetention))
        dbInstances = rdsClient.modify_db_instance(DBInstanceIdentifier=dbName,ApplyImmediately=bool(applyTime),BackupRetentionPeriod=backupRetention)
        time.sleep(90)
        
        
    finalJSON={}
    waiter = rdsClient.get_waiter('db_instance_available')
    
    try:
        waiter.wait(DBInstanceIdentifier=dbName)
        print("DB Instance "+dbName+" is now available.")
        if action=="Start" :
            array = [{'key' : dbName, 'value' : 'started'}]
        elif action=="Modify" :
            array = [{'key' : dbName, 'value' : 'modified'}]
        finalJSON["RDSInstances"]=array
        sfnClient.send_task_success(taskToken=sfnToken,output=json.dumps(finalJSON))
        
        
    except botocore.exceptions.WaiterError as e:
        if "Max attempts exceeded" in e.message:
            errorMessage="Number of attempts exceeded in starting the DBInstance: "+ dbName
            print("Database did not start in 600 seconds")
        else :
            print("Error Message:"+e.message)  
            errorMessage="Error occurred while starting the DBInstance: "+ dbName
        sfnClient.send_task_failure(taskToken=sfnToken,error=errorMessage,cause=e.message)
        