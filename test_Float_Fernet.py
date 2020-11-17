# Usage of Pyfhel with Numpy
import numpy as np
from numpy import random
import time
from cryptography.fernet import Fernet
import pickle


class Float_Fernet:
    def __init__(self, showOutput=False):
        self.report = {} # key (description) : value (average time)
        
        self.array1 = None
        self.array2 = None
        
        self.sum_arr = None
        self.sub_arr = None
        self.mul_arr = None
        
        self.showOutput = showOutput
    
    def test(self, runs, size, fracDigits, useSameNumbers=True, arr1=None, arr2=None):
        # try fracDigits with 32 and then lower to 3
        if useSameNumbers:
            np.random.seed(0)
            
        if arr1 is not None:
            self.array1 = arr1
        if arr2 is not None:
            self.array2 = arr2
        
        if self.array1 is None:
            self.array1 = random.uniform(0, 1.0, size=(size,))
        if self.array2 is None:
            self.array2 = random.uniform(0, 1.0, size=(size,))
            
        if not useSameNumbers and arr1 is None and arr2 is None:
            self.array1 = random.uniform(0, 1.0, size=(size,))
            self.array2 = random.uniform(0, 1.0, size=(size,))
            
        
        array1 = np.round(self.array1, fracDigits)
        array2 = np.round(self.array2, fracDigits)

        ######################################################

        # print("Setup context and keys") 
        times = []
        for i in range(runs):
            t0 = time.time()
            
            key = Fernet.generate_key()
            f = Fernet(key)
            
            t1 = time.time()
            times.append(t1 - t0)
        # print(f"Setup context and keys: {sum(times)/runs}")
        self.report["setup"] = sum(times)/runs

        ######################################################

        # print("Encryption") 
        times = []
        for i in range(runs):
            t0 = time.time()
            
            arr1_bytes = pickle.dumps(array1)
            arr2_bytes = pickle.dumps(array2)
            encrypted_arr1 = f.encrypt(arr1_bytes)
            encrypted_arr2 = f.encrypt(arr2_bytes)
            
            t1 = time.time()
            times.append(t1 - t0)
        # print(f"Encryption avg: {sum(times)/runs}")
        self.report["encryption"] = sum(times)/runs

        ######################################################


        # print("Decryption") 
        times = []
        for i in range(runs):
            t0 = time.time()
            
            decrypted_arr1 = f.decrypt(encrypted_arr1)
            decrypted_arr2 = f.decrypt(encrypted_arr2)
            arr_ctxt1 = pickle.loads(decrypted_arr1)
            arr_ctxt2 = pickle.loads(decrypted_arr2)
            
            t1 = time.time()
            times.append(t1 - t0)
        # print(f"Decryption avg: {sum(times)/runs}")
        self.report['decryption'] = sum(times)/runs

        ######################################################


        # print("Vectorized addition")
        times = []
        for i in range(runs):
            t0 = time.time()
            ctxtSum = arr_ctxt1 + arr_ctxt2         # `ctxt1 += ctxt2` for quicker inplace operation
            t1 = time.time()
            times.append(t1 - t0)
        # print(f"Vectorized addition avg: {sum(times)/runs}")
        self.report['addition'] = sum(times)/runs

        ######################################################
        # print("Vectorized subtraction")
        times = []
        for i in range(runs):
            t0 = time.time()
            ctxtSub = arr_ctxt1 - arr_ctxt2
            t1 = time.time()
            times.append(t1 - t0)
        # print(f"Vectorized subtraction avg: {sum(times)/runs}")
        self.report['subtraction'] = sum(times)/runs
        
        ######################################################
        # print("Vectorized multiplication")
        times = []
        for i in range(runs):
            t0 = time.time()
            ctxtMul = arr_ctxt1 * arr_ctxt2
            t1 = time.time()
            times.append(t1 - t0)
        # print(f"Vectorized multiplication avg: {sum(times)/runs}")
        self.report['multiplication'] = sum(times)/runs
        
        if self.showOutput:
            print(ctxtSum, ctxtSub, ctxtMul)
            
        self.sum_arr = ctxtSum
        self.sub_arr = ctxtSub
        self.mul_arr = ctxtMul

        ######################################################
        
        ### if we factor in the extra time to reencrypt the files
        
        # print("ReEncryption") 
        times = []
        for i in range(runs):
            t0 = time.time()
            
            sum_arr_bytes = pickle.dumps(ctxtSum)
            sub_arr_bytes = pickle.dumps(ctxtSub)
            mult_arr_bytes = pickle.dumps(ctxtMul)
            encrypted_sum_arr = f.encrypt(sum_arr_bytes)
            encrypted_sub_arr = f.encrypt(sub_arr_bytes)
            encrypted_mult_arr = f.encrypt(mult_arr_bytes)
            
            t1 = time.time()
            times.append(t1 - t0)
        # print(f"ReEncryption avg: {sum(times)/runs}")
        self.report["re_encryption"] = sum(times)/runs

        ######################################################


if __name__ == '__main__':
    float_fernet_tester = Float_Fernet()
    float_fernet_tester.test(1, 100, 32)
    float_fernet_tester.test(1, 100, 3)