#!/usr/bin/env python3
'''
Python script that provides some stats about Nginx logs stored in MongoDB:
    Database: logs
    Collection: nginx
    Display (same as the example):
        first line: x logs where x is the number of documents in this collection
        second line: Methods:
        5 lines with the number of documents with the method = ["GET", "POST",
         "PUT", "PATCH", "DELETE"] in this order (see example below - warning:
         it’s a tabulation before each line)
        one line with the number of documents with:
            method=GET
            path=/status
'''


from pymongo import MongoClient


def logs_stats():
    '''provides some stats about Nginx logs stored in MongoDB'''
    client = MongoClient('mongodb://localhost:27017/')
    all_collections = client.logs.nginx
    count_all_documents = all_collections.count_documents({})

    with_get = all_collections.count_documents({'method': 'GET'})
    with_post = all_collections.count_documents({'method': 'POST'})
    with_put = all_collections.count_documents({'method': 'PUT'})
    with_patch = all_collections.count_documents({'method': 'PATCH'})
    with_delete = all_collections.count_documents({'method': 'DELETE'})

    special_log_count = all_collections.count_documents(
            {"method": "GET", "path": "/status"})

    print(f'{count_all_documents} logs')
    print('Methods:')
    print(f'\tmethod GET: {with_get}')
    print(f'\tmethod POST: {with_post}')
    print(f'\tmethod PUT: {with_put}')
    print(f'\tmethod PATCH: {with_patch}')
    print(f'\tmethod DELETE: {with_delete}')
    
    print(f'{special_log_count} status check')


if __name__ == "__main__":
        logs_stats()
