import boto3
from boto3.dynamodb.conditions import Key,Attr
client = boto3.client('dynamodb', region_name='us-west-2')
#dynamodb = boto3.resource('dynamodb')
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
#response = client.describe_table( TableName='dev_chat_history')
from datetime import date 
#table = dynamodb.TABLE='dev_chat_history'
table = dynamodb.Table('dev_chat_history')
datenow = str(date.today())
# response = table.put_item(
#         Item={
#             'id':4,
#             'userid': 5,
#             'question':" is it a test 1?",
#             'answer': 'Yes, for testing insertion process 1',
#             'date': f'{datenow}',
#             'status':'active',
#         }
#     )

# table_name = 'dev_chat_history'
userid_to_query=1
response = table.scan(
    FilterExpression=Attr("userid").eq(userid_to_query)
)
#print(response)
for item in response['Items']:
    print(item['question'])
# def enable_ttl(table_name, ttl_attribute_name):
#     """
#     Enables TTL on DynamoDB table for a given attribute name
#         on success, returns a status code of 200
#         on error, throws an exception

#     :param table_name: Name of the DynamoDB table
#     :param ttl_attribute_name: The name of the TTL attribute being provided to the table.
#     """
#     try:
#         dynamodb = boto3.client('dynamodb')

#         # Enable TTL on an existing DynamoDB table
#         response = dynamodb.update_time_to_live(
#         TableName=table_name,
#         TimeToLiveSpecification={
#             'Enabled': False,
#             "AttributeName":"expiration_time"
#         }
#     )
#         # In the returned response, check for a successful status code.
#         if response['ResponseMetadata']['HTTPStatusCode'] == 200:
#             print("TTL has been enabled successfully.")
#         else:
#             print(f"Failed to enable TTL, status code {response['ResponseMetadata']['HTTPStatusCode']}")
#     except Exception as ex:
#         print("Couldn't enable TTL in table %s. Here's why: %s" % (table_name, ex))
#         raise


# # your values
# enable_ttl('dev_chat_history', 'ExpirationTime')