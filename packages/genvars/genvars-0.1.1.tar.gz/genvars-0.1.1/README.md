# GenVars

Generate description tables for your Pydantic BaseSettings models in Markdown.

```shell
Usage: poetry run python3 -m genvars [-h] [--output OUTPUT] modules [modules ...]

positional arguments:
  modules          Modules with settings to describe, e.g. common.settings config <...>

options:
  -h, --help       show this help message and exit
  --output OUTPUT  Output file in Markdown.
```

<!-- begin env -->
### AWSS3CliSettings

|Variable|Type|Default|Description|
|--------------|--------------|--------------|--------------|
|`CONFIG_FILE_PATH`|string|~/.aws/config||
|`MAX_CONCURRENT_REQUESTS`|integer|10|The number of concurrent uploads per directory. The minimum count of threads on my system was 6 with the concurrency value of 1. https://docs.aws.amazon.com/cli/latest/topic/s3-config.html#max-concurrent-requests|
|`MAX_QUEUE_SIZE`|integer|1000|https://docs.aws.amazon.com/cli/latest/topic/s3-config.html#max-queue-size|
|`MULTIPART_THRESHOLD`|string|8MB|https://docs.aws.amazon.com/cli/latest/topic/s3-config.html#multipart-threshold|
|`MULTIPART_CHUNKSIZE`|string|8MB|https://docs.aws.amazon.com/cli/latest/topic/s3-config.html#multipart-chunksize|
|`MAX_BANDWIDTH`|string, null|None|https://docs.aws.amazon.com/cli/latest/topic/s3-config.html#max-bandwidth|
|`ARGS`|array|['--size-only']|Arbitrary keyword arguments to be passed to the AWS CLI command.|


### BackupManagerSettings

|Variable|Type|Default|Description|
|--------------|--------------|--------------|--------------|
|`SCHEMA`|string|http||
|`HOST`|string|||
|`PORT`|integer|||


### PostgresSettings

|Variable|Type|Default|Description|
|--------------|--------------|--------------|--------------|
|`HOST`|string|||
|`PORT`|integer|||
|`USER`|string|||
|`PASSWORD`|string|||
|`DB`|string|||


### ProductionS3StorageSettings

|Variable|Type|Default|Description|
|--------------|--------------|--------------|--------------|
|`CONFIG_FILE_PATH`|string|~/.aws/config||
|`MAX_CONCURRENT_REQUESTS`|integer|10|The number of concurrent uploads per directory. The minimum count of threads on my system was 6 with the concurrency value of 1. https://docs.aws.amazon.com/cli/latest/topic/s3-config.html#max-concurrent-requests|
|`MAX_QUEUE_SIZE`|integer|1000|https://docs.aws.amazon.com/cli/latest/topic/s3-config.html#max-queue-size|
|`MULTIPART_THRESHOLD`|string|8MB|https://docs.aws.amazon.com/cli/latest/topic/s3-config.html#multipart-threshold|
|`MULTIPART_CHUNKSIZE`|string|8MB|https://docs.aws.amazon.com/cli/latest/topic/s3-config.html#multipart-chunksize|
|`MAX_BANDWIDTH`|string, null|None|https://docs.aws.amazon.com/cli/latest/topic/s3-config.html#max-bandwidth|
|`ARGS`|array|['--size-only']|Arbitrary keyword arguments to be passed to the AWS CLI command.|
|`ACCESS_KEY_ID`|string|||
|`SECRET_ACCESS_KEY`|string|||
|`ENDPOINT_URL`|string|||
|`REGION`|string|||
|`BUCKET_NAME`|string||Name of the bucket to be used.|


### S3StorageSettings

|Variable|Type|Default|Description|
|--------------|--------------|--------------|--------------|
|`ACCESS_KEY_ID`|string|||
|`SECRET_ACCESS_KEY`|string|||
|`ENDPOINT_URL`|string|||
|`REGION`|string|||
<!-- end env -->
