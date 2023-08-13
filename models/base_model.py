#!/usr/bin/pyhon3
"""
all others classes inhert from this class
"""
import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """
    define all methods and attributes
    """
    def __init__(self, *args, **kwargs):
        """
        statrt init all attributes
        """
        frmt = "%Y-%m-%dT%H:%M:%S.%f"
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            storage.new(self)
        else:
            for k, v in kwargs.items():
                if k == "created_at" or k == "updated_at":
                    v = datetime.strptime(kwargs[k], frmt)
                if k != '__class__':
                    setattr(self, k, v)

    def __str__(self):
        """return attr of dictionary"""
        clsName = self.__class__.__name__
        dic = self.__dict__
        return f"[{clsName}] ({self.id}) {dic}"

    def save(self):
        """update the updated time"""
        self.updated_at = datetime.now()

    def to_dict(self):
        """create new dicction"""
        newDict = {}
        frm = "%Y-%m-%dT%H:%M:%S.%f"
        for k, v in self.__dict__.items():
            if k == "created_at" or k == "updated_at":
                newDict[k] = v.strftime(frm)
            else:
                if not v:
                    pass
                else:
                    newDict[k] = v
        newDict["__class__"] = self.__class__.__name__
        return newDict


md = BaseModel()
print(md)
print(md.to_dict())
