# Git Stalk
[![Code Health](https://landscape.io/github/zebde/git-stalk/master/landscape.svg?style=flat)](https://landscape.io/github/zebde/git-stalk/master)

The git-stalk script scrapes identities from git repositories. It can perform offline analysis on repositories that are already stored on disk, or it can clone all repositories from a single GitHub user/organisation.


Currently the following is returned as JSON:

```json
[
    {
        "user": "Bob Bobbington",
        "email": "bob@gmail.com"
    },
    {
        "user": "Helen Helensworth",
        "email": "helen@gmail.com"
    },
    {
        "user": "Fred Fredington",
        "email": "fred@gmail.com"
    },
    {
        "user": "Alice Aliceton",
        "email": "alice@gmail.com"
    }
  ]
```


## Dependencies
The script is compatible with both Python 2.7 and 3.x The following python libraries are required and can be installed with pip.
- gitpython
- requests


### Installation of dependecies
```
sudo pip install -r requirements.txt
```

## License
See the [LICENSE](LICENSE.md) file for license rights and limitations (GPLv3).
