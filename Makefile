PYTHON=python

bootstrap: .installed.cfg

.installed.cfg:
		$(PYTHON) bootstrap.py --distribute && bin/buildout

clean:
		rm -rf bin eggs develop-eggs parts .installed.cfg _trial_temp pydenji/build pydenji/dist pydenji/*.egg-info
		find . -name "*.pyc" -o -name "*.pyo" -exec rm -f {} \;
