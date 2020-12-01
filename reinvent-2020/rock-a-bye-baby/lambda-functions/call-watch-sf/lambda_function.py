import boto3
import logging
import os


logger = logging.getLogger()
logger.setLevel(logging.INFO)

# The Amazon Resource Name (ARN) of the state machine to execute.
# Example - arn:aws:states:us-west-2:112233445566:stateMachine:HelloWorld-StateMachine
STATE_MACHINE_ARN = os.environ['smArn']

def lambda_handler(event, context):

    #The string that contains the JSON input data for the execution
    INPUT = "{\"timer_seconds\": 120}"

    sfn = boto3.client('stepfunctions')

    response = sfn.start_execution(
        stateMachineArn=STATE_MACHINE_ARN,
        input=INPUT
    )

    #display the arn that identifies the execution
    logging.info ('SF ARN:' + response.get('executionArn'))
