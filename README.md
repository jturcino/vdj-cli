vdj-cli 
=======

Python cli tools for VDJServer, made using [AgavePy](https://github.com/TACC/agavepy).

Installation using GitHub
-------------------------

```
$ git init
$ git pull https://github.com/jturcino/vdj-cli.git
```

Set Up
------

First, enable bash completion.
```
$ source vdj-completion.bash
```

Now, pull a token to access VDJServer. This requires an account, which can be created through the [website](https://vdjserver.org/). The -s flag caches the token in a file (~/.vdjapi); if you do not want to save the token for future use, simply leave off this flag.
```
$ vdj login -s -u myusername
```

Usage
-----

A valid access token is required to use any of the commands in this CLI. Once you have cached an access token the first time, you may refresh expired access tokens using your cache:
```
$ vdj login -r -s
```
If you prefer to not cache your access token, you must manually pass an access token to each command you run via the `-z` flag.


Project creation and deletion is currently not supported in this CLI; however, projects may be listed at any time with:
```
$ vdj projects
```


In general, anything you do to a projectFile can be done to a projectJobFile by switching the `-f` f
lag to `-j`. The exception to this rule is file uploads and imports, which can only be uploaded as projectFiles. For example, all of a project's files, its projectFiles, and its projectJobFiles, respectively can be listed by:
```
$ vdj files ls -p myproject
$ vdj files ls -p myproject -f
$ vdj files ls -p myproject -j
```


The commands that distinguish between projectFiles and projectJobFiles are as follows:
```
$ vdj files download
$ vdj files rm
$ vdj files ls
$ vdj files cp
$ vdj files history
$ vdj files mv
$ vdj files rename
$ vdj files pems ls
$ vdj files pems update
$ vdj files pems rm
```
Use the `-h` flag with each command to see an explanation of their usage and function.


To upload or import a file such that it is visible on <vdjserver.org>, use:
```
$ vdj files upload -p myproject -f myfile
$ vdj files import -p myproject -u importURL
```


A set of commands for apps, jobs, metadata, notifications, postits, profiles, and systems is also included. To see the set of commands for each of these, do one of the following and hit tab three times:
```
$ vdj apps 
$ vdj jobs
$ vdj metadata
$ vdj notifications
$ vdj postits
$ vdj profiles
$ vdj systems
```


Additionally, there is a set of nonspecific files commands not supported by bash complete. These commands are distinguishable from vdj-specific commands in their naming structure. vdj-specific commands are named vdj-files-\*, while nonspecific commands are named files-\*. These commands do not update metadata, which means their effects will not be visible on <vdjserver.org>. In short, use these with caution!
