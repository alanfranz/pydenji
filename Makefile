PYTHON=python

bootstrap: .installed.cfg

.installed.cfg:
		$(PYTHON) bootstrap.py --distribute && bin/buildout

clean:
		rm -rf bin eggs develop-eggs parts .installed.cfg _trial_temp build dist *.egg-info
		find . \( -name "*.pyc" -o -name "*.pyo" \) -exec rm -f {} \;

release: clean bootstrap
		bin/testunits || exit 1
		rm setup.cfg
		bin/buildout setup . register sdist upload
		hg revert setup.cfg
