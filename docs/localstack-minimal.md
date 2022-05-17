# localstack minimal

1. run docker services


## s3 and dynamodb

sets up these services: s3 and dynamoDB (AWS Lambda will be added later)

## install pre-reqs

1. run docker-compose to get localstack up

```
docker-compose up

```


2. install awscli (if needed)

[Localstack and aws-cli documentation](https://docs.localstack.cloud/integrations/aws-cli/)

[aws-cli command options](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-options.html)

```
pip install awscli

```

3. set region to ap-southeast-1 (same region as docker-compose, avoids error message about specifying a region)

```
aws configure

AWS Access Key ID [****************YSYY]:
AWS Secret Access Key [****************HmDM]:
Default region name [None]: ap-southeast-1
Default output format [None]:
```

## S3

1. create a test bucket
```
aws --endpoint-url=http://localhost:4566 s3 mb s3://mybucket
```

2. upload a file

```
$ aws --endpoint-url=http://localhost:4566 s3 cp README.md s3://mybucket
upload: .\README.md to s3://mybucket/README.md
```

3. check if file is really there    

```
$ aws --endpoint-url=http://localhost:4566 s3 ls s3://mybucket
2022-05-11 21:02:37       3514 README.md
```

4. download CyberDuck to visualize files

Download CyberDuck visualizer from [here](https://cyberduck.io/download/)

![alt text](docs/img/s3_00.png "07")


## Dynamodb-admin on localstack

based on this [simple and effective tutorial](https://onexlab-io.medium.com/docker-compose-dynamodb-localstack-a967a8f49a0e)


1. issue command to create dynamo-db table

```
aws dynamodb --endpoint-url=http://localhost:4566 create-table --table-name Music --attribute-definitions AttributeName=Artist,AttributeType=S AttributeName=SongTitle,AttributeType=S --key-schema AttributeName=Artist,KeyType=HASH AttributeName=SongTitle,KeyType=RANGE --provisioned-throughput ReadCapacityUnits=10,WriteCapacityUnits=5 --region=ap-southeast-1

```

expected response

```
{
    "TableDescription": {
        "AttributeDefinitions": [
            {
                "AttributeName": "Artist",
                "AttributeType": "S"
            },
            {
                "AttributeName": "SongTitle",
                "AttributeType": "S"
            }
        ],
        "TableName": "Music",
        "KeySchema": [
            {
                "AttributeName": "Artist",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "SongTitle",
                "KeyType": "RANGE"
            }
        ],
        "TableStatus": "ACTIVE",
        "CreationDateTime": 1652305352.831,
        "ProvisionedThroughput": {
            "ReadCapacityUnits": 10,
            "WriteCapacityUnits": 5
        },
        "TableSizeBytes": 0,
        "ItemCount": 0,
        "TableArn": "arn:aws:dynamodb:ap-southeast-1:000000000000:table/Music",
        "TableId": "dd00f761-f2ed-4f2d-a2e5-06841aa67ba8"
    }
}
```

2. check TableStatus

```
aws --endpoint-url=http://localhost:4566 dynamodb describe-table --table-name Music | grep TableStatus
```

expected response
```
"TableStatus": "ACTIVE",
```

3. insert data

```
aws --endpoint-url=http://localhost:4566 dynamodb put-item --table-name Music  --item '{\"Artist\": {\"S\": \"No One You Know\"}, \"SongTitle\": {\"S\": \"Call Me Today\"}}'

{
    "ConsumedCapacity": {
        "TableName": "Music",
        "CapacityUnits": 1.0
    }
}
```


4. read data

```
aws dynamodb scan --endpoint-url=http://localhost:4566 --table-name Music
```

5. download and install NoSQL workbench

get [NoSQL Workbench](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/workbench.html) executable for your OS in [download site](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/workbench.settingup.html)

6. follow the screenshots

![alt text](docsgdyn_00.png "00")
![alt text](docs/img/dyn_01.png "01")
![alt text](docs/img/dyn_02.png "02")
![alt text](docs/img/dyn_03.png "03")
connection name : locdyn_alstack port : 4566
![alt text](docs/img/dyn_04.png "04")
![alt text](docs/img/dyn_05.png "05")
![alt text](docs/img/dyn_06.png "06")
![alt text](docs/img/dyn_07.png "07")





