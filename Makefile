PYTHON=python

.PHONY : buildout clean distclean release 

buildout: .installed.cfg

.installed.cfg: bin buildout.cfg
		bin/buildout

bin:
		$(PYTHON) bootstrap.py --distribute

clean:
		rm -rf _trial_temp build dist *.egg-info
		find . \( -name "*.pyc" -o -name "*.pyo" \) -exec rm -f {} \;

distclean: clean
		rm -rf bin eggs develop-eggs .installed.cfg parts

VER=$(shell $(PYTHON) get_hg_version.py)
release: clean buildout
		# [ "" == "`hg status`" ] || ( echo "Working copy must be clean in order to perform a release." ; exit 1 )
		bin/testunits 
		bin/integrationtests
		sed -i.old -e "s/REPLACE_WITH_VERSION/\"$(VER)\"/g" setup.py
		hg commit -m "Version setup for $(VER)" setup.py
		hg tag v$(VER)
		bin/buildout setup . clean sdist
		cp setup.py.old setup.py
		hg commit -m "Restore non-release setup.py file."
		rm setup.py.old



