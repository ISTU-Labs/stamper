.PHONY: help init mysql setup server

help:
	cat Makefile

server:
	pserve --reload development.ini

init:
	initialize_stamper_db development.ini

setup:
	python setup.py develop

mysql:
	mysql -h 172.17.0.2 -u stamper -pstamperpsw
