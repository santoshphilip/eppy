.. highlight:: shell

============
Contributing
============

This project uses 
`C4(Collective Code Construction Contract) <https://rfc.zeromq.org/spec:42/C4/>`__ process for contributions



Steps for making updates to the software, based on C4 document above:


- *User*:
    - Opens an issue in issue tracker, describing problem (called issue #n)
- *Contributer*:
    - forks the repository
    - makes changes
    - commits with appropriate commit following message
      ::
      
        fixed issue #n (*on first line*)
        
        Problem: describe Problem
        Solution: describe Solution

    - Make a pull request
- *Maintianer*:
    - Merge pull request into master
- *User*:
    - Closes issue #n in issue tracker

After the merge, The *Contributer* may want to take the following steps:

- *Contributer*: pull the changes from santoshphilip/eppy *Maintainer* has completed the merge
    - This has to be done in the command line
      ::

        git pull --rebase upstream master


    - To do the above you need a remote called `upstream`. You can set this up by the following line in the command line
      ::

        git remote add upstream https://github.com/santoshphilip/eppy.git
        # this needs to be done only once
