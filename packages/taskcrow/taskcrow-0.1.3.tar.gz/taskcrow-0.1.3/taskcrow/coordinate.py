from pymongo import MongoClient
from bson import ObjectId
import datetime

from .task import Task
from .utils.uuid import generate_uuid_from_seed


def generate_task_id(task_type, unique_id):
    task_id = str(generate_uuid_from_seed(f'{task_type}_{unique_id}'))
    return task_id


class TaskCoordinate:
    def __init__(self, dsn):
        self.client = MongoClient(dsn)
        self.db = self.client.task_db

    def create_task(self, task_type, parameters, unique_id=None):
        task_id = str(generate_uuid_from_seed(f'{task_type}_{unique_id}'))
        new_task = Task(self.db, task_type=task_type, parameters=parameters, task_id=task_id)
        task_id = new_task.save()
        return task_id

    def is_task_duplicate(self, task_id: str):
        is_duplicate = self.db.tasks.find_one({'_id': task_id})
        return is_duplicate

    def count_tasks(self, query):
        counts = self.db.tasks.count_documents(query)
        return counts

    def find_tasks(self, query, limit=10, skip=0):
        tasks = self.db.tasks.find(query).limit(limit).skip(skip)
        # return [Task(self.db, task_id=str(task['_id']), **task) for task in tasks]
        return [Task(self.db,
                     task_id=str(task['_id']),
                     task_type=task['type'],
                     status=task['status'],
                     # result=task['result'],
                     result=task['result2'],
                     parameters=task['parameters']) for task in tasks]

    def find_one_and_update(self, query, update, return_document=True):
        task = self.db.tasks.find_one_and_update(query, update, return_document=return_document)
        # return [Task(self.db, task_id=str(task['_id']), **task) for task in tasks]
        return Task(self.db,
                    task_id=str(task['_id']),
                    task_type=task['type'],
                    status=task['status'],
                    result=task['result'],
                    parameters=task['parameters'])

    def get_task(self, task_id):
        task_data = self.db.tasks.find_one({"_id": ObjectId(task_id)})
        if task_data:
            # return Task(self.db, task_id=task_id, **task_data)
            return Task(self.db,
                        task_id=task_id,
                        task_type=task_data['type'],
                        status=task_data['status'],
                        result=task_data['result'],
                        parameters=task_data['parameters']
                        )
        else:
            return None

    def update_task(self, task_id, status, result=None):
        task = self.get_task(task_id)
        if task:
            return task.update(status, result)
        else:
            return None
