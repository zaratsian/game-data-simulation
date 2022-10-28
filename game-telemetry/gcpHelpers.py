import json


def saveToLocal(outputFilename, dataContent):
    try:
        f = open(outputFilename, 'w')
        f.write(dataContent)
        f.close()
        print(f'[ INFO ] Saved data to local file {outputFilename}.')
    except Exception as e:
        print(f'[ EXCEPTION ] At saveToLocal. {e}')


def saveFileToCloudStorage(bucket_name, blob_name, source_file_name):
    from google.cloud import storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(source_file_name)
    print(f'[ INFO ] {source_file_name} uploaded to {bucket_name} as {blob_name}')


def saveObjectToCloudStorage(bucket_name, blob_name, data):
    from google.cloud import storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(data)
    print(f'[ INFO ] In memory data uploaded to {bucket_name} as {blob_name}')


def push_to_pubsub(pubsub_publisher, project_id, pubsub_topic, json_paylod):
    topic_path = pubsub_publisher.topic_path(project_id, pubsub_topic)
    # Data must be a bytestring
    data = json.dumps(json_paylod).encode('utf-8')
    
    future = pubsub_publisher.publish(topic_path, data)
    print(future.result())
    print(f"Published message to {topic_path}.")


def saveToBigQuery(gcpProjectID, bqDataset, bqTable, rows_to_insert):
    '''
        BigQuery Streaming Insert
        NOTE: Streaming insert cost extra.
        
        rows_to_insert = [
            {"full_name": "Phred Phlyntstone", "age": 32},
            {"full_name": "Wylma Phlyntstone", "age": 29},
        ]
    '''
    from google.cloud import bigquery
    bigquery_client = bigquery.Client()
    table_id = f'{gcpProjectID}.{bqDataset}.{bqTable}'
    errors = bigquery_client.insert_rows_json(table_id, rows_to_insert)
    if errors == []:
        print(f'[ INFO ] {len(rows_to_insert)} new rows have been added.')
    else:
        print(f'[ WARNING ] Encountered errors while inserting rows: {errors}')


def createBQTable(gcpProjectID, bqDataset, bqTable, schema):
    try:
        from google.cloud import bigquery
        bigquery_client = bigquery.Client()
        table_id = f'{gcpProjectID}.{bqDataset}.{bqTable}'
        table = bigquery.Table(table_id, schema=schema)
        table = bigquery_client.create_table(table)
        print("[ INFO ] Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id))
    except Exception as e:
        print(f'[ EXCEPTION ] At createBQTable. {e}')


def saveToSpanner(instance_id, database_id, table_id, payload):
    '''
    payload = {'eventId': '16668855067540', 'userid': '466789f8-d5ad-424d-b915-3d7650dd5385', 'username': 'Sofia Rocha', 
    'datetime': '2020-02-03 04:34:00', 'points': 60, 'itemID': 1100, 'itemName': 'Black Shorts', 'itemPrice': 32, 
    'visitsToStore': 2, 'minutesPlayed': 262.7593307912732, 'gameType': 'tournament', 'newFriends': 1, 
    'offensePercentage': 0.6576237224090705, 'defensePercentage': 0.3423762775909295, 'timeWithBall': 0.19510076783810765, 
    'scoredGoal': False, 'scoredOn': False, 'fieldPosition_DefendingLeftSidePct': 0.20579079432692798, 
    'fieldPosition_DefendingRightSidePct': 0.1365854832640015, 'fieldPosition_AttackingLeftSidePct': 0.44318056517044807, 
    'fieldPosition_AttackingRightSidePct': 0.21444315723862245, 'platform': 'ps4'}
    '''
    from google.cloud import spanner
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)
    
    def spannerQuery(transaction):
        columnNames = ','.join(list(payload))
        columnValues = tuple(payload.values())
        row_ct = transaction.execute_update(f'''
            INSERT INTO {table_id} ({columnNames}) VALUES
            {columnValues}
            '''
        )
        print("{} record(s) inserted.".format(row_ct))
    
    database.run_in_transaction(spannerQuery)
    return None


def streamToPubSub(project_id, pubsub_publisher, pubsub_topic, json_paylod):
    try:
        topic_path = pubsub_publisher.topic_path(project_id, pubsub_topic)
        # Data must be a bytestring
        data = json.dumps(json_paylod).encode('utf-8')
        
        future = pubsub_publisher.publish(topic_path, data)
        print(future.result())
        print(f"Published message to {topic_path}.")
    except Exception as e:
        print(f'[ EXCEPTION ] At streamToPubSub. {e}')
