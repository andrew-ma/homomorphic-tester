from test_Int_Fernet import Int_Fernet
from test_Float_Fernet import Float_Fernet
from test_Int_HE import Int_HE
from test_Float_HE import Float_HE
import csv

class HE_Fernet_Comparison():
    def __init__(self, ):
        self.int_fernet = Int_Fernet()
        self.int_HE = Int_HE()
        self.float_fernet = Float_Fernet()
        self.float_HE = Float_HE()
        
        self.report_filename = 'report.csv'

    
    def test_int(self):
        # testing integers
        self.int_fernet.test(20, 100)
        self.int_HE.test(20, 100)
        
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
        

    def test_float(self, num_decimals):
        self.float_fernet.test(20, 100, num_decimals)
        self.float_HE.test(20, 100, num_decimals)
                
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
                
        return report
        
        
    def run_tests(self):
        int_report = self.test_int()
        float_report_32 = self.test_float(32)
        float_report_3 = self.test_float(3)
        
        
        with open(self.report_filename, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Test Type', 'Operation', 'Fernet Time', 'HE Time', 'HE X Times Longer']) # header
            for operation, operation_info in int_report.items():
                csvwriter.writerow(['Integer', operation, operation_info['fernet_time'], operation_info['he_time'], operation_info['he_x_times_longer']])
                
            for operation, operation_info in float_report_32.items():
                csvwriter.writerow(['Float 32 decimals', operation, operation_info['fernet_time'], operation_info['he_time'], operation_info['he_x_times_longer']])
            
            for operation, operation_info in float_report_3.items():
                csvwriter.writerow(['Float 3 decimals', operation, operation_info['fernet_time'], operation_info['he_time'], operation_info['he_x_times_longer']])
            
        
    
if __name__ == "__main__":
    tester = HE_Fernet_Comparison()
    tester.run_tests()