import string, json
from api_utils import prepare_and_send_request
from find_api_location import findAPILocation

#HTTP_API endpoint: /:channel/metadata/posts
def all_metadata_access(api_location, username, target_channel_name):

	(status, response) = prepare_and_send_request('GET', "%s%s/metadata/posts" % (api_location,
		target_channel_name), authorization=username)

	if status:

		response = json.loads(response.content)
		return ( 'title' in response
		and 'description' in response
		and 'access_model' in response
		and 'creation_date' in response
		and 'channel_type' in response
		and 'default_affiliation' in response )
	
	return False

#HTTP_API endpoint: /:channel/content/status
def mood_status_access(api_location, username, target_channel_name):

	(status, response) = prepare_and_send_request('GET', "%s%s/content/status" % (api_location,
		target_channel_name), authorization=username)

	return status

#HTTP_API endpoint: /:channel/content/posts
def posts_read_access(api_location, username, target_channel_name):

	(status, response) = prepare_and_send_request('GET', "%s%s/content/posts" % (api_location,
		target_channel_name), authorization=username)

	return status

#HTTP_API endpoint: /:channel/subscribers/posts
def subscribers_access(api_location, username, target_channel_name):

	(status, response) = prepare_and_send_request('GET', "%s%s/subscribers/posts" % (api_location,
		target_channel_name), authorization=username)

	return status

#HTTP_API endpoint: /subscribed
def subscribed_to_access(api_location, username, target_channel_name):

	(status, response) = prepare_and_send_request('GET', "%ssubscribed" % (api_location), authorization=username)

	return status

#HTTP_API endpoint: /:channel/content/geoloc
def geoloc_access(api_location, username, target_channel_name):

	(status, response) = prepare_and_send_request('GET', "%s%s/content/geoloc" % (api_location,
		target_channel_name), authorization=username)

	return status

VISIBILITY_TESTS = {
	'ALL_METADATA_ACCESS'	 	: ( all_metadata_access, "Access to all channel metadata" ),
	'MOOD_STATUS_ACCESS' 		: ( mood_status_access, "Access to channel mood status" ),
	'POSTS_READ_ACCESS'		: ( posts_read_access, "Read access to channel posts" ),
	'SUBSCRIBERS_ACCESS'		: ( subscribers_access, "Access to channel subscribers list" ),
	'SUBSCRIBED_TO_ACCESS'		: ( subscribed_to_access, "Access to channel outside roles" ),
	'GEOLOC_ACCESS'			: ( geoloc_access, "Access to channel geolocation" )

}

def performVisibilityTests(domain_url, username, expected_results):

	(status, briefing, message, api_location) = findAPILocation(domain_url)
	if status != 0:
		return (status, briefing, message, None)

	actual_results_match_expected_results = {}
	status = 0

	for test in expected_results.keys():

		if not test in VISIBILITY_TESTS:
			continue

		if not test in actual_results_match_expected_results:
			actual_results_match_expected_results[test] = { True : [], False : [] }

		for target_channel_name in expected_results[test].get(True, []):

			if VISIBILITY_TESTS[test][0](api_location, username, target_channel_name):
				actual_results_match_expected_results[test][True].append(target_channel_name)
			else:
				veredict = "%s (%s)" % (target_channel_name, "should have access")
				actual_results_match_expected_results[test][False].append(veredict)
				print veredict
				status = 1

		for target_channel_name in expected_results[test].get(False, []):

			if VISIBILITY_TESTS[test][0](api_location, username, target_channel_name):
				veredict = "%s (%s)" % (target_channel_name, "should not have access")
				print veredict
				actual_results_match_expected_results[test][False].append(veredict)
				status = 1
			else:
				actual_results_match_expected_results[test][True].append(target_channel_name)

	if status == 0:
		partial_report = "Every visibility test had the expected results!<br/>"
		show_problems_only = False
	else:
		partial_report = "Not all visibility tests had the expected results!<br/>"
		show_problems_only = True

	for test in actual_results_match_expected_results.keys():

		if len(actual_results_match_expected_results[test][not show_problems_only]) == 0:
			continue

		partial_report += "<br/><em>%s</em>:<br/><strong>%s</strong>" % (VISIBILITY_TESTS[test][1],
				string.join(actual_results_match_expected_results[test][not show_problems_only], "<br/>"))

	return (status, partial_report)