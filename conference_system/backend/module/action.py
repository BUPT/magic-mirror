"""
File: action.py
Author: Duan-JM
Email: vincent.duan95@outlook.com
Github: https://github.com/Duan-JM
Description:
    Define the Actions, such as send emails, split video/audio, merge video/audio
"""
class base_action:
    """
    base action module for futuer
    """
    def get_inputs(self, input_data):
        """
        Check if input_data match the requirements, if True receive the input
        """
        raise NotImplementedError

    def process(self):
        """
        Use `self.input_data` to do some actions
        """
        raise NotImplementedError

