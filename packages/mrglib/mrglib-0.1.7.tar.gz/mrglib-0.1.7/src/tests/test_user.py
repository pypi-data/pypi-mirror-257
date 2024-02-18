from mrglib import User

def test_login():
    u = User.User('testuser','testp@ss4676')
    retcode = u.login()
    assert (retcode == 0)

def test_find_project():
    u = User.User('testuser','testp@ss4676')
    retcode = u.find_project('testuser')
    assert (retcode == 0)

def test_new_experiment():
    u = User.User('testuser','testp@ss4676')
    retcode = u.create_experiment('testexp1', 'testuser', 'test description 1')
    assert (retcode == 0)
