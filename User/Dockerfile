FROM python:3.11
EXPOSE 8084
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . ./
ENV AWS_REGION=us-east-1
# AWS credentials will be passed as environment variables when running the container
# Example: docker run -e AWS_ACCESS_KEY_ID=your_key -e AWS_SECRET_ACCESS_KEY=your_secret -e BUCKET_NAME=your_bucket -p 8083:8083 -it pdf-reader-admin
ENTRYPOINT [ "streamlit", "run", "app.py", "--server.port=8084", "--server.address=0.0.0.0" ]
