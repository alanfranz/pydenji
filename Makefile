PYTHON=python

.PHONY : buildout clean distclean release test integrationtest

buildout: .installed.cfg

.installed.cfg: bin buildout.cfg
		bin/buildout

bin:
		$(PYTHON) bootstrap.py --distribute

clean:
		rm -rf _trial_temp build dist 
		find . \( -name "*.pyc" -o -name "*.pyo" \) -exec rm -f {} \;

distclean: clean
		rm -rf bin eggs develop-eggs .installed.cfg parts *.egg-info

test: buildout
	bin/testunits

integrationtest: buildout
	bin/integrationtests

release: clean buildout test integrationtest
		[ "" == "`hg status`" ] || ( echo "Working copy must be clean in order to perform a release." ; exit 1 )
		rm -f setup.cfg
		hg tag `$(PYTHON) setup.py --version`
		bin/buildout setup . clean register sdist upload
		hg revert setup.cfg
		echo "Now pull up version string!"
