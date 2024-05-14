run-dev:
	export NO_AUTH=true && uvicorn colbertdb.server.main:app --reload