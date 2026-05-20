from pymongo import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient(
    "mongodb+srv://<username>:<password>@allord.4d7ahvt.mongodb.net/?appName=Allord",
    #<username> and <password> should be replaced with yours.
    server_api=ServerApi('1')
)

db = client["cats"]
collection = db["cats"]

def add_cat(name, age, features):

    '''Adds cat to DB'''

    cat = {
        "name": name,
        "age": age,
        "features": features
    }

    result = collection.insert_one(cat)
    print(f"Cat added with ID: {result.inserted_id}")

def get_all_cats():

    '''Prints all DB cat entities to console'''

    cats = collection.find()
    if cats:
        for cat in cats:
            print(cat)
    else:
        print("No cats are there yet")

def get_cat_by_name(cat_name):

    '''prints info from DB of cat with specified name'''

    cat = collection.find_one({'name': cat_name})

    if cat:
        print(cat)
    else:
        print("Cat not found")

def update_age_by_name(cat_name, updated_age):

    '''updates age of cat in DB by cat name'''

    result = collection.update_one({"name": cat_name}, {"$set": {"age": updated_age}})

    if result.modified_count:
        print("Age updated successfully")
        get_cat_by_name(cat_name)
    else:
        print("Cat not found")
    
def add_new_feature_by_name(cat_name, feature):

    '''adds one more feature to cat with specified name'''

    result = collection.update_one({"name": cat_name}, {"$push": {"features": feature}})
    
    if result.modified_count:
        print("Feature added successfully")
        get_cat_by_name(cat_name)
    else:
        print("Cat not found")
    
    
def delete_cat_by_name(cat_name):

    '''deleter cat by specified name'''

    result = collection.delete_one({"name": cat_name})

    if result.deleted_count:
        print("Cat deleted successfully")
    else:
        print("Cat not found")

def orphanage_closed():

    '''deletes all cat entities in DB'''

    result = collection.delete_many({})

    print(f"Deleted {result.deleted_count} cats")