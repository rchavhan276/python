FROM python:alpine3.17

# Set the working directory inside the container

# Copy the Python requirements file and install the dependencies
RUN apk update && apk add gnupg gcc g++ unixodbc-dev unixodbc curl 

COPY requirements.txt .
RUN pip install --use-pep517 package-name && pip install --upgrade pip && pip install --upgrade setuptools
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python code to the container
COPY . .

# Set the default command to run when the container starts
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
# uvicorn app.main:app --host 0.0.0.0
