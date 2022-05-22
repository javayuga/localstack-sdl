# getting started

follow [TESTING PYTHON AWS APPLICATIONS USING LOCALSTACK](https://hands-on.cloud/testing-python-aws-applications-using-localstack/#h-connect-to-localstack-services-using-boto3)

except that:
- we'll be using dockerized localstack instead of python-installed service
- configuring aliases for awscli is optional

[Boto 3 - AWS SDK Python Library](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

```
python -m pip install boto3
```

# configure localstack profile

passwords must match the ones used in *docker-compose.yml*

```
aws configure --profile localstack

AWS Access Key ID [****************foo]:
AWS Secret Access Key [****************foo]:
Default region name [None]: ap-southeast-1
Default output format [None]:
```

# start your localstack container

then check if default bucket has been created @see scripts on folder *initaws*

```
$ docker-compose up
...

PS D:\pub\localstack-sdl> aws --endpoint=http://localhost:4566 s3 ls
2022-05-21 21:29:52 testbucket

```

# run hello_boto.py, which creates a new bucket

...

PS D:\pub\localstack-sdl> aws --endpoint=http://localhost:4566 s3 ls
2022-05-21 21:29:52 testbucket
2022-05-21 21:34:55 hands-on-cloud-localstack-bucket

```




