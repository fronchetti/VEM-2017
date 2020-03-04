#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import collections
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime


# # # # # # # # # # # # # # # #
#       Other methods         #
# # # # # # # # # # # # # # # #


def read_json_file(file_name):
    # This method reads JSON files.
    with open(file_name) as data_file:
        data = json.load(data_file)
    return data


def pull_requests_monthly_frequency(pull_requests):
    # This method returns the monthly distribution of pull requests for each
    # project.
    monthly_frequency = collections.OrderedDict()

    for pull_request in pull_requests:
        # We set a standard day for each month, because our goal is not to
        # see a daily distribution of pull requests.
        date = datetime.strptime(
            pull_request['created_at'],
            '%Y-%m-%dT%H:%M:%SZ').date().replace(day=15)

        if date not in monthly_frequency:
            monthly_frequency[date] = 1
        else:
            monthly_frequency[date] = monthly_frequency[date] + 1

    return monthly_frequency

# # # # # # # # # # # # # # # #
#  Methods to generate charts #
# # # # # # # # # # # # # # # #


def open_pull_requests(pull_requests, project_name):
    # This method generates an open pull requests chart
    # As a first step, we split the pull requests between Externals and
    # Internals, and we generate the monthly distribution for each list.
    paid_contributors_pull_requests = []
    unpaid_contributors_pull_requests = []

    for pull_request in pull_requests:
        if 'open' in pull_request['state']:
            if pull_request['user']['site_admin'] is True:
                paid_contributors_pull_requests.append(pull_request)
            elif pull_request['user']['site_admin'] is False:
                unpaid_contributors_pull_requests.append(pull_request)

    monthly_frequency_unpaid = pull_requests_monthly_frequency(
        unpaid_contributors_pull_requests)
    monthly_frequency_paid = pull_requests_monthly_frequency(
        paid_contributors_pull_requests)

    # The code below is responsible for generating the chart.
    # Visit the Matplotlib¹ page for more information.
    # ¹ https://matplotlib.org/index.html
    fig, ax = plt.subplots()
    plt.title(project_name.title())
    plt.xlabel(u'Years')
    plt.ylabel(u'# Open PRs')
    ax.plot(monthly_frequency_unpaid.keys(), monthly_frequency_unpaid.values(),
            'o-', linewidth=2, label=u'Externals')
    ax.plot(monthly_frequency_paid.keys(), monthly_frequency_paid.values(),
            'o--', linewidth=2, label=u'Internals')
    # Additional settings
    ax.legend(handlelength=4)
    ax.xaxis.set_minor_locator(mdates.YearLocator())
    ax.set_ylim(ymin=0)
    plt.xticks([datetime(2015, 1, 1), datetime(
        2016, 1, 1), datetime(2017, 1, 1), datetime(2018, 1, 1)])
    plt.yticks(np.arange(0, 71, 10))
    plt.savefig(project_name + '_open.eps', bbox_inches='tight')


def closed_pull_requests(pull_requests, project_name):
    # This method generates an closed pull requests chart
    # As a first step, we split the pull requests between Externals and
    # Internals, and we generate the monthly distribution for each list.
    paid_contributors_pull_requests = []
    unpaid_contributors_pull_requests = []

    for pull_request in pull_requests:
        if 'closed' in pull_request['state'] and pull_request['merged_at'] is None:
            if pull_request['user']['site_admin'] is True:
                paid_contributors_pull_requests.append(pull_request)
            elif pull_request['user']['site_admin'] is False:
                unpaid_contributors_pull_requests.append(pull_request)

    monthly_frequency_unpaid = pull_requests_monthly_frequency(
        unpaid_contributors_pull_requests)
    monthly_frequency_paid = pull_requests_monthly_frequency(
        paid_contributors_pull_requests)

    # The code below is responsible for generating the chart.
    # Visit the Matplotlib¹ page for more information.
    # ¹ https://matplotlib.org/index.html
    fig, ax = plt.subplots()
    plt.xlabel(u'Years')
    plt.ylabel(u'# Closed PRs')
    plt.title(project_name.title())
    ax.plot(monthly_frequency_unpaid.keys(), monthly_frequency_unpaid.values(),
            'o-', linewidth=2, label=u'Externals')
    ax.plot(monthly_frequency_paid.keys(), monthly_frequency_paid.values(),
            'o--', linewidth=2, label=u'Internals')
    # Additional settings
    ax.legend(handlelength=4)
    ax.set_ylim(ymin=0)
    plt.xticks([
        datetime(2012, 1, 1), datetime(2013, 1, 1), datetime(2014, 1, 1),
        datetime(2015, 1, 1), datetime(2016, 1, 1), datetime(2017, 1, 1),
        datetime(2018, 1, 1)])
    plt.yticks(np.arange(0, 71, 10))
    # Save the image
    plt.savefig(project_name + '_closed.eps', bbox_inches='tight')


def merged_pull_requests(pull_requests, project_name):
    # This method generates an merged pull requests chart
    # As a first step, we split the pull requests between Externals and
    # Internals, and we generate the monthly distribution for each list.
    paid_contributors_pull_requests = []
    unpaid_contributors_pull_requests = []

    for pull_request in pull_requests:
        if 'closed' in pull_request['state'] and pull_request['merged_at'] is not None:
            if pull_request['user']['site_admin'] is True:
                paid_contributors_pull_requests.append(pull_request)
            elif pull_request['user']['site_admin'] is False:
                unpaid_contributors_pull_requests.append(pull_request)

    monthly_frequency_unpaid = pull_requests_monthly_frequency(
        unpaid_contributors_pull_requests)
    monthly_frequency_paid = pull_requests_monthly_frequency(
        paid_contributors_pull_requests)

    # The code below is responsible for generating the chart.
    # Visit the Matplotlib¹ page for more information.
    # ¹ https://matplotlib.org/index.html
    fig, ax = plt.subplots()
    plt.title(project_name.title())
    plt.xlabel(u'Years')
    plt.ylabel(u'# Accepted PRs')
    ax.plot(monthly_frequency_unpaid.keys(), monthly_frequency_unpaid.values(),
            'o-', linewidth=2, label=u'Externals')
    ax.plot(monthly_frequency_paid.keys(), monthly_frequency_paid.values(),
            'o--', linewidth=2, label=u'Internals')
    # Additional settings
    ax.legend(handlelength=4)
    ax.set_ylim(ymin=0)
    plt.xticks([datetime(2011, 1, 1), datetime(2012, 1, 1),
                datetime(2013, 1, 1), datetime(2014, 1, 1),
                datetime(2015, 1, 1), datetime(2016, 1, 1),
                datetime(2017, 1, 1), datetime(2018, 1, 1)])
    plt.yticks(np.arange(0, 71, 10))
    # Save the image
    plt.savefig(project_name + '_merged.eps', bbox_inches='tight')


# Atom - The hackable text editor
# https://github.com/atom/atom
atom_pull_requests = read_json_file('JSON/atom_pulls.json')

# Hubot - A customizable life embetterment robot.
# https://github.com/github/hubot
hubot_pull_requests = read_json_file('JSON/hubot_pulls.json')

open_pull_requests(atom_pull_requests, 'atom')
open_pull_requests(hubot_pull_requests, 'hubot')
closed_pull_requests(atom_pull_requests, 'atom')
closed_pull_requests(hubot_pull_requests, 'hubot')
merged_pull_requests(atom_pull_requests, 'atom')
merged_pull_requests(hubot_pull_requests, 'hubot')
