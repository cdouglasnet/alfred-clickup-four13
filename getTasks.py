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
	getTasks(wf)


def getTasks(wf):
	'''Retrieves a list of Tasks from the ClickUp API.

----------
	'''
	log = wf.logger
	
	# Skip empty queries for search mode to avoid wasteful API calls
	if len(wf.args) > 1 and wf.args[1] == 'search' and (not wf.args[0] or wf.args[0].strip() == ''):
		wf3 = Workflow()
		wf3.add_item(
			title = 'Start typing to search tasks...',
			subtitle = 'Enter at least one character to begin searching',
			valid = False,
			icon = 'icon.png'
		)
		wf3.send_feedback()
		return
	
	# For mode = search: ClickUp does not offer a parameter 'filter_by' - therefore we receive all tasks, and use Alfred/fuzzy to filter.
	if DEBUG > 0:
		log.debug('[ Calling API to list tasks ]')
	url = 'https://api.clickup.com/api/v2/team/' + getConfigValue(confNames['confTeam']) + '/task'
	params = {}
	wf3 = Workflow()

	# Use searchScope, default to 'auto' if not configured
	search_scope = getConfigValue(confNames['confSearchScope']) or 'auto'
	
	if search_scope == 'list':
		params['list_ids[]'] = getConfigValue(confNames['confList'])
	elif search_scope == 'folder':
		params['project_ids[]'] = getConfigValue(confNames['confProject'])
	elif search_scope == 'space':
		params['space_ids[]'] = getConfigValue(confNames['confSpace'])
	elif search_scope == 'auto':
		# Auto mode: start with list scope
		params['list_ids[]'] = getConfigValue(confNames['confList'])
	params['order_by'] = 'due_date'
	# ClickUp API will return up to 100 tasks per page (their maximum)
	params['page'] = 0
	
	# Differentiates between listing all Alfred-created tasks and searching for all tasks (any)
	if DEBUG > 0 and len(wf.args) > 1 and wf.args[1] == 'search':
		log.debug('[ Mode: Search (cus) ]')
		# Add search query if provided
		if len(wf.args) > 0 and wf.args[0]:
			params['query'] = wf.args[0]
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
	except Exception as e:
		log.debug('Error on HTTP request: ' + str(e))
		wf3.add_item(title = 'Error connecting to ClickUp.', subtitle = 'Open configuration to check your parameters?', valid = True, arg = 'cu:config ', icon = 'error.png')
		wf3.send_feedback()
		exit()
	
	try:
		result = request.json()
		if DEBUG > 1:
			log.debug('Response received with %d tasks (ClickUp max: 100 per page)' % len(result.get('tasks', [])))
	except Exception as e:
		log.debug('Error parsing JSON response: ' + str(e))
		wf3.add_item(title = 'Error parsing ClickUp response.', subtitle = 'The response may be too large. Try a more specific search.', valid = False, icon = 'error.png')
		wf3.send_feedback()
		exit()

	# Check if response has tasks
	if 'tasks' not in result:
		log.debug('No tasks key in response: ' + str(result.keys()))
		wf3.add_item(title = 'No tasks found.', subtitle = 'Try a different search query.', valid = False, icon = 'note.png')
		wf3.send_feedback()
		exit()
	
	# Auto mode expansion logic - accumulate results from all levels
	if search_scope == 'auto' and len(wf.args) > 1 and wf.args[1] == 'search':
		all_tasks = list(result.get('tasks', []))  # Start with list-level tasks
		task_ids = {task['id'] for task in all_tasks}  # Track IDs to avoid duplicates
		
		if DEBUG > 0:
			log.debug('Auto mode: Got %d tasks at list level' % len(all_tasks))
		
		# Always try folder level to get more results
		if getConfigValue(confNames['confProject']):
			if DEBUG > 0:
				log.debug('Auto mode: Expanding to folder level')
			# Remove list constraint, add folder constraint
			temp_params = params.copy()
			if 'list_ids[]' in temp_params:
				del temp_params['list_ids[]']
			temp_params['project_ids[]'] = getConfigValue(confNames['confProject'])
			
			# Make another API call
			try:
				request = web.get(url, params = temp_params, headers = headers)
				request.raise_for_status()
				folder_result = request.json()
				
				# Add new tasks (avoid duplicates)
				for task in folder_result.get('tasks', []):
					if task['id'] not in task_ids:
						all_tasks.append(task)
						task_ids.add(task['id'])
				
				if DEBUG > 0:
					log.debug('Auto mode: Total %d tasks after folder level' % len(all_tasks))
			except Exception as e:
				if DEBUG > 0:
					log.debug('Auto mode folder expansion failed: %s' % str(e))
		
		# If we still don't have many results, try space level
		if len(all_tasks) < 50 and getConfigValue(confNames['confSpace']):
			if DEBUG > 0:
				log.debug('Auto mode: Expanding to space level')
			# Remove folder constraint, add space constraint
			temp_params = params.copy()
			if 'list_ids[]' in temp_params:
				del temp_params['list_ids[]']
			if 'project_ids[]' in temp_params:
				del temp_params['project_ids[]']
			temp_params['space_ids[]'] = getConfigValue(confNames['confSpace'])
			
			# Make another API call
			try:
				request = web.get(url, params = temp_params, headers = headers)
				request.raise_for_status()
				space_result = request.json()
				
				# Add new tasks (avoid duplicates)
				for task in space_result.get('tasks', []):
					if task['id'] not in task_ids:
						all_tasks.append(task)
						task_ids.add(task['id'])
				
				if DEBUG > 0:
					log.debug('Auto mode: Total %d tasks after space level' % len(all_tasks))
			except Exception as e:
				if DEBUG > 0:
					log.debug('Auto mode space expansion failed: %s' % str(e))
		
		# Replace result with accumulated tasks
		result['tasks'] = all_tasks

	for task in result['tasks']:
		tags = ''
		if task.get('tags'):
			for allTaskTags in task.get('tags', []):
				tags += allTaskTags.get('name', '') + ' '

		subtitle_parts = []
		if task.get('due_date'):
			subtitle_parts.append(emoji.emojize(':calendar:') + str(datetime.datetime.fromtimestamp(int(task.get('due_date'))/1000)))
		if task.get('priority'):
			priority_info = task.get('priority', {})
			if priority_info.get('priority'):
				subtitle_parts.append(emoji.emojize(':exclamation_mark:') + priority_info['priority'].title())
		if task.get('tags') and tags.strip():
			subtitle_parts.append(emoji.emojize(':label:') + tags.strip())
		
		# Safe access to required fields with defaults
		status_text = task.get('status', {}).get('status', 'Unknown')
		task_name = task.get('name', 'Untitled Task')
		task_url = task.get('url', '')
		
		wf3.add_item(
			title = '[' + status_text + '] ' + task_name,
			subtitle = ' '.join(subtitle_parts) if subtitle_parts else 'No additional details',
			match = task_name,  # Use just the task name for fuzzy matching
			valid = True,
			arg = task_url
		)
	wf3.send_feedback()


if __name__ == "__main__":
	wf = Workflow()
	log = wf.logger
	sys.exit(wf.run(main))
