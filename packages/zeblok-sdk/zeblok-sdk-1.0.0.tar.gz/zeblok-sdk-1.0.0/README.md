# Zeblok Python SDK

Python SDK will help in integrating outside systems with Zeblok platform via code

## Create Python Package

Run the following command from the project root directory to create the python wheel file

```python
python setup.py sdist bdist_wheel
```

## Usage

### Microservice

#### Authentication

```python
from zeblok.auth import AuthOld

auth = AuthOld(username='<your-username>', password='<your-password>', base_url='<your-zbl-url>')

auth_token = auth.get_token()
```

#### Deploy Image

```python
from zeblok.microservice import ModelMicroService

microservice_model = ModelMicroService(
    base_url='<your-zbl-url>', token=auth.get_token(), bucket_name='<bucket-name>',
    username='<your-username>', storage_url='<storage-url>'
)

microservice_model.deploy_microservice(
    image_name='<image-name>', microservice_id='<microservice-id>', plan_id="<plan-id>",
    service_name=f'<unique-service-name>', namespace_id='<namespace-id>',
    datacenter_id='<datacenter-id>', envs=['example-env1', 'example-env2', 'example-env3']
)
```

#### Get Namespaces

```python
from zeblok.microservice import ModelMicroService

microservice_model = ModelMicroService(
    base_url='<your-zbl-url>', token=auth.get_token(), bucket_name='<bucket-name>',
    username='<your-username>', storage_url='<storage-url>'
)

microservice_model.get_plans()
```

#### Get Datacenters

```python
from zeblok.microservice import ModelMicroService

microservice_model = ModelMicroService(
    base_url='<your-zbl-url>', token=auth.get_token(), bucket_name='<bucket-name>',
    username='<your-username>', storage_url='<storage-url>'
)

microservice_model.get_datacenters()
```

#### Get Namespaces

```python
from zeblok.microservice import ModelMicroService

microservice_model = ModelMicroService(
    base_url='<your-zbl-url>', token=auth.get_token(), bucket_name='<bucket-name>',
    username='<your-username>', storage_url='<storage-url>'
)

microservice_model.get_namespaces()
```

### Pipeline

#### Deploy Pipeline

```python
from pipeline import PipelineOld

pipeline = PipelineOld(
    base_url="<your-zbl-url>",
    cross_cloud_service_url='<zbl-cross-cloud-url>', storage_url='<storage-url>',
    api_access_key='<api_access_key>', api_access_secret='<api_access_secret>',
    storage_username='<storage_username>', storage_access_secret='<storage_access_secret>'
)

pipeline.deploy_pipeline(
    model_folder_path='<model-folder-path>', entrypoint='<entrypoint>', bucket_name='<bucket-name>',
    pipeline_name='<unique-pipeline-name>', plan_id=['<plan-id1>', '<plan-id2'],
    namespace_id='<namespace-id>', datacenter_id='<datacenter-id>', autodeploy=True
)
```

#### Get Namespaces

```python
from pipeline import PipelineOld

pipeline = PipelineOld(
    base_url="<your-zbl-url>", cross_cloud_service_url='<zbl-cross-cloud-url>', storage_url='<storage-url>',
    api_access_key='<api_access_key>', api_access_secret='<api_access_secret>',
    storage_username='<storage_username>', storage_access_secret='<storage_access_secret>'
)

pipeline.get_plans()
```

#### Get Datacenters

```python
from pipeline import PipelineOld

pipeline = PipelineOld(
    base_url="<your-zbl-url>", cross_cloud_service_url='<zbl-cross-cloud-url>', storage_url='<storage-url>',
    api_access_key='<api_access_key>', api_access_secret='<api_access_secret>',
    storage_username='<storage_username>', storage_access_secret='<storage_access_secret>'
)

pipeline.get_datacenters()
```

#### Get Namespaces

```python
from pipeline import PipelineOld

pipeline = PipelineOld(
    base_url="<your-zbl-url>", cross_cloud_service_url='<zbl-cross-cloud-url>', storage_url='<storage-url>',
    api_access_key='<api_access_key>', api_access_secret='<api_access_secret>',
    storage_username='<storage_username>', storage_access_secret='<storage_access_secret>'
)

pipeline.get_namespaces()
```


