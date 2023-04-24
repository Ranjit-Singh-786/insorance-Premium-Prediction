FROM python:3.8-slim-buster
# USER root
# to make repository to store snapshot of project in dockerimage
# RUN mkdir /app  
# to copy all the snapshot in app repository .means from current directory    
WORKDIR /app
COPY . /app
# to define current working directory inside the app directory

# to install all the dependency
RUN pip install -r requirements.txt
CMD ["python", "train.py"]












# CMD ["python",'main.py']


# alternative command for above command
# CMD ["python", "train.py"] 
# CMD ["python",'main.py']

# to initialize the airflow enviroment variable

# ENV AIRFLOW_HOME="/app/airflow"
# ENV AIRFLOW__CORE__DAGBAG_IMPORT_TIMEOUT=1000
# ENV AIRFLOW__CORE__ENABLE_XCOM_PICKLING=True
# RUN airflow db init 
# RUN airflow users create  -e avnish@ineuron.ai -f Avnish -l Yadav -p admin -r Admin  -u admin
# RUN chmod 777 start.sh
# RUN apt update -y && apt install awscli -y
# ENTRYPOINT [ "/bin/sh" ]
# CMD ["start.sh"]