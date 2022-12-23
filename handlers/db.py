import pymongo
from pymongo.server_api import ServerApi
from configurebot import cfg

dburl = cfg['db_url']
db = cfg['db_name']

client = pymongo.MongoClient(dburl, server_api=ServerApi('1'))
db = client[db]
profiles = db['profiles']
statistics = db['statistics']

def db_profile_exist(uid):
    if profiles.find_one({"_id": uid}) != None:
        return True
    else:
        return False

def db_profile_exist_usr(username):
    if profiles.find_one({"username": username}) != None:
        return True
    else:
        return False

def db_profile_insertone(query):
    return profiles.insert_one(query)

def db_profile_access(uid):
    return profiles.find_one({'_id': uid})['access']

def db_profile_banned(uid):
    if profiles.find_one({'_id': uid})['ban'] == 1:
        return True
    else:
        return False

def db_profile_updateone(query, query2):
    return profiles.update_one(query, query2)

def db_profile_get_usrname(username, get):
    return profiles.find_one({'username': username})[get]

def db_statistics_insertone(query):
    return statistics.insert_one(query)

def db_statistics_find_last(query):
    return statistics.find_one(query,sort=[('_id', pymongo.DESCENDING)])

def db_statistics_updateone(query, query2):
    return statistics.update_one(query, query2)
