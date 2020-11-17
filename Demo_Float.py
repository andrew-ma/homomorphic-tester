# Fractional / float Demo for Pyfhel, covering the different ways of encrypting
#   and decrypting.

from Pyfhel import Pyfhel, PyPtxt, PyCtxt
import time

runs = 20


######################################################
print("Setup context (p=65537, base=2, intDigits=64, fracDigits = 3) and keys") 
times = []
for i in range(runs):
    t0 = time.time()
    
    HE = Pyfhel()           # Creating empty Pyfhel object
    HE.contextGen(p=65537, base=2, intDigits=64, fracDigits = 32) 
                            # Generating context. The value of p is important.
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

    float1 = -7.3
    float2 = 3.4
    ctxt1 = HE.encryptFrac(float1) # Encryption makes use of the public key
    ctxt2 = HE.encryptFrac(float2) # For integers, encryptInt function is used.
    
    t1 = time.time()
    times.append(t1 - t0)
print(f"Encryption avg: {sum(times)/runs}")

######################################################

print("Addition") 
times = []
for i in range(runs):
    t0 = time.time()

    ctxtSum = ctxt1 + ctxt2
    
    t1 = time.time()
    times.append(t1 - t0)
print(f"Addition avg: {sum(times)/runs}")

######################################################

print("Subtraction") 
times = []
for i in range(runs):
    t0 = time.time()

    ctxtSub = ctxt1 - ctxt2
    
    t1 = time.time()
    times.append(t1 - t0)
print(f"Subtraction avg: {sum(times)/runs}")

######################################################

print("Multiplication") 
times = []
for i in range(runs):
    t0 = time.time()

    ctxtMul = ctxt1 * ctxt2
    
    t1 = time.time()
    times.append(t1 - t0)
print(f"Multiplication avg: {sum(times)/runs}")

######################################################

print("Decryption Sum") 
times = []
for i in range(runs):
    t0 = time.time()

    resSum = HE.decryptFrac(ctxtSum)
    
    t1 = time.time()
    times.append(t1 - t0)
print(f"Decryption Sum avg: {sum(times)/runs}")

######################################################


print("Decryption Subtraction") 
times = []
for i in range(runs):
    t0 = time.time()

    resSub = HE.decryptFrac(ctxtSub)
    
    t1 = time.time()
    times.append(t1 - t0)
print(f"Decryption Subtraction avg: {sum(times)/runs}")

######################################################


print("Decryption Multiplication") 
times = []
for i in range(runs):
    t0 = time.time()

    resMul = HE.decryptFrac(ctxtMul)
    
    t1 = time.time()
    times.append(t1 - t0)
print(f"Decryption Multiplication avg: {sum(times)/runs}")

######################################################

print(resSum, resSub, resMul)
print("NOTE: Very accurate! Let's try lowering the fracDigits from the context.")
print("==============================================================")

######################################################
######################################################
######################################################
######################################################

######################################################
print("Setup context (p=65537, base=2, intDigits=64, fracDigits = 3) and keys") 
times = []
for i in range(runs):
    t0 = time.time()
    
    HE = Pyfhel()           # Creating empty Pyfhel object
    HE.contextGen(p=65537, base=2, intDigits=64, fracDigits = 3)
                            # Generating context. The value of p is important.
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

    float1 = -7.3
    float2 = 3.4
    ctxt1 = HE.encryptFrac(float1) # Encryption makes use of the public key
    ctxt2 = HE.encryptFrac(float2) # For integers, encryptInt function is used.
    
    t1 = time.time()
    times.append(t1 - t0)
print(f"Encryption avg: {sum(times)/runs}")

######################################################

print("Addition") 
times = []
for i in range(runs):
    t0 = time.time()

    ctxtSum = ctxt1 + ctxt2
    
    t1 = time.time()
    times.append(t1 - t0)
print(f"Addition avg: {sum(times)/runs}")

######################################################

print("Subtraction") 
times = []
for i in range(runs):
    t0 = time.time()

    ctxtSub = ctxt1 - ctxt2
    
    t1 = time.time()
    times.append(t1 - t0)
print(f"Subtraction avg: {sum(times)/runs}")

######################################################

print("Multiplication") 
times = []
for i in range(runs):
    t0 = time.time()

    ctxtMul = ctxt1 * ctxt2
    
    t1 = time.time()
    times.append(t1 - t0)
print(f"Multiplication avg: {sum(times)/runs}")

######################################################

print("Decryption Sum") 
times = []
for i in range(runs):
    t0 = time.time()

    resSum = HE.decryptFrac(ctxtSum)
    
    t1 = time.time()
    times.append(t1 - t0)
print(f"Decryption Sum avg: {sum(times)/runs}")

######################################################


print("Decryption Subtraction") 
times = []
for i in range(runs):
    t0 = time.time()

    resSub = HE.decryptFrac(ctxtSub)
    
    t1 = time.time()
    times.append(t1 - t0)
print(f"Decryption Subtraction avg: {sum(times)/runs}")

######################################################


print("Decryption Multiplication") 
times = []
for i in range(runs):
    t0 = time.time()

    resMul = HE.decryptFrac(ctxtMul)
    
    t1 = time.time()
    times.append(t1 - t0)
print(f"Decryption Multiplication avg: {sum(times)/runs}")

######################################################

print("NOTE: As you can see, the accuracy drops! As usual, there is a tradeoff.")
print(resSum, resSub, resMul)