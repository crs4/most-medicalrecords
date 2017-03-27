devel:

	echo "clone libs"

	@if ! [ -d libs/most ]; then git clone https://github.com/crs4/most libs/most -b develop; fi

	echo "link libs"

	cd src/most/web ; ln -fs ../../../libs/most/src/most/web/utils utils; ln -fs ../../../libs/most/src/most/web/users users ; \
	ln -fs ../../../libs/most/src/most/web/authentication authentication;

	cd examples; ln -fs ../libs/most/src/provider provider;

	echo "copy settings to examples"
	@if ! [ -d examples/most/main/settings.py ]; then cp examples/most/main/settings.py.conf examples/most/main/settings.py; fi
	
clean:

	echo "clean devel mode"

	@if [ `git -C libs/most status --porcelain` ]; then \
		echo "CHANGES - most repository not removed"; \
	else \
		echo "NO CHANGES - remove most repository"; \
		rm -fr libs/most; \
		rm -f src/most/web/utils; \
		rm -f src/most/web/users; \
		rm -f src/most/web/authentication; \
	fi

run:

	cd examples/most; PYTHONPATH=.. python manage.py runserver 0.0.0.0:9000


shell: 

	cd examples/most; PYTHONPATH=.. python manage.py shell

sync:

	cd examples/most; PYTHONPATH=.. python manage.py migrate

dump:
	@cd examples/most; PYTHONPATH=.. python manage.py dumpdata --exclude contenttypes --exclude auth --exclude sessions --exclude admin --natural-foreign

test:

	cd src/most/web/medicalrecords/; nosetests --logging-level=DEBUG -s
