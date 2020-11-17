# Usage of Pyfhel with Numpy
import numpy as np
from numpy import random
import time
from Pyfhel import Pyfhel, PyPtxt, PyCtxt

runs = 20
# start data
#  100 length numpy array of random numbers from 0-99
array1 = random.randint(100, size=(100,))
array2 = random.randint(100, size=(100,))

######################################################

print("Setup context and keys") 
times = []
for i in range(runs):
    t0 = time.time()
    
    HE = Pyfhel()           # Creating empty Pyfhel object
    HE.contextGen(p=65537)  # Generating context. The value of p is important.
                            #  There are many configurable parameters on this step
                            #  More info in Demo_ContextParameters.py, and
                            #  in the docs of the function (link to docs in README)
    HE.keyGen()             # Key Generation.
    
    t1 = time.time()
    times.append(t1 - t0)
print(f"Setup context and keys: {sum(times)/runs}")

######################################################

print("Encryption") 
times = []
for i in range(runs):
    t0 = time.time()
    # since we need to create empty arrays to encrypt, we include these in the time
    arr_ctxt1 = np.empty(len(array1),dtype=PyCtxt)
    arr_ctxt2 = np.empty(len(array1),dtype=PyCtxt)
    
    # Encrypting! This can be parallelized!
    for i in np.arange(len(array1)):
        arr_ctxt1[i] = HE.encryptInt(array1[i])
        arr_ctxt2[i] = HE.encryptInt(array2[i])
        
    t1 = time.time()
    times.append(t1 - t0)
print(f"Encryption avg: {sum(times)/runs}")

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

print("Decryption Sum")
times = []
for i in range(runs):
    t0 = time.time()
    resSum = [HE.decryptInt(ctxtSum[i]) for i in np.arange(len(ctxtSum))]
    t1 = time.time()
    times.append(t1 - t0)
print(f"Decryption Sum avg: {sum(times)/runs}")

######################################################

print("Decryption Subtraction")
times = []
for i in range(runs):
    t0 = time.time()
    resSub = [HE.decryptInt(ctxtSub[i]) for i in np.arange(len(ctxtSub))] 
    t1 = time.time()
    times.append(t1 - t0)
print(f"Decryption Subtraction avg: {sum(times)/runs}")

######################################################

print("Decryption Multiplication")
times = []
for i in range(runs):
    t0 = time.time()
    resMul = [HE.decryptInt(ctxtMul[i]) for i in np.arange(len(ctxtMul))]
    t1 = time.time()
    times.append(t1 - t0)
print(f"Decryption Multiplication avg: {sum(times)/runs}")

######################################################