# User Guide
![Shrek](static/shrek-dancing.gif)

The aptly named _Cringe Lord_ is our configuration management tool. Its
goal is to load configuration settings from various sources so our 
applications can conveniently use them. This way of working improves both the 
maintainability and security of our applications. 

_Cringe Lord_ is a CLI tool that helps you separate configuration 
from implementation. Running the tool loads your application's settings 
into the environment by looking for their values in your configuration file. You 
do not have to specify which settings you require, as _Cringe Lord_ will parse 
your application's source code to infer which ones you need.

## Installation
You can find Cringe Lord's binaries in [Cringe Lord's Package Repository on 
our GitLab](https://gitlab.cegeka.com/api/v4/projects/869/packages/pypi).

The repository's access token is stored in [PIM](https://pim.cegeka.com/SecretServer/app/#/secrets/198979/general).


### Pip
You can manually install cringelord through `pip`:
```shell
pip install cringelord --index-url https://__token__:<access_token>@gitlab.cegeka.com/api/v4/projects/869/packages/pypi/simple
```

Or add it to your `requirements.txt`:
```shell
--extra-index-url https://__token__:<access_token>@gitlab.cegeka.com/api/v4/projects/869/packages/pypi/simple
cringelord==<version_number>

```

### Pipenv
Add Cringe Lord's Package Repository on GitLab to your `Pipfile` as a source:
```shell
[[source]]
url = "https://__token__:<access_token>@gitlab.cegeka.com/api/v4/projects/869/packages/pypi/simple"
verify_ssl = false
name = "<source_name>"
```
You can now use it for the `cringelord` package in your `Pipfile`:
```shell
[packages]
cringelord = {version="<version_number>", index = "<source_name>"}
```


## Usage
### Documentation
_Cringe Lord_ is a CLI tool you can use via the `cringelord` command. The tool 
will definitely change over time, so we advise using the --help option when 
inquiring about the options and arguments:
```shell
cringelord --help
```

### Example
```shell
cringelord development
```
The above code will load the settings your application requires from the 
`cringe-config.yaml` file. Your application should be located in the current 
working directory, and this directory should contain the `cringe-config.yaml` 
file in its root. 

If you want to use a different configuration file or application directory, 
you have to specify them using options:
```shell
cringelord -c my-config.yaml -d app/ development
```
or
```shell
cringelord --config my-config.yaml --app-dir app/ development
```


### Timing
Always run `cringelord` before running your application (locally, on Jenkins,
etc.), because it will make sure your application has all of its required 
environment variables present in the environment. 

## Setup
_Cringe Lord_ requires you to have a `.yaml` configuration file with the values
of the environment variables your script requirements. By default (i.e., when 
you don't specify a configuration file), `cringelord` will look for a 
`cringe-config.yaml` file in the current working directory. 

### cringe-config.yaml
`cringe-config.yaml` is the file that contains all the configuration settings 
that your application requires. 

Let's take a look at an example:
```yaml
metadata:
  author: Thomas Vanhelden
  company: Cegeka
  
environments:
  prd:
    name: Production
    description: Production environment.
    aliases:
      - prd
      - prod
      - production
    settings:
      database_pim_id: 12345
      driver:
        name: pyodbc
        spec: Microsoft ODBC Version 18
      users_names:
        - secuser_usd12_prd
        - soc_srvc_prd
  acc:
    name: Acceptance environment
    description: Acceptance environment for testing.
    aliases:
      - acc
      - test
      - acceptance
      - dev
    settings:
      database_pim_id: 67890
      driver:
        name: pyodbc
        spec: Microsoft ODBC Version 17
      users_names:
        - secuser_usd12_acc
        - soc_srvc_acc

pim_service_account:
  location: jenkins
  name: pim_api
  username: soc_srvc_jenkins
```
The structure of this file is very forgiving, and only requires the 
`environments` top-level key to be present. Here, `cringelord` will look for
environment-specific settings. Other top-level keys will be regarded as 
settings that are valid for all environments.

#### Settings
Environment-specific settings have to be specified under the environment's 
`settings` key, and have to be individual key-value pairs. 

Settings can be anything you like, as long as their values are serializable. 
This includes strings, dictionaries, lists, etc. However, don't forget to 
de-serialize the values you get from the environment variables (i.e., using 
`json.loads(<env_var_value>)`)

### Environments
Environments don't require a name, description or aliases, but it is advised 
to do so. This is because it makes the configuration more human-readable, and 
`cringelord` looks in both the key, name, and aliases to find the correct 
environment. With the above example, if the user of `cringelord` wants to run 
it for the "Production" environment, he can provide the following values:
1. prd
2. prod
3. production
4. PRodUcTioN
5. etc.

This is done to make the tool's usage more fault-tolerant.

## Developer Documentation
### Source Code
You can find all source code in the `cringe_lord` package. 

### Commandline API
The commandline API is defined in `cringe_lord/api/api.py`. This module only 
contains code related to the interface, and does not contain any logic. 

### Logic
The high-level logic is defined in the `cringe_lord/app.py` module, while the 
lower-level logic is contained in utility modules in the `cringe_lord/util` 
package. Here we have two modules `config_parser.py` and `env_call_finder.py`. 

#### Config Parser
The `ConfigParser` class is responsible for parsing a configuration file. It 
will determine which settings are related to which environments, and it can 
parse the environment structure. 

When you have a set of settings for which you require the values, you can use 
the `get_settings` object of your `ConfigParser` object. 

#### Env Call Finder
The `env_call_finder.py` module exposes the `find_env_call_vars` function that 
detects all environment variable usages in the directory you provide. It will 
recursively walk through the given directory (current working directory, by 
default) and look for `getenv` statements in all Python files. 



