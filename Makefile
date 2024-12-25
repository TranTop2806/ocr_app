nom-api:
	python nom/api.py

extract:
	python package/extract.py

han-api:
	python han/api.py

worker:
	python event/worker.py

run:
	streamlit run app.py
	