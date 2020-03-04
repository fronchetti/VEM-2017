import matplotlib.pyplot as plot
import crawler
import json
import numpy as np


def read_json_file(file_name):
    with open(file_name) as data_file:
        data = json.load(data_file)
    return data


# # # # # # # # # # # # # # # #
#  Method to collect commits  #
# # # # # # # # # # # # # # # #
# This is an example of how you can collect data using Octopus

def commits_per_pull_request(pull_requests, project_name):
    # This method is responsible for collecting all commits for each
    # pull request. This code was based on a parallel project by the
    # author called Octopus. Visit: github.com/fronchetti/octopus

    dictionary_unpaid = {}
    dictionary_paid = {}
    for pull_request in pull_requests:
        commits_url = pull_request['comments_url']
        pull_request_number = pull_request['number']
        request = ['Waiting...']
        page_number = 1
        number_of_commits = 0

        while(request):
            request = crawler.request(
                commits_url.replace('https://api.github.com/', ''),
                ['page=' + str(page_number)])
            number_of_commits = number_of_commits + len(request)
            page_number += 1

        if 'closed' in pull_request['state'] and pull_request['merged_at'] is not None:
            if pull_request['user']['site_admin'] is True:
                dictionary_paid[pull_request_number] = number_of_commits

            elif pull_request['user']['site_admin'] is False:
                dictionary_unpaid[pull_request_number] = number_of_commits

        with open(project_name + '_comments_unpaid.json', 'w') as unpaid_file:
            json.dump(dictionary_unpaid, unpaid_file)

        with open(project_name + '_comments_paid.json', 'w') as paid_file:
            json.dump(dictionary_paid, paid_file)

        print project_name
        print len(dictionary_paid.items())
        print sorted(dictionary_paid.items(), key=lambda x: x[1])
        print len(dictionary_unpaid.items())
        print sorted(dictionary_unpaid.items(), key=lambda x: x[1])


# # # # # # # # # # # # # # # #
#  Method to create boxplot   #
# # # # # # # # # # # # # # # #

# Single boxplot


def boxplot(values, project_name, group_type):
    plot.figure(figsize=(3, 5))
    medianprops = dict(color='black')
    plot.title(project_name.title())
    boxplot = plot.boxplot(values.values(), showfliers=False,
                           medianprops=medianprops, widths=0.5)
    max_value = [item.get_ydata()[1] for item in boxplot['whiskers']]
    plot.yticks(np.arange(0, max(max_value) + 3, 2))
    plot.ylim(ymin=0)
    plot.legend()
    plot.savefig(project_name + '_' + group_type.lower() +
                 '_boxplot.eps', bbox_inches='tight', pad_inches=0.1)

# Group of boxplot (Similar to that of the article)


def boxplot_group(values, project_name):
    plot.figure(figsize=(3, 5))
    medianprops = dict(color='black')
    plot.title(project_name.title())
    boxplot = plot.boxplot(values, showfliers=False,
                           medianprops=medianprops, widths=0.5)
    max_value = [item.get_ydata()[1] for item in boxplot['whiskers']]
    plot.yticks(np.arange(0, max(max_value) + 3, 2))
    plot.xticks([1, 2], ['Internals', 'Externals'])
    plot.ylim(ymin=0)
    plot.legend()
    plot.savefig(project_name +
                 '_group_boxplot.eps', bbox_inches='tight', pad_inches=0.1)


# Atom - The hackable text editor
# https://github.com/atom/atom
atom_commits_unpaid = read_json_file('JSON/atom_commits_unpaid.json')
atom_commits_paid = read_json_file('JSON/atom_commits_paid.json')
# Hubot - A customizable life embetterment robot.
# https://github.com/github/hubot_paid
hubot_commits_unpaid = read_json_file('JSON/hubot_commits_unpaid.json')
hubot_commits_paid = read_json_file('JSON/hubot_commits_paid.json')

atom_comments_unpaid = read_json_file('JSON/atom_comments_unpaid.json')
atom_comments_paid = read_json_file('JSON/atom_comments_paid.json')
hubot_comments_unpaid = read_json_file('JSON/hubot_comments_unpaid.json')
hubot_comments_paid = read_json_file('JSON/hubot_comments_paid.json')

# Boxplot's
boxplot_group([hubot_commits_paid.values(),
               hubot_commits_unpaid.values()], 'hubot_commits')
boxplot_group([hubot_commits_paid.values(),
               atom_commits_unpaid.values()], 'atom_commits')
boxplot_group([hubot_comments_paid.values(), hubot_comments_unpaid.values()],
              'hubot_comments')
boxplot_group([atom_comments_paid.values(), atom_comments_unpaid.values()],
              'atom_comments')
