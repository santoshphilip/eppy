
Notes for release of a new version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

see:

https://x.com/i/grok/share/5c670016b2b44c8e89da2c95fa26b1c9

1. Prepare
----------

- Assume you are working in the branch ``issue_branch``. 
- You have made changes to fix the issue
- Commits with appropriate commit message
  ::
  
    fixed issue #n (*on first line*)
    
    Problem: describe Problem
    Solution: describe Solution


- Update HISTORY.rst with the changes for the new release




::

    git checkout master
    git pull origin master
    merge issue_branch master


::

    # Run tests
    uv run pytest
    # (optional) uv run flake8 eppy tests

2. Bump the version
-------------------

::

    uv version --bump patch          # patch/minor/major
    # or: uv version 0.6.7
    uv lock

3. Commit
---------

::

    git add .
    git commit -m "Release 0.6.7"

4. Tag and push
---------------

::

    git tag 0.6.7
    git push origin master
    git push origin 0.6.7

5. Build
--------

::

    rm -rf dist/ build/          # optional clean
    uv build

6. Publish to PyPI
------------------

create a token for eppy on https://pypi.org/manage/project/eppy/settings/

::

    export UV_PUBLISH_TOKEN=pypi-...your-token...
    uv publish

7. Create the GitHub Release
----------------------------

With GitHub CLI::

gh release create 0.6.7 --title "0.6.7" --notes-file HISTORY.rst

8. Read the Docs
----------------

The new tag 0.6.7 appears in the Versions list on your Read the Docs project.


