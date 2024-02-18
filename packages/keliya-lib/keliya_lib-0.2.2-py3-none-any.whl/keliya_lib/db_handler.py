import json
import os
from . import log_handler
from decimal import Decimal
from datetime import datetime
import uuid

logger = log_handler.logger
now = datetime.now().isoformat()
id_key = os.environ['ID_KEY']

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def get_by_id(table, id):
    logger.info("executing db_handler.get_by_id ")
    data = table.get_item(Key={id_key: id})
    if "Item" in data:
        return {
            'statusCode': 200,
            'body': json.dumps(data['Item'],default=decimal_default)
        }
                
    else:
        return {
            'statusCode': 204,
            'body': json.dumps({"error":"no content"})
        }

def get_all_by_pagination(table, query_string_parameters):
    page_size = int(query_string_parameters.get('pageSize', 10))
    page_number = int(query_string_parameters.get('pageNumber', 1))
    last_evaluated_key = query_string_parameters.get('lastEvaluatedKey') if 'lastEvaluatedKey' in query_string_parameters else None 
    offset = (page_number - 1) * page_size
    exclusive_start_key = None
    response = None

    try:
        if offset != 0:
            exclusive_start_key = {id_key: last_evaluated_key} if last_evaluated_key else None
            response = table.scan(Limit=page_size, ExclusiveStartKey=exclusive_start_key)
        else:
            response = table.scan(Limit=page_size)
                    
        logger.info("retrieved data for page: %s", page_number) 
    
    except Exception as e:
        logger.error("error occured retrieving data  %s....",str(e))
        return {
            'statusCode': 400,
            'body': json.dumps({"error":"something went wrong"})
        }    

    items = response['Items']
    
    return {
        'statusCode': 200,
        'body': json.dumps({ "data": items, "lastEvaluatedKey" : items[-1][id_key] if items else 'null'}, default=decimal_default)
    }
    
def insert(table, data):
    body = json.loads(data)
    body[id_key] = str(uuid.uuid4())
    body['createdDate'] = now
    body['updatedDate'] = now
    try:
        table.put_item(Item=body)
    except Exception as e:
        logger.error("error occured saving data  %s....",str(e))
        return {
            'statusCode': 400,
            'body': json.dumps({"error":"something went wrong."})
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps({"message":"request success."})
    }

def delete_by_id(table, id):
    try:
        response = table.delete_item(Key={id_key: id})
        return {
            'statusCode': 202,
            'body': json.dumps({"message":"Item deleted successfully."})
        } 
    except Exception as e:
        logger.error("error deleting data  %s....", str(e))
        return {
            'statusCode': 400,
            'body': json.dumps({"error":"something went wrong"})
        }