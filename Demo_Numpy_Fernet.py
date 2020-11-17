# Usage of Pyfhel with Numpy
import numpy as np
from numpy import random
import time
from cryptography.fernet import Fernet
import pickle

runs = 20
# start data
#  100 length numpy array of random numbers from 1 to 100
array1 = random.randint(100, size=(100,))
array2 = random.randint(100, size=(100,))

######################################################

print("Setup context and keys") 
times = []
for i in range(runs):
    t0 = time.time()
    
    key = Fernet.generate_key()
    f = Fernet(key)
    
    t1 = time.time()
    times.append(t1 - t0)
print(f"Setup context and keys: {sum(times)/runs}")

######################################################

print("Encryption") 
times = []
for i in range(runs):
    t0 = time.time()
    
    arr1_bytes = pickle.dumps(array1)
    arr2_bytes = pickle.dumps(array2)
    encrypted_arr1 = f.encrypt(arr1_bytes)
    encrypted_arr2 = f.encrypt(arr2_bytes)
    
    t1 = time.time()
    times.append(t1 - t0)
print(f"Encryption avg: {sum(times)/runs}")

######################################################


print("Decryption") 
times = []
for i in range(runs):
    t0 = time.time()
    
    decrypted_arr1 = f.decrypt(encrypted_arr1)
    decrypted_arr2 = f.decrypt(encrypted_arr2)
    arr_ctxt1 = pickle.loads(decrypted_arr1)
    arr_ctxt2 = pickle.loads(decrypted_arr2)
    
    t1 = time.time()
    times.append(t1 - t0)
print(f"Decryption avg: {sum(times)/runs}")

######################################################


print("Vectorized addition")
times = []
for i in range(runs):
    t0 = time.time()
    ctxtSum = arr_ctxt1 + arr_ctxt2         # `ctxt1 += ctxt2` for quicker inplace operation
    t1 = time.time()
    times.append(t1 - t0)
print(f"Vectorized addition avg: {sum(times)/runs}")

######################################################
print("Vectorized subtraction")
times = []
for i in range(runs):
    t0 = time.time()
    ctxtSub = arr_ctxt1 - arr_ctxt2
    t1 = time.time()
    times.append(t1 - t0)
print(f"Vectorized subtraction avg: {sum(times)/runs}")
######################################################
print("Vectorized multiplication")
times = []
for i in range(runs):
    t0 = time.time()
    ctxtMul = arr_ctxt1 * arr_ctxt2
    t1 = time.time()
    times.append(t1 - t0)
print(f"Vectorized multiplication avg: {sum(times)/runs}")

######################################################