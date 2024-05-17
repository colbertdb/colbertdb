run-dev:
	export NO_AUTH=true && uvicorn colbertdb.server.main:app --reload

test:
	docker exec -it colbertdb poetry run pytest -v