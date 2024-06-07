import unittest
import pickle
import hashlib
import enum
import datetime

class Color(enum.Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
class MyClass:
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y
     
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
def pickle_serialization(data,data2):
    pickled_data_first = pickle.dumps(data)
    pickled_data_second = pickle.dumps(data2)
    return pickled_data_first, pickled_data_second

def pickle_deserialization(data,data2):
    pickled_data_first = pickle.dumps(data)
    unpickled_data_first = pickle.loads(pickled_data_first)
    pickled_data_second = pickle.dumps(data2)
    unpickled_data_second = pickle.loads(pickled_data_second)
    return unpickled_data_first, unpickled_data_second

def pickle_integrity(data,data2):
    pickled_data_first = pickle.dumps(data)
    md5_first = hashlib.md5(pickled_data_first).hexdigest()
    pickled_data_second = pickle.dumps(data2)
    md5_second = hashlib.md5(pickled_data_second).hexdigest()
    return md5_first, md5_second

class TestPickleModule(unittest.TestCase):

    def setUp(self):
        self.test_cases = [
            1234567,#int
            3.4,#float
            "Hello, World!",#string
            [1, 2, 3, "four", 5.0], #lists
            {"key1": "value1", "key2": 2, "key3": 3.0}, #Dicts
            {1, 2, 3, 4, 5},# Sets
            (1, 2, 3, "four", 5.0), #tuple
            True, #bool,
            False, #bool,
            None,   #None
            Color.RED, #Enum
            datetime.datetime(2024, 5, 20, 12, 0, 0), #datetime
            0.12345678901234567890, #large float
            1234567890123456789012345678901234567890, #large int
            (1, "two", 3.0, [4, 5], {"six": 6}), #nested tuple
            {1, 2, 3, "four"}, #complex set
            {'key': 'value', 'key': 123, 'list': [1, 2, 3]}, #duplicate keys dict
            (1, "two", 3.0, [4, 5], {"six": 6}), #nested tuple
            {'key': 'value', 'int': 123, 'list': [1, 2, 3],'key': 'value'}, #dict
            0.0,   #zero float
            -0.0, #negative zero float
            1.79e308, #float with large exponent
            5e-324, #float with small exponent
            [[[[[[[[[1]]]]]]]]],    #nested list
            list(range(1000000)), #large list
            float('nan'), #nan
            float('inf'), #inf
            float('-inf'), #negative inf
            [], #empty list
            (),     #empty tuple
            {}, #empty dict
            set(), #empty set
            MyClass(x=123, y=123), #class       
        ]

    def test_pickle_serialization(self):
        for data in self.test_cases:
            with self.subTest(data=data):
                pickled_data = pickle.dumps(data)
                expected_pickled_data = pickle.dumps(data)
                self.assertEqual(pickled_data, expected_pickled_data, "Pickled data does not match expected result")

    def test_pickle_deserialization(self):
        for data in self.test_cases:
            with self.subTest(data=data):
                pickled_data = pickle.dumps(data)
                unpickled_data = pickle.loads(pickled_data)
                self.assertEqual(unpickled_data, data, "Unpickled data does not match original data")

    def test_pickle_integrity(self):
        for data in self.test_cases:
            with self.subTest(data=data):
                pickled_data = pickle.dumps(data)
                expected_md5 = hashlib.md5(pickled_data).hexdigest()
                md5_hash = hashlib.md5(pickled_data).hexdigest()
                self.assertEqual(md5_hash, expected_md5, "MD5 hash of pickled data does not match expected hash")

 
class AdditionalTests(unittest.TestCase):
    def test_custom_class(self):
        obj = MyClass()
        obj2 = MyClass()
        
        obj.x=123
        obj.y=123
        
        obj2.y=123
        obj2.x=123
        
        pickle = pickle_serialization(obj,obj2)
        unpickle=pickle_deserialization(obj,obj2)
        hash=pickle_integrity(obj,obj2)
        self.assertEqual(pickle[0], pickle[1], "Pickled data does not match expected result")
        self.assertEqual(unpickle[0], unpickle[1], "Unpickled data does not match original data")
        self.assertEqual(hash[0], hash[1], "MD5 hash of pickled data does not match expected hash")

    def test_recursive_list(self):
        obj = []
        obj.append(obj)
        obj2 = []
        obj2.append(obj2)
        pickle = pickle_serialization(obj,obj2)
        unpickle=pickle_deserialization(obj,obj2)
        hash=pickle_integrity(obj,obj2)
        self.assertEqual(pickle[0], pickle[1], "Pickled data does not match expected result")
        self.assertEqual(unpickle[0], unpickle[1], "Unpickled data does not match original data")
        self.assertEqual(hash[0], hash[1], "MD5 hash of pickled data does not match expected hash")
    
    def test_recursive_dict(self):
        obj = {}
        obj["self"] = obj
        obj2 = {}
        obj2["self"] = obj2
        pickle = pickle_serialization(obj,obj2)
        unpickle=pickle_deserialization(obj,obj2)
        hash=pickle_integrity(obj,obj2)
        self.assertEqual(pickle[0], pickle[1], "Pickled data does not match expected result")
        self.assertEqual(unpickle[0], unpickle[1], "Unpickled data does not match original data")
        self.assertEqual(hash[0], hash[1], "MD5 hash of pickled data does not match expected hash")
    

    def test_recursive_class(self):
        obj = Node(1)
        obj.next = obj
        obj2 = Node(1)
        obj2.next = obj2
        pickle = pickle_serialization(obj,obj2)
        unpickle=pickle_deserialization(obj,obj2)
        hash=pickle_integrity(obj,obj2)
        self.assertEqual(pickle[0], pickle[1], "Pickled data does not match expected result")
        self.assertEqual(unpickle[0], unpickle[1], "Unpickled data does not match original data")
        self.assertEqual(hash[0], hash[1], "MD5 hash of pickled data does not match expected hash")
    

    def test_Dict_Insert_History(self):
        obj = {}
        obj2 = {}
        obj2["key2"] = "value2"
        obj["key1"] = "value1"
        obj2["key1"] = "value1"
        obj["key2"] = "value2"
        pickle = pickle_serialization(obj,obj2)
        unpickle=pickle_deserialization(obj,obj2)
        hash=pickle_integrity(obj,obj2)
        self.assertEqual(pickle[0], pickle[1], "Pickled data does not match expected result")
        self.assertEqual(unpickle[0], unpickle[1], "Unpickled data does not match original data")
        self.assertEqual(hash[0], hash[1], "MD5 hash of pickled data does not match expected hash")
    
    def test_Dict_Delete_History(self):
        obj = {}
        obj2 = {}
        obj["key1"] = "value1"
        obj2["key1"] = "value1"
        del obj["key1"]
        obj["key2"] = "value2"
        obj2["key2"] = "value2"
        del obj2["key1"]
        pickle = pickle_serialization(obj,obj2)
        unpickle=pickle_deserialization(obj,obj2)
        hash=pickle_integrity(obj,obj2)
        self.assertEqual(pickle[0]  , pickle[1], "Pickled data does not match expected result")
        self.assertEqual(unpickle[0], unpickle[1], "Unpickled data does not match original data")
        self.assertEqual(hash[0], hash[1], "MD5 hash of pickled data does not match expected hash")

    def test_multiple_references(self):
        obj = [1, 2, 3]
        obj2 = obj
        pickle = pickle_serialization(obj,obj2)
        unpickle=pickle_deserialization(obj,obj2)
        hash=pickle_integrity(obj,obj2)
        self.assertEqual(pickle[0]  , pickle[1], "Pickled data does not match expected result")
        self.assertEqual(unpickle[0], unpickle[1], "Unpickled data does not match original data")
        self.assertEqual(hash[0], hash[1], "MD5 hash of pickled data does not match expected hash")

if __name__ == '__main__':
    unittest.main()
