# Fractional / float Demo for Pyfhel, covering the different ways of encrypting
#   and decrypting.
import numpy as np
from numpy import random
from Pyfhel import Pyfhel, PyPtxt, PyCtxt
import time

class Float_HE:
    def __init__(self, showOutput=False):
        self.report = {}
        
        self.array1 = None
        self.array2 = None
        
        self.showOutput = showOutput
        
    def test(self, runs, size, fracDigits, useSameNumbers=True):
        # try fracDigits with 32 and then lower to 3
        if useSameNumbers:
            np.random.seed(0)
        
        if self.array1 is None:
            self.array1 = random.uniform(0, 1.0, size=(size))
        if self.array2 is None:
            self.array2 = random.uniform(0, 1.0, size=(size))
            
        if not useSameNumbers:
            self.array1 = random.uniform(0, 1.0, size=(size))
            self.array2 = random.uniform(0, 1.0, size=(size))
            
        
        array1 = np.round(self.array1, fracDigits)
        array2 = np.round(self.array2, fracDigits)
        
        ######################################################
        # print("Setup context (p=65537, base=2, intDigits=64, fracDigits = 3) and keys") 
        times = []
        for i in range(runs):
            t0 = time.time()
            
            HE = Pyfhel()           # Creating empty Pyfhel object
            HE.contextGen(p=65537, base=2, intDigits=64, fracDigits = fracDigits) 
                                    # Generating context. The value of p is important.
                                    #  There are many configurable parameters on this step
                                    #  More info in Demo_ContextParameters.py, and
                                    #  in the docs of the function (link to docs in README)
            HE.keyGen()             # Key Generation.
            
            t1 = time.time()
            times.append(t1 - t0)
        # print(f"Setup context and keys: {sum(times)/runs}")
        self.report["setup"] = sum(times)/runs
        

        ######################################################

        # print("Encryption") 
        times = []
        for i in range(runs):
            t0 = time.time()

            arr_ctxt1 = np.empty(len(array1), dtype=PyCtxt)
            arr_ctxt2 = np.empty(len(array2), dtype=PyCtxt)
            
            for i in np.arange(len(array1)):
                arr_ctxt1[i] = HE.encryptFrac(array1[i])
                arr_ctxt2[i] = HE.encryptFrac(array2[i])
            
            t1 = time.time()
            times.append(t1 - t0)
        # print(f"Encryption avg: {sum(times)/runs}")
        self.report["encryption"] = sum(times)/runs

        ######################################################

        # print("Addition") 
        times = []
        for i in range(runs):
            t0 = time.time()

            ctxtSum = arr_ctxt1 + arr_ctxt2
            
            t1 = time.time()
            times.append(t1 - t0)
        # print(f"Addition avg: {sum(times)/runs}")
        self.report["addition"] = sum(times)/runs

        ######################################################

        # print("Subtraction") 
        times = []
        for i in range(runs):
            t0 = time.time()

            ctxtSub = arr_ctxt1 - arr_ctxt2
            
            t1 = time.time()
            times.append(t1 - t0)
        # print(f"Subtraction avg: {sum(times)/runs}")
        self.report["subtraction"] = sum(times)/runs

        ######################################################

        # print("Multiplication") 
        times = []
        for i in range(runs):
            t0 = time.time()

            ctxtMul = arr_ctxt1 * arr_ctxt2
            
            t1 = time.time()
            times.append(t1 - t0)
        # print(f"Multiplication avg: {sum(times)/runs}")
        self.report["multiplication"] = sum(times)/runs

        ######################################################
        
        # print("Decryption")
        times = []
        for i in range(runs):
            t0 = time.time()
            resSum = [HE.decryptFrac(ctxtSum[i]) for i in np.arange(len(ctxtSum))]
            resSub = [HE.decryptFrac(ctxtSub[i]) for i in np.arange(len(ctxtSub))] 
            resMul = [HE.decryptFrac(ctxtMul[i]) for i in np.arange(len(ctxtMul))]

            t1 = time.time()
            times.append(t1 - t0)
        # print(f"Decryption avg: {sum(times)/runs}")
        
        self.report['decryption'] = sum(times) / runs

        ######################################################

        if self.showOutput:
            print(resSum, resSub, resMul)
        
if __name__ == '__main__':
    float_he_tester = Float_HE()
    float_he_tester.test(1, 100, 32)
    float_he_tester.test(1, 100, 3)
    