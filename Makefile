install:
	pipenv install
    
run:
	pipenv run robot \
		--pythonpath robotdebug \
		--listener Listener:localhost:5555 \
		demo.robot

PHONY: install run