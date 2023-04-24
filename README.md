# Reset Retention period for RDS instances
Source code to reset retention period on RDS instances using Step Functions &amp; Lambda

findRDSInstancesWithNonZeroRetention: This function finds the DB instances which have backup retention period greater than 0.

performRDSActions: This function starts the RDS instance, modifies it & handles the callback pattern to ensure that the task token is returned to the STepFunction once the DB is in available state.


StepFunctionsDefinition: This file contains the definition of our Step function.