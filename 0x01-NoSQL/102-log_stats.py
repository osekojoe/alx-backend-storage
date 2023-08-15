#!/usr/bin/env python3
'''
Improves 12-log_stats.py by adding the top 10 of the most present IPs
in the collection nginx of the database logs:
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

    print('IPs:')
    
    sorted_ips = all_collections.aggregate([
        {
            '$group': { '_id': '$ip', 'count': { '$sum': 1}}
        },
        {
            '$sort': {'count': -1}   
        }
    ])

    i = 0
    iterator = iter(sorted_ips)

    while i < 10:
        try:
            s = next(iterator)
            print(f"\t{s.get('_id')}: {s.get('count')}")
            i += 1
        except StopIteration:
            break

if __name__ == "__main__":
        logs_stats()
