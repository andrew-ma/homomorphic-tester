import numpy as np
from numpy import random
from test_Int_Fernet import Int_Fernet
from test_Float_Fernet import Float_Fernet
from test_Int_HE import Int_HE
from test_Float_HE import Float_HE
import csv
np.random.seed(0)

class HE_Fernet_Comparison():
    def __init__(self, ):
        self.int_fernet = Int_Fernet()
        self.int_HE = Int_HE()
        self.float_fernet = Float_Fernet()
        self.float_HE = Float_HE()
        
        self.report_filename = 'report.csv'

    
    def test_int(self):
        # same inputs to HE and fernet functions to verify match results
        array1 = random.randint(100, size=(100,))
        array2 = random.randint(100, size=(100,))
        
        array1_1 = np.copy(array1)
        array2_1 = np.copy(array2)
        
        # testing integers
        self.int_fernet.test(5, 100, arr1=array1, arr2=array2)
        self.int_HE.test(5, 100, arr1=array1_1, arr2=array2_1)
        
        # make sure the HE library actually produced correct results and matched up with non HE calculations
        assert np.equal(self.int_fernet.sum_arr, self.int_HE.sum_arr).all()
        assert np.equal(self.int_fernet.sub_arr, self.int_HE.sub_arr).all()
        assert np.equal(self.int_fernet.mul_arr, self.int_HE.mul_arr).all()
        
        report = {}
        
        for operation, operation_avg_time in self.int_fernet.report.items():
            if operation == 're_encryption':
                report[operation] = {
                    'fernet_time': operation_avg_time,
                    'he_time' : None,
                    'he_x_times_longer': None
                }
            else:
                report[operation] = {
                    'fernet_time': operation_avg_time,
                    'he_time' : self.int_HE.report[operation],
                    'he_x_times_longer': self.int_HE.report[operation] / operation_avg_time
                }
                
        return report
        

    def test_float(self, num_decimals, float_tolerance=None):
        """
        if float_tolerance is None, it will calculate the maximum absolute difference and report it as the float tolerance
        if it is specified, the float tolerance will be asserted and it will cause exception if values not within float tolerance
        """
        # same inputs to HE and fernet functions to verify match results
        array1 = random.uniform(0, 1.0, size=(100,))
        array2 = random.uniform(0, 1.0, size=(100,))
        
        array1_1 = np.copy(array1)
        array2_1 = np.copy(array2)
        
        self.float_fernet.test(5, 100, num_decimals, arr1=array1, arr2=array2)
        self.float_HE.test(5, 100, num_decimals, arr1=array1_1, arr2=array2_1)
        
        # make sure the HE library actually produced correct results and matched up with non HE calculations
        sum_max_diff = np.abs(self.float_fernet.sum_arr - self.float_HE.sum_arr).max()
        sub_max_diff = np.abs(self.float_fernet.sub_arr - self.float_HE.sub_arr).max()
        mul_max_diff = np.abs(self.float_fernet.mul_arr - self.float_HE.mul_arr).max()
        
        results_float_tolerance = max([sum_max_diff, sub_max_diff, mul_max_diff])
        
        if float_tolerance is not None:
            assert np.allclose(self.float_fernet.sum_arr, self.float_HE.sum_arr, atol=float_tolerance) , "Float Addition results don't match: " + str(self.float_fernet.sum_arr) + str(self.float_HE.sum_arr)
            assert np.allclose(self.float_fernet.sub_arr, self.float_HE.sub_arr, atol=float_tolerance), "Float Subtraction results don't match: " + str(self.float_fernet.sub_arr) + str(self.float_HE.sub_arr)
            assert np.allclose(self.float_fernet.mul_arr, self.float_HE.mul_arr, atol=float_tolerance), "Float Multiply results don't match: " + str(self.float_fernet.mul_arr) + str(self.float_HE.mul_arr)
                
        report = {}
        
        for operation, operation_avg_time in self.float_fernet.report.items():
            if operation == 're_encryption':
                report[operation] = {
                    'fernet_time': operation_avg_time,
                    'he_time' : None,
                    'he_x_times_longer': None
                }
                    
            else:
                report[operation] = {
                    'fernet_time': operation_avg_time,
                    'he_time' : self.float_HE.report[operation],
                    'he_x_times_longer': self.float_HE.report[operation] / operation_avg_time
                }
                
        return (report, results_float_tolerance)
        
        
    def run_tests(self):
        int_report = self.test_int()
        float_report_32, float_32_tol = self.test_float(32)
        float_report_10, float_10_tol = self.test_float(10)
        float_report_3, float_3_tol = self.test_float(3)
        print("32 tolerance:", float_32_tol)
        print("10 tolerance:", float_10_tol)
        print("3 tolerance:", float_3_tol)
        
        
        with open(self.report_filename, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Test Type', 'Operation', 'Fernet Time (s)', 'HE Time (s)', 'HE X Times Longer']) # header
            for operation, operation_info in int_report.items():
                csvwriter.writerow(['Integer', operation, operation_info['fernet_time'], operation_info['he_time'], operation_info['he_x_times_longer']])
                
            for operation, operation_info in float_report_32.items():
                csvwriter.writerow([f'Float 32 decimals (tolerance {float_32_tol:.3e})', operation, operation_info['fernet_time'], operation_info['he_time'], operation_info['he_x_times_longer']])
                
            for operation, operation_info in float_report_10.items():
                csvwriter.writerow([f'Float 10 decimals (tolerance {float_10_tol:.3e})', operation, operation_info['fernet_time'], operation_info['he_time'], operation_info['he_x_times_longer']])
            
            
            for operation, operation_info in float_report_3.items():
                csvwriter.writerow([f'Float 3 decimals (tolerance {float_3_tol:.3e})', operation, operation_info['fernet_time'], operation_info['he_time'], operation_info['he_x_times_longer']])
            
        
    
if __name__ == "__main__":
    tester = HE_Fernet_Comparison()
    tester.run_tests()