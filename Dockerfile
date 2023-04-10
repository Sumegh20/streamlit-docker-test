FROM python:3.9
COPY . /test
WORKDIR /test
RUN pip install -r requirements.txt
CMD ["streamlit","run","app.py"]