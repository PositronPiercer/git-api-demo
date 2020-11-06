import requests
import logging

MAX_RESULTS_PER_PAGE = 100

def comp(repo1, repo2):
    return repo1[1] <= repo2[1]

def getTopContributers(org, repo, n):
    '''
    Returns top n contributors of a given repo based on number of contributions
    '''
    logging.info('Fetching top {} contributors for {}/{}'.format(n, org, repo))
    ans = []
    URL = 'https://api.github.com/repos/{orgName}/{repoName}/contributors'.format(orgName = org, repoName = repo)
    p = {
        'q' : 'contributions',
        'order' : 'desc', # descending order
        'per_page' : min (MAX_RESULTS_PER_PAGE, n),
        'page' : 1
    }
    '''
    GitHub's REST API v3 dosen't allow selecting particular fields. We have to load the whole json and select the required fields.

    '''
    while(n > 0):
        logging.info('Top contributors sending req for page {}'.format(p['page']))
        r = requests.get(url = URL, params = p)
        data = r.json()
        if (r.status_code == 200):
            for user in data:
                ans.append((user['login'], user['contributions']))
   
            if (len(data) < MAX_RESULTS_PER_PAGE or len(data) == n):
                break
            else:
                n = n - len(data)
                p['page'] = p['page'] + 1
                p['per_page'] = min (MAX_RESULTS_PER_PAGE, n)
        else:
            print('Oops! Something unexpected happened. Here is the message from GitHub\'s API')
            print(r.status_code)
            print(r.text)
            exit(1)
    logging.info('Found top {} contributors for {}/{}'.format(n, org, repo))  
    return ans


def getRepos(org):
    '''
    Fetches and returns all repo names and their forks count of the given org
    '''
    URL = 'https://api.github.com/orgs/{orgName}/repos'.format(orgName = org)
    repoList = []
    p = {
        'per_page' : MAX_RESULTS_PER_PAGE,
        'page' : 1
    }
    logging.info('Loading all repos for {}'.format(org))

    '''

    GitHub's REST API v3 dosen't provide sort based on forks. We have to load all repos and sort them

    '''
    while(True):
        logging.info('getRepos sending req for page {}'.format(p['page']))
        r = requests.get(url = URL, params = p)      
        data = r.json()
        if (r.status_code == 200):
            #request successfull
            for repo in data:
                repoList.append((repo['name'], repo['forks']))

            if (len(data) < MAX_RESULTS_PER_PAGE):
                break
            else:
                p['page'] = p['page'] + 1
        else:
            print('Oops! Something unexpected happened. Here is the message from GitHub\'s API')
            print(r.status_code)
            print(r.text)
            exit(1)
    return repoList

def getTopRepos(org, n):
    '''
    Returns Top n repos of the given org based on fork counts
    '''
    repoList = getRepos(org)
    repoList.sort(key = lambda x:x[1], reverse = True)
    return repoList[:n]


