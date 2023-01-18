.PHONY: setup clean

setup: setup_client setup_server

setup_client:
	make -C client/ setup

setup_server:
	make -C server/ setup

run_client:
	make -C client/ run

run_server:
	make -C server/ run

clean:
	-rm -f ./*/__pycache__/*

uninstall:
	make -C client/ uninstall
	make -C server/ uninstall