import sys

def error_message_details(error,error_detail:sys):
    _,_,exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    error_message = f'Execution failed: Exception in <{file_name}> at line <{line_number}> with error: {str(error)}'
    return error_message

class CException(Exception):
    
    def __init__(self,error_message,error_detail:sys):
        super.__init__(error_message)
        self.error_message = error_message_details(error_message,error_detail=error_detail)
    
    def __str__9(self):
        return self.error_message