from nose import with_setup
from app import unix_time



def my_setup():
	print 'this starts before test'

def my_teardown():
	print 'this happens after test'

def setup_module():
	print 'this happens first'

def teardown_module():
	print 'this happens last'

@with_setup(my_setup, my_teardown)
def test1():
	unix_time

@with_setup(my_setup, my_teardown)
def test2():
	unix_time