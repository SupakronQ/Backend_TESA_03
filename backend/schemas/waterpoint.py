# def waterEnitity(item) -> dict:
#     return {

#         "id":str(item["_id"]),
#         "point1":item["point1"],
#         "point2":item["point2"],
#         "created":item["created"]
        
#     }

# def watersEnitity(entity) -> list:
#     return [waterEnitity(item) for item in entity]

def serializeDict(a) -> dict:
    return {**{i:str(a[i]) for i in a if i=='_id'},**{i:a[i] for i in a if i!='_id'}}

def serializeList(entity) -> list:
    return [serializeDict(a) for a in entity]