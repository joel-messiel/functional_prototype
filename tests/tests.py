import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.loginModel import loginModel
from mock_functions import mockChangePasswordModel

def test_login_model():
    """

    """
    # TC-ADM-01-01: valid email and valid password
    assert loginModel("p.delpueblo@coopmanati.net", "123") is not None
    # TC-ADM-01-02: invalid email and invalid password
    assert loginModel("juan.del.pueblo@gmail.com", "") == {}
    # TC-ADM-01-03: valid email and invalid password
    assert loginModel("p.delpueblo@coopmanati.net", "12345") == {}


def test_reset_password_model():
    """

    """
    # TC-ADM-15-01: 
    assert mockChangePasswordModel("p.delpueblo@coopmanati.net", "12345", "12345") == 1
    # TC-ADM-15-02: 
    assert mockChangePasswordModel("p.delpueblo@coopmanati.net", "12345", "123") == -2
    # TC-ADM-15-03: 
    assert mockChangePasswordModel("juan.del.pueblo@gmail.com", "12345", "12345") == -1
