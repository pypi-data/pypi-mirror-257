import ctypes
import sys
import time
import timeit
from multiprocessing import shared_memory, Array, Value
import pickle
from multiprocessing import Process


class PyObject(ctypes.Structure):
    _fields_ = [
        ("refcnt", ctypes.c_size_t),
        ("typeid", ctypes.c_void_p)
    ]

class PyInt(PyObject):
    _fields_ = [("val", ctypes.c_long)]

class PyFloat(PyObject):
    _fields_ = [("val", ctypes.c_double)]

class PyVarObject(PyObject):
    _fields_ = [("size", ctypes.c_size_t)]

class PyStr(PyVarObject):
    _fields_ = [("hash", ctypes.c_long),
                ("state", ctypes.c_int),
                ("_val", ctypes.c_char * 0)]

class PyLong(PyVarObject):
    _fields_ = [("_val", ctypes.c_uint16 * 0)]

def create_var_object(struct, obj):
    inner_type = None
    for name, t in struct._fields_:
        # 首先搜索名为_val的字段，并将其类型保存到inner_type中
        if name == "_val":
            inner_type = t._type_
            print(inner_type)
    if inner_type is not None:
        # 然后创建一个PyVarObject结构体读取obj对象中的size字段
        tmp = PyVarObject.from_address(id(obj))
        size = tmp.size

        # 再通过size字段的大小创建一个对应的Inner结构体类，它可
        # 以从struct继承，因为struct中的_val字段不占据内存。
        class Inner(struct):
            _fields_ = [("val", inner_type * size)]

        Inner.__name__ = struct.__name__
        struct = Inner
    return struct.from_address(id(obj))

class PyList(PyVarObject):
    # item字段是指针数组，这里表现为二级指针
    _fields_ = [("items", ctypes.POINTER(ctypes.POINTER(PyObject))),
                ("allocated", ctypes.c_size_t)]

    def print_field(self):
        # size字段表示指针数组中已经使用的元素个数
        # allocated字段表示这个指针数组的长度
        # 指针字段items指向可变长度的数组
        print(self.size, self.allocated, ctypes.byref(self.items[0]))


class PyBuffer(PyVarObject):
    """Python 3 Buffer Interface"""
    _fields_ = (('buf', ctypes.c_void_p),
                ('obj', ctypes.c_void_p), # owned reference
                ('len', ctypes.c_size_t),
                # itemsize is Py_ssize_t so it can be pointed to
                # by strides in the simple case.
                ('itemsize', ctypes.c_size_t),
                ('readonly', ctypes.c_int),
                ('ndim', ctypes.c_int),
                ('format', ctypes.c_char_p),
                ('shape', ctypes.POINTER(ctypes.c_size_t)),
                ('strides', ctypes.POINTER(ctypes.c_size_t)),
                ('suboffsets', ctypes.POINTER(ctypes.c_size_t)),
                # static store for shape and strides of
                # mono-dimensional buffers.
                ('smalltable', ctypes.c_size_t * 2),
                ('internal', ctypes.c_void_p))


def f(name):
    var_int = 666
    var_inta = 123
    pybuf = PyBuffer.from_address(id(shm_a.buf))
    print("pybuf -> ", pybuf.buf)
    bytes_b = PyInt.from_address(id(var_int))
    # bytes_a = PyInt.from_address(id(var_inta))
    bytes_a = PyInt.from_address(pybuf.buf)
    # bytes_b = PyInt.from_address(id(var_int))

    ctypes.memmove(ctypes.byref(bytes_a), ctypes.byref(bytes_b), sys.getsizeof(var_int))
    print("bytes_a = ", var_inta, bytes_a.val)
    print("bytes_b = ", var_int, bytes_b.val)
    shm_int = PyInt.from_address(pybuf.buf)
    print("shm_int -> ", bytes_b.val, shm_int.val)

# 测试一下添加元素
def test_list():
    t1 = time.time()
    alist = []
    alist_obj = PyList.from_address(id(alist))
    # alist_obj.allocated = 100000
    for i in range(100000):
        alist.append(i)
    alist_obj.print_field()
    print(1000 * (time.time() - t1))

    t1 = time.time()
    alist = [None] * 100000
    alist_obj = PyList.from_address(id(alist))
    # object = (PyObject * 1)()
    # print(id(object[0]),id(object[1]))
    # alist_obj.items = ctypes.cast(object, ctypes.POINTER(ctypes.POINTER(PyObject)))

    pybuf = PyBuffer.from_address(id(shm_a.buf))
    for i in range(100000):
        alist[i] = i
    # shm_int.val = 100
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()
    print("DO -> ")

    shm_int = PyInt.from_address(pybuf.buf)
    alist_obj.items[0] = ctypes.cast(ctypes.byref(shm_int), ctypes.POINTER(PyObject))
    alist_obj.print_field()
    print(1000 * (time.time() - t1))
    print("alist[0] = ", alist[0])
    alist = [1, 2.3, "abc"]
    alist = [0] * 16384

    for x in range(10):
        alist_obj.print_field()
        alist.append(x)

from cityhash import CityHash64

def steamIdToPlayerUid(uid):
    hash = CityHash64(str(uid).encode("utf-16-le"))
    return "%x" % (u32(u32(hash) + (hash >> 32) * 23))
FarmHash64("76561198419123487".encode("utf-16le"))

#
# shm_map = MPMapProperty(size=10485760, count=100)
# for i in range(100):
#     shm_map.append({"key":toUUID(uuid.uuid4()), "value": i})
#
# [x for x in shm_map]
# shm_map.close()

# print(timeit.timeit(lambda: shm_map.append({"key":123, "value": 456}), number=1000000))
# test_map = []
# print(timeit.timeit(lambda: test_map.append({"key":123, "value": 456}), number=1000000))
#
# shm_map[0]['value']
# print(timeit.timeit(lambda: shm_map[0]['value'], number=100000))
# print(timeit.timeit(lambda: test_map[0]['value'], number=100000))
