devel:

	echo "clone libs"

	@if ! [ -d libs/most ]; then git clone https://github.com/crs4/most libs/most -b develop; fi

	echo "link libs"

	cd src/most/web ; ln -s ../../../libs/most/src/most/web/utils utils; ln -s ../../../libs/most/src/most/web/users users ; \
	ln -s ../../../libs/most/src/most/web/authentication authentication; 

	echo "copy settings to examples"
	@if ! [ -d examples/most/main/settings.py ]; then cp examples/most/main/settings.py.conf examples/most/main/settings.py; fi
	
clean:

	echo "clean devel mode"
	
	@if [[ `git -C libs/most status --porcelain` ]]; then \
			echo "CHANGES - most repository not removed"; \
		else \
			echo "NO CHANGES - remove most repository"; \
			rm -fr libs/most; \
			rm -f server/most/web/utils; \
			rm -f server/most/web/users; \
			rm -f server/most/web/authentication; \
	fi

run:

	cd examples/most; PYTHONPATH=.. python manage.py runserver 0.0.0.0:8000


shell: 

	cd examples/most; PYTHONPATH=.. python manage.py shell

sync:

	cd examples/most; PYTHONPATH=.. python manage.py migrate
