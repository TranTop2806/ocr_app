run:
	streamlit run app.py

build:
	docker build -t ocr_app .

run-docker:
	docker run -p 8501:8501  \
	    -e EMAIL=dotu30257@gmail.com \
		-e TOKEN=7f853fbc-951b-429d-b515-011a9ad5d733 \
		-e GOOGLE_APPLICATION_CREDENTIALS=credential/key.json \
		ocr_app
	