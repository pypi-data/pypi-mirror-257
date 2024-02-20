from enum import Enum
from pymongo import MongoClient
from bson import ObjectId
import datetime


class Task:
    def __init__(self, db, task_id=None, task_type=None, parameters=None, status=None, result=None):
        self.db = db
        self.task_id = task_id
        self.task_type = task_type
        self.parameters = parameters
        self.status = status
        self.result = result

    def save(self):
        task_data = {
            "_id": self.task_id,
            "type": self.task_type,
            "parameters": self.parameters,
            "status": "pending",
            "result": None,
            "timestamp": datetime.now()
        }

        return self.db.tasks.insert_one(task_data).inserted_id

    def insert(self, status, result=None):
        self.status = status
        self.result = result
        return self.db.tasks.insert_one(
            # {"_id": ObjectId(self.task_id)},
            {"_id": self.task_id},
            {"$set": {"status": status, "result": result}}
        )

    def update(self, status, result=None):
        self.status = status
        self.result = result
        return self.db.tasks.update_one(
            # {"_id": ObjectId(self.task_id)},
            {"_id": self.task_id},
            {"$set": {"status": status, "result": result}}
        )

    def delete(self):
        return self.db.tasks.delete_one({"_id": ObjectId(self.task_id)})
        # return self.db.tasks.delete_one({"_id": ObjectId(self.task_id)})
