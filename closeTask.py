#!/usr/bin/env python
# encoding: utf-8
#
# Copyright  (c) 2020 Michael Schmidt-Korth
#
# GNU GPL v2.0 Licence. See https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
#
import sys
from main import DEBUG, formatDate
from config import confNames, getConfigValue
from workflow import Workflow, ICON_WEB, ICON_CLOCK, ICON_WARNING, ICON_GROUP, web


def main(wf):
	if len(wf.args):
		query = wf.args[0]
	else:
		query = None
	if query:
		updateTask(query.split('/')[-1])


def updateTask(strTaskId):
	'''Updates an existing Task and sets its status to 'Closed'.

----------
	@param str strTaskId: Id of the Task to update.
	'''
	from workflow.notify import notify
	if DEBUG > 0:
		log.debug('[ Calling API to close task ]')
	wf3 = Workflow()
	url = 'https://api.clickup.com/api/v2/task/' + strTaskId

	headers = {}
	headers['Authorization'] = getConfigValue(confNames['confApi'])
	headers['Content-Type'] = 'application/json'
	data = {}
	data['status'] = 'Closed'
	if DEBUG > 1:
		log.debug(url)
		log.debug(headers)
		log.debug(data)

	try:
		import requests
		request = requests.put(url, json = data, headers = headers)
		request.raise_for_status()
		result = request.json()
		if DEBUG > 1:
			log.debug('Response: ' + str(result))
			notify('Closed Task', result['name'])
	except Exception as exc:
		log.debug('Error on HTTP request:' + str(exc))
		wf3.add_item(title = 'Error connecting to ClickUp.', subtitle = 'Open configuration to check your parameters?', valid = True, arg = 'cu:config ', icon = 'error.png')
		wf3.send_feedback()
		exit()


if __name__ == "__main__":
	wf = Workflow()
	log = wf.logger
	sys.exit(wf.run(main))
