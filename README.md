HOW TO SET UP THE PROJECT (UPDATED)

Prerequisites:
Please make sure to have python (Version 3.7.4) installed. It it highly
recommended to use pyenv.


Please delete the current roombooking folder that you have on your local
machine and create a new one by following these steps:

1) So the folder roombooking is deleted now. In the Terminal move into the
directory where you want to create the new project folder.

2) Then go to GitLab and copy the SSH-link (you find this by clicking on the
  button 'clone' in GitLab)

3) Go back in the terminal and execute the following command: git clone <copied-SSH-link>

4) Test if the project folder has been created. So in the terminal execute the
following command: ls
You should have the folder roombooking there now.

5) Move into that folder: cd roombooking

6) Run the following command to create the virtual environment: python -m venv venv

7) Activate your virtual environment: source venv/bin/activate

8) Install the packages from requirements.txt: pip install -r requirements.txt

9) Check if the installation worked with the following command: pip list

There should be several packages installed, one of them is Django.

10) To deactivate the virtual environment execute the following command in the terminal:
deactivate


Important Links:

https://simpleisbetterthancomplex.com/tutorial/2018/01/18/how-to-implement-multiple-user-types-with-django.html


USING GIT:

git stash save -u    # save local changes locally
git stash apply      # get local changes back

git checkout -b feature_branch_name    # Create a new branch

git push -u origin feature_branch_name    # Push your branch to the remote repository (first push)
vgl. https://www.freecodecamp.org/forum/t/push-a-new-local-branch-to-a-remote-git-repository-and-track-it-too/13222
