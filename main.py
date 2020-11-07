from utilities import getTopContributers, getTopRepos
import argparse


def main():
    parser = argparse.ArgumentParser(description = "GitHub API Demo. Find the n most popular repositories of a given organization on Github based on the number of forks. For each such repo find the top m committees and their commit counts.")
    parser.add_argument ('-o', '--org', help = 'org name', required = True)
    parser.add_argument ('-n', help = 'max number of top repos to load', required = True)
    parser.add_argument ('-m', help = 'max number of top contributors to load', required = True)

    args = parser.parse_args()

    orgName = str(args.org)
    m = int(args.m)
    n = int(args.n)

    with open(orgName + '.txt', mode = 'w') as outFile:
        outFile.write(orgName + '\n')
        #get top m repos
        topRepos = getTopRepos (orgName, m)

        for repo in topRepos:
            repoName = repo[0]
            forkCount = repo[1]

            outFile.write(repoName + "\t" + str(forkCount)  + '\n')
            #get top n contributors
            topContributors = getTopContributers(orgName, repoName, n)

            for contributor in topContributors:
                outFile.write("\t" + contributor[0] + "\t" + str(contributor[1])  + '\n')

    



if __name__ == '__main__':
    main()