test:
	mkdir -p .pyATS
	docker run -it -e PYATS_USERNAME -e PYATS_PASSWORD -e PYATS_AUTH_PASS --rm -v $(PWD):/tests ciscotestautomation/pyats bash /tests/run_tests.sh
