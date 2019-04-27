FROM continuumio/miniconda3:4.3.27

# Set environmental variable(s)
ENV ACCEPT_INTEL_PYTHON_EULA=yes


ADD . /code
WORKDIR /code
EXPOSE 8000

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD python main.py

