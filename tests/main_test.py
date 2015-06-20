from nose import with_setup
import app

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
  test_app = app.app.test_client()
  rv = test_app.post('/create', data={'game': "jane game", 'date_time': app.unix_time(datetime.datetime.now())})
  print rv.headers
  print rv.data
  print rv.status

# post to /create the dict {game: alex's game, date_time: python's datetime now}

# @with_setup(my_setup, my_teardown)
# def test2():
# 	unix_time