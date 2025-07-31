#!/usr/bin/env python
# encoding: utf-8
#
# Copyright  (c) 2020 Michael Schmidt-Korth
#
# GNU GPL v2.0 Licence. See https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
#
import sys
import datetime
import emoji
from main import DEBUG
from workflow import Workflow, ICON_WEB, ICON_CLOCK, ICON_WARNING, ICON_GROUP, web
from config import confNames, getConfigValue


def main(wf):
	getTasks()


def getTasks():
	'''Retrieves a list of Tasks from the ClickUp API.

----------
	'''
	# For mode = search: ClickUp does not offer a parameter 'filter_by' - therefore we receive all tasks, and use Alfred/fuzzy to filter.
	if DEBUG > 0:
		log.debug('[ Calling API to list tasks ]')
	url = 'https://api.clickup.com/api/v2/team/' + getConfigValue(confNames['confTeam']) + '/task'
	params = {}
	wf3 = Workflow()

	if getConfigValue(confNames['confHierarchyLimit']):
		if 'space' in getConfigValue(confNames['confHierarchyLimit']):
			params['space_ids[]'] = getConfigValue(confNames['confSpace']) # Use [] instead of %5B%5D
		if 'folder' in getConfigValue(confNames['confHierarchyLimit']):
			params['project_ids[]'] = getConfigValue(confNames['confProject'])
		if 'list' in getConfigValue(confNames['confHierarchyLimit']):
			params['list_ids[]'] = getConfigValue(confNames['confList'])
	params['order_by'] = 'due_date'
	# Differentiates between listing all Alfred-created tasks and searching for all tasks (any)
	if DEBUG > 0 and len(wf.args) > 1 and wf.args[1] == 'search':
		log.debug('[ Mode: Search (cus) ]')
	elif DEBUG > 0 and len(wf.args) > 1 and wf.args[1] == 'open':
		log.debug('[ Mode: Open tasks (cuo) ]')
		# from datetime import date, datetime, timezone, timedelta

		today = datetime.date.today()
		todayEndOfDay = datetime.datetime(today.year, today.month, today.day, 23, 59, 59)
		epoch = datetime.datetime(1970, 1, 1)
		todayEndOfDayMs = int((todayEndOfDay - epoch).total_seconds() / datetime.timedelta(microseconds = 1).total_seconds() / 1000)

		params['due_date_lt'] = todayEndOfDayMs
	else:
		log.debug('[ Mode: List tasks (cul) ]')
		defaultTag = getConfigValue(confNames['confDefaultTag'])
		if not defaultTag:
			wf3.add_item(
				title = 'No default tag configured',
				subtitle = 'Use "cu:config" to set a default tag before using this command',
				valid = False,
				icon = 'error.png'
			)
			wf3.send_feedback()
			exit()
		params['tags[]'] = defaultTag
	headers = {}
	headers['Authorization'] = getConfigValue(confNames['confApi'])
	headers['Content-Type'] = 'application/json'
	if DEBUG > 1:
		log.debug(url)
		log.debug(headers)
		log.debug(params)
	try:
		request = web.get(url, params = params, headers = headers)
		request.raise_for_status()
	except:
		log.debug('Error on HTTP request')
		wf3.add_item(title = 'Error connecting to ClickUp.', subtitle = 'Open configuration to check your parameters?', valid = True, arg = 'cu:config ', icon = 'error.png')
		wf3.send_feedback()
		exit()
	result = request.json()
	if DEBUG > 1:
		log.debug('Response: ' + str(result))

	for task in result['tasks']:
		tags = ''
		if task['tags']:
			for allTaskTags in task['tags']:
				tags += allTaskTags['name'] + ' '

		wf3.add_item(
			title = '[' + task['status']['status'] + '] ' + task['name'],
			subtitle = (emoji.emojize(':calendar:') + \
                str(datetime.datetime.fromtimestamp(int(task['due_date'])/1000)) if task['due_date'] else '') + (emoji.emojize(
			':exclamation_mark:') + task['priority']['priority'].title() if task['priority'] else '') + (' ' + emoji.emojize(':label:') + tags if task['tags'] else ''),
			valid = True,
			arg = task['url']
		)
	wf3.send_feedback()


if __name__ == "__main__":
	wf = Workflow()
	log = wf.logger
	sys.exit(wf.run(main))
