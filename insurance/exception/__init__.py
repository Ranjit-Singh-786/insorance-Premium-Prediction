# exception file. to control execution of our program
import sys

class InsuranceException(Exception):
    def __init__(self, error_message:Exception, error_detail:sys):
        super().__init__(error_message)
        self.error_message = InsuranceException.error_message_detail(error_message,error_detail=error_detail)
    
    @staticmethod
    def error_message_detail(error:Exception, error_detail:sys)->str:
        error_class,error_mesage,exc_tb = error_detail.exc_info()
        line_number = exc_tb.tb_frame.f_lineno  # to get line number
        file_name = exc_tb.tb_frame.f_code.co_filename
        # formating of error message
        error_message = f" error occured in this {file_name} file, at the line no. [{line_number}], Error message :- [{error_mesage}]"
        return error_message
    
    def __str__(self):
        return InsuranceException.__name__.__str__()