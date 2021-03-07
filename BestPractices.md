# Coding 

- Always assign variables outside of the code.
- Don't remove/delete data if possible.

# Git
- always pull from master when developing code. The following code changes the local branch to master, then pulls all the files from the remote.
> git checkout master
> git pull

- after that, create a new branch. We will use branch naming in the format of the issue code on Git, such as issue #24 -> branch name = #24
> git checkout -b #XX

- once work is done, commit the changes with a message, then push the changes to the branch.
- make sure to keep the commit messages short and concise.
> git commit -m "commit message"
 
- once all changes are done, push the changes.
> git push --set-upstream origin <branch name>
> git push

- At this point, the user should go to git and submit a pull request for this branch into the main branch for code review.
- Once approved, the branch can be merged into main. 
- Now we can remove the remote and local branches (typically, remote_name = origin)
> git push -d <remote_name> <branch_name>
> git branch -d <branch_name>


