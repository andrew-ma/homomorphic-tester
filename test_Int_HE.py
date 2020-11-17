# Usage of Pyfhel with Numpy
import numpy as np
from numpy import random
import time
from Pyfhel import Pyfhel, PyPtxt, PyCtxt

class Int_HE:
    def __init__(self, showOutput=False):
        self.report = {}
                
        self.array1 = None
        self.array2 = None
        
        self.sum_arr = None
        self.sub_arr = None
        self.mul_arr = None
        
        self.showOutput = showOutput
    
    def test(self, runs, size, useSameNumbers=True, arr1=None, arr2=None):
        if useSameNumbers:
            np.random.seed(0)
            
        if arr1 is not None:
            self.array1 = arr1
        if arr2 is not None:
            self.array2 = arr2
            
            
        #  100 length numpy array of random numbers from 0-99
        if self.array1 is None:
            self.array1 = random.randint(100, size=(size,))
        if self.array2 is None:
            self.array2 = random.randint(100, size=(size,))
            
        if not useSameNumbers and arr1 is None and arr2 is None:
            self.array1 = random.randint(100, size=(size,))
            self.array2 = random.randint(100, size=(size,))
            
        array1 = self.array1
        array2 = self.array2

        ######################################################

        # print("Setup context and keys") 
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
        # print(f"Setup context and keys: {sum(times)/runs}")
        self.report['setup'] = sum(times) / runs
        
        ######################################################

        # print("Encryption") 
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
        # print(f"Encryption avg: {sum(times)/runs}")
        self.report['encryption'] = sum(times) / runs

        ######################################################

        # print("Vectorized addition")
        times = []
        for i in range(runs):
            t0 = time.time()
            ctxtSum = arr_ctxt1 + arr_ctxt2         # `ctxt1 += ctxt2` for quicker inplace operation
            t1 = time.time()
            times.append(t1 - t0)
        # print(f"Vectorized addition avg: {sum(times)/runs}")
        self.report['addition'] = sum(times) / runs
        
        ######################################################

        # print("Vectorized subtraction")
        times = []
        for i in range(runs):
            t0 = time.time()
            ctxtSub = arr_ctxt1 - arr_ctxt2
            t1 = time.time()
            times.append(t1 - t0)
        # print(f"Vectorized subtraction avg: {sum(times)/runs}")
        self.report['subtraction'] = sum(times) / runs
        
        ######################################################

        # print("Vectorized multiplication")
        times = []
        for i in range(runs):
            t0 = time.time()
            ctxtMul = arr_ctxt1 * arr_ctxt2
            t1 = time.time()
            times.append(t1 - t0)
        # print(f"Vectorized multiplication avg: {sum(times)/runs}")
        self.report['multiplication'] = sum(times) / runs
        
        ######################################################

        # print("Decryption")
        times = []
        for i in range(runs):
            t0 = time.time()
            resSum = [HE.decryptInt(ctxtSum[i]) for i in np.arange(len(ctxtSum))]
            resSub = [HE.decryptInt(ctxtSub[i]) for i in np.arange(len(ctxtSub))] 
            resMul = [HE.decryptInt(ctxtMul[i]) for i in np.arange(len(ctxtMul))]

            t1 = time.time()
            times.append(t1 - t0)
        # print(f"Decryption avg: {sum(times)/runs}")
        
        self.report['decryption'] = sum(times) / runs
        
        if (self.showOutput):
            print(resSum, resSub, resMul)
            
        self.sum_arr = resSum
        self.sub_arr = resSub
        self.mul_arr = resMul
        
        ######################################################
        
        
if __name__ == '__main__':
    int_he_tester = Int_HE()
    int_he_tester.test(1, 100)
    int_he_tester.test(1, 100)
    
    