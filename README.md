# git-api-demo
Find the n most popular repositories of a given organization on Github (Eg:https://github.com/google) based on the number of forks. For each such repo find the top m committees and their commit counts. 

## setup

* `pip install -r requirements.txt` to install dependencies

## run
* `python main.py -o <org name> -m <number of repos> -n <number of contributors>`
* optional arguments

   * `[-h]` help
   * `[-v]` verbose mode

The result is saved in a file named `<orgName>.txt`
