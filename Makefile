bootstrap: .installed.cfg

.installed.cfg:
		python bootstrap.py --distribute && bin/buildout

clean:
		rm -rf bin eggs develop-eggs parts .installed.cfg _trial_temp src/build src/dist src/*.egg-info
		find . -name "*.pyc" -exec rm -rf {} \;
		find . -name "*.pyo" -exec rm -rf {} \;
