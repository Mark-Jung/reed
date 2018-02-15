# reed
Powers the app, &lt;insert name here/>
# Required downloads
xcode(front-end), brew, pip, virtualenv,
# Steps to setup
1. Setup Git
2. Download Python 3.6
3. Clone this repo by "git clone https://github.com/Mark-Jung/reed.git"
4. Navigate to the repo - cd: stands for change directory. It's used to switch between directories(folders). ls: lists all files and directories in current directory
5. Download virtualenv through pip. 'pip virtualenv'
6. On your commandline, write: virtualenv env --python=python3.6
7. On your commandline, write: source env/bin/activate
8. Try typing 'python', and if you can see that it's python version 3.6, you're good to go.
9. On your commandline, write: pip install -r requirements.txt
10. Ask mark for his secret env variable
11. run 'nose2' and see if all of the tests pass. If any doen't pass, alert mark IMMEDIATELY. 

# Steps to do before running server
1. git pull origin master
2. source env/bin/activate
3. export SECRET='<what i told you in the facebook messenger>'
4. nose2 (if any errors come up, notify mark)
5. python app.py
