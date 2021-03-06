from importlib import import_module
import os, sys
tests_path = os.path.join(os.getcwd(), "integration", "tests")
if not tests_path in sys.path:
	sys.path.insert(0, tests_path)


class IntegrationTest:

	def __init__(self, name, function):

		self.name = name
		self.function = function
		self.source = "github.com/buddycloud/buddycloud-tests-framework/blob/master/integration/tests/" + name + ".py"

	def jsonfy(self):

		json = { 'name' : self.name,
			 'test' : self.function,
			 'continue_if_fail' : True,
			 'source' : self.source
		}
		return json


test_entries = []
suite_config_path = os.path.join(os.getcwd(), "integration", "integration_tests.cfg")
config = open(suite_config_path)

for test_name in config.xreadlines():

	test_name = test_name.strip().replace(".py", "")
	if test_name.startswith("#"):
		continue

	problem_loading = False
	test_reference = None
	try:
		test_reference = getattr(import_module(test_name), "testFunction")
		test_reference = IntegrationTest(test_name, test_reference)
	except Exception, e:
		print "Problem: "+str(e)
		print "Error: "+test_name+" could not be loaded. Ignoring this test..."
		problem_loading = True

	if problem_loading or test_reference == None:
		continue

	test_entries.append(test_reference.jsonfy())


config.close()

del config
