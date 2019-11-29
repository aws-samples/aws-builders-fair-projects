import boto3
import json
import os
import time

# Update these 3 parameters for your environment
database_name = 'bot'
db_cluster_arn = 'arn:aws:rds:us-west-2:369432278579:cluster:bdfair'
db_credentials_secrets_store_arn = 'arn:aws:secretsmanager:us-west-2:369432278579:secret:dev/bdfair/aurora-Ty33LB'

# This is the Data API client that will be used in our examples below
rds_client = boto3.client('rds-data')

# Timing function executions
def timeit(f):
    def timed(*args, **kw):
        ts = time.time()
        result = f(*args, **kw)
        te = time.time()
        print(f'Function: {f.__name__}')
        print(f'*  args: {args}')
        print(f'*  kw: {kw}')
        print(f'*  execution time: {(te-ts)*1000:8.2f} ms')
        return result
    return timed

def begin_transaction():
    transaction = rds_client.begin_transaction(
    secretArn=db_credentials_secrets_store_arn,
    resourceArn=db_cluster_arn,
    database=database_name)
    return transaction['transactionId']

def commit_transaction(transactionId):
    transaction_response = rds_client.commit_transaction(
    secretArn=db_credentials_secrets_store_arn,
    resourceArn=db_cluster_arn,
    transactionId=transactionId)
    return transaction_response["transactionStatus"]

def rollback_transaction(transactionId):
    transaction_response = rds_client.rollback_transaction(
    secretArn=db_credentials_secrets_store_arn,
    resourceArn=db_cluster_arn,
    transactionId=transactionId)
    return transaction_response["transactionStatus"]

@timeit
def execute_statement(sql, sql_parameters=[],transactionId=None):
    parameters = {
            'secretArn': db_credentials_secrets_store_arn,
            'database': database_name,
            'resourceArn': db_cluster_arn,
            'sql': sql,
            'parameters': sql_parameters
        }
    if transactionId is not None:
        parameters['transactionId'] = transactionId
    response = rds_client.execute_statement(**parameters)
    return response

# Formatting query returned Field
def formatField(field):
   fieldName = list(field.keys())[0]
   if fieldName == 'isNull':
       return None
   return list(field.values())[0]
# Formatting query returned Record
def formatRecord(record):
   return [formatField(field) for field in record]
# Formatting query returned Field
def formatRecords(records):
   return [formatRecord(record) for record in records]

@timeit
def execute_get_query(sql, sql_parameters):
    print('===== Example - Simple query =====')
    response = execute_statement(sql, sql_parameters)
    print(response)
    
    return formatRecords(response['records'])

def insert_bot_request(bot_request_id, txId):
    sql= 'insert into bot_request (bot_request_id,conv_start_time) values (:bot_request_id,now())'
    entry = [{'name':'bot_request_id','value':{'longValue':bot_request_id}}]
    execute_statement(sql, entry, txId)

def insert_bot_request_steps(bot_request_id, stepname, s3path, txId):
    sql= 'insert into bot_request_steps (bot_request_id,step_name,s3url, start_time) values (:bot_request_id,:step_name,:s3url,now())'
    entry = [{'name':'bot_request_id','value':{'longValue':bot_request_id}},
    {'name':'step_name','value':{'stringValue':f'{stepname}'}},
    {'name':'s3url','value':{'stringValue':f'{s3path}'}}]
    execute_statement(sql, entry, txId)

def update_bot_request_steps(bot_request_id, translate_text, step_name, txId):
    sql= 'update bot_request_steps set end_time=now(), transcript_text=:transcript_text where step_name=:step_name and bot_request_id=:bot_request_id'
    entry = [{'name':'bot_request_id','value':{'longValue':bot_request_id}},
    {'name':'transcript_text','value':{'stringValue':f'{translate_text}'}},
    {'name':'step_name','value':{'stringValue':f'{step_name}'}}]
    execute_statement(sql, entry, txId)

def update_bot_request_language(bot_request_id,language,txId):
    sql= 'update bot_request set language_code=:language where bot_request_id=:bot_request_id'
    entry = [{'name':'bot_request_id','value':{'longValue':bot_request_id}},
    {'name':'language','value':{'stringValue':f'{language}'}}] 
    execute_statement(sql, entry, txId)

def update_bot_request_city(bot_request_id,city,txId):
    sql= 'update bot_request set city_name=:city where bot_request_id=:bot_request_id'
    entry = [{'name':'bot_request_id','value':{'longValue':bot_request_id}},
    {'name':'city','value':{'stringValue':f'{city}'}}] 
    execute_statement(sql, entry, txId)

def update_bot_request_resort(bot_request_id,resortname,txId):
    sql= 'update bot_request set resort_name=:resort_name where bot_request_id=:bot_request_id'
    entry = [{'name':'bot_request_id','value':{'longValue':bot_request_id}},
    {'name':'resort_name','value':{'stringValue':f'{resortname}'}}] 
    execute_statement(sql, entry, txId)

def insert_bot_request_lang_detection(bot_request_id, language, txId):
    sql= 'insert into bot_request_lang_detection (bot_request_id,language,start_time) values (:bot_request_id,:language,now())'
    entry = [{'name':'bot_request_id','value':{'longValue':bot_request_id}},
    {'name':'language','value':{'stringValue':f'{language}'}}]
    execute_statement(sql, entry, txId)

def getBotLanguage(bot_request_id):
    print('getting bot')
    sql= 'select language_code from bot_request where bot_request_id=:bot_request_id'
    entry = [{'name':'bot_request_id','value':{'longValue':bot_request_id}}]
    response_records = execute_get_query(sql, entry)
    print(response_records)
    for record in response_records:
        return record[0]
    return None

def getPendingLanguageDetectionJobs(bot_request_id):
    sql= 'select count(lang_detection_id) from bot_request_lang_detection where end_time is null and bot_request_id=:bot_request_id'
    entry = [{'name':'bot_request_id','value':{'longValue':bot_request_id}}]
    response_records = execute_get_query(sql, entry)
    print(response_records)
    for record in response_records:
        return record[0]
    return None

