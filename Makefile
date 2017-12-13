test:
	mkdir -p .pyATS
	docker run -it --rm -v $(PWD):/tests ciscotestautomation/pyats bash /tests/run_tests.sh
