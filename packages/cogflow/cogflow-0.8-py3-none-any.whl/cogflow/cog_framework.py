"""
CogFramework: A class for defining reusable components and pipelines for Kubeflow Pipelines.

CogContainer: A subclass of Container that extends it with additional functionality for adding environment variables related to model access.

CogFramework:
- Initializes methods to add model access environment variables to Container classes.
- Defines a static method `pipeline` to create pipeline decorators for defining Kubeflow Pipelines.
- Provides methods for creating components from Python functions, managing the Kubeflow Pipeline client, and loading components from URLs.
- Provides methods for defining InputPath and OutputPath components.
"""


import os
from kubernetes.client.models import V1EnvVar
import kfp
from kfp import dsl
from kfp.components import InputPath
from kfp.components import OutputPath
from tenacity import retry, stop_after_attempt, wait_exponential
from kserve import KServeClient
from kubernetes import client 
from kserve import utils

from datetime import datetime
import kserve
from kubernetes.client.exceptions import ApiException

from kubernetes.client import V1ObjectMeta
from kubernetes import client as k8s_client, config as k8s_config
from kserve import (
    constants,
    KServeClient,
    V1beta1InferenceService,
    V1beta1InferenceServiceSpec,
    V1beta1PredictorSpec,
    V1beta1TFServingSpec,
    V1beta1ModelFormat,
    V1beta1ModelSpec,
)
from kserve import (
            constants,
            KServeClient,
            V1beta1InferenceService,
            V1beta1InferenceServiceSpec,
            V1beta1PredictorSpec,
            V1beta1SKLearnSpec,
        )


class CogContainer(kfp.dsl._container_op.Container):
    """
    Subclass of Container to add model access environment variables.
    """
    def __init__(self):
        """
        Initializes the CogContainer class.
        """
        super().__init__()
        
    
    def AddModelAccess(self):
        """
        Adds model access environment variables to the container.
        
        Returns:
            CogContainer: Container instance with added environment variables.
        """
        return (self.add_env_variable(V1EnvVar(name='MLFLOW_TRACKING_URI', value=os.getenv('MLFLOW_TRACKING_URI')))
        .add_env_variable(V1EnvVar(name='MLFLOW_S3_ENDPOINT_URL', value=os.getenv('MLFLOW_S3_ENDPOINT_URL')))
        .add_env_variable(V1EnvVar(name='AWS_ACCESS_KEY_ID', value=os.getenv('AWS_ACCESS_KEY_ID')))
        .add_env_variable(V1EnvVar(name='AWS_SECRET_ACCESS_KEY', value=os.getenv('AWS_SECRET_ACCESS_KEY'))))



class CogFramework:
    """
    Class for defining reusable components and pipelines for Kubeflow Pipelines.
    """
    def __init__(self):
        """
        Initializes the CogFramework class.
        """
        kfp.dsl._container_op.Container.AddModelAccess=self.AddModelAccess
        kfp.dsl._container_op.ContainerOp.AddModelAccess=self.AddModelAccess
        kfp.dsl.structures.TaskSpec.AddModelAccess=self.AddModelAccess
    

    
    def pipeline(name=None, description=None):
        """
        Decorator function to define Kubeflow Pipelines.
        
        Args:
            name (str, optional): Name of the pipeline. Defaults to None.
            description (str, optional): Description of the pipeline. Defaults to None.
        
        Returns:
            Callable: Decorator for defining Kubeflow Pipelines.
        """
        return dsl.pipeline(name=name, description=description)

    
    
    def create_component_from_func(func, output_component_file=None, base_image=None, packages_to_install=None):
        """
        Create a component from a Python function.
        
        Args:
            func (Callable): Python function to convert into a component.
            output_component_file (str, optional): Path to save the component YAML file. Defaults to None.
            base_image (str, optional): Base Docker image for the component. Defaults to None.
            packages_to_install (List[str], optional): List of additional Python packages to install in the component. Defaults to None.
        
        Returns:
            kfp.components.ComponentSpec: Component specification.
        """
        training_var= kfp.components.create_component_from_func(
            func=func,
            output_component_file=output_component_file,
            base_image=base_image,
            packages_to_install=packages_to_install
        )
        kfp.dsl._container_op.ContainerOp.AddModelAccess=CogFramework.AddModelAccess
        return training_var
    
        
    
    def client():
        """
        Get the Kubeflow Pipeline client.
        
        Returns:
            kfp.Client: Kubeflow Pipeline client instance.
        """
        return kfp.Client()
    
    
    def load_component_from_url(url):
        """
        Load a component from a URL.
        
        Args:
            url (str): URL to load the component from.
        
        Returns:
            kfp.components.ComponentSpec: Loaded component specification.
        """
        return kfp.components.load_component_from_url(url)
    
    
    def InputPath(label: str):
        """
        Create an InputPath component.
        
        Args:
            label (str): Label for the input path.
        
        Returns:
            InputPath: InputPath component instance.
        """
        return kfp.components.InputPath(label)
    
    
    def OutputPath(label: str):
        """
        Create an OutputPath component.
        
        Args:
            label (str): Label for the output path.
        
        Returns:
            OutputPath: OutputPath component instance.
        """
        return kfp.components.OutputPath(label)
    
    
    def AddModelAccess(self):
        """
        Add model access environment variables to the container.
        
        Returns:
            CogContainer: Container instance with added environment variables.
        """
        return (self.add_env_variable(V1EnvVar(name='MLFLOW_TRACKING_URI', value=os.getenv('MLFLOW_TRACKING_URI')))
        .add_env_variable(V1EnvVar(name='MLFLOW_S3_ENDPOINT_URL', value=os.getenv('MLFLOW_S3_ENDPOINT_URL')))
        .add_env_variable(V1EnvVar(name='AWS_ACCESS_KEY_ID', value=os.getenv('AWS_ACCESS_KEY_ID')))
        .add_env_variable(V1EnvVar(name='AWS_SECRET_ACCESS_KEY', value=os.getenv('AWS_SECRET_ACCESS_KEY'))))
    
    def Serve_Model_v2(model_uri:str,name:str):
        """
        Create a kserve instance.

        Args:
            model_uri (str): URI of the model.
            name (str, optional): Name of the kserve instance. If not provided, a default name will be generated.

        Returns:
            None
        """
        from kubernetes import client 
        from kserve import utils

        from datetime import datetime
        import kserve

        from kubernetes.client.exceptions import ApiException
        from kubernetes.client import V1ObjectMeta
        from kubernetes import client as k8s_client, config as k8s_config
        from kserve import (
            constants,
            KServeClient,
            V1beta1InferenceService,
            V1beta1InferenceServiceSpec,
            V1beta1PredictorSpec,
            V1beta1TFServingSpec,
            V1beta1ModelFormat,
            V1beta1ModelSpec,
        )
        namespace = utils.get_default_target_namespace()
        if name is None:
            now = datetime.now()
            v = now.strftime("%d%M")
            name='predictor_model{}'.format(v)
        ISVC_NAME=name
        predictor = V1beta1PredictorSpec(
            service_account_name="kserve-controller-s3",
            min_replicas=1,
            model=V1beta1ModelSpec(
                model_format=V1beta1ModelFormat(
                    name="mlflow",
                ),
                storage_uri=model_uri,
                protocol_version="v2",
            ),
        )

        isvc = V1beta1InferenceService(
            api_version=constants.KSERVE_V1BETA1,
            kind=constants.KSERVE_KIND,
            metadata=client.V1ObjectMeta(
                name=ISVC_NAME, namespace=namespace,
                annotations={"sidecar.istio.io/inject": "false"},
            ),
            spec=V1beta1InferenceServiceSpec(predictor=predictor),
        )
        KServe = KServeClient()
        try:
            KServe.create(isvc)
        except ApiException as e:
            if e.status == 409:
                # Handle the conflict error
                print("Inference service already exists.")
            else:
                #    Handle other ApiException errors
                print("An error occurred:", e)

    

    def Serve_Model_v1(model_uri:str,name:str):
        """
        Create a kserve instance version1.

        Args:
            model_uri (str): URI of the model.
            name (str, optional): Name of the kserve instance. If not provided, a default name will be generated.

        Returns:
            None
        """
        import requests
        from tenacity import retry, stop_after_attempt, wait_exponential
        from kubernetes.client import V1ObjectMeta
        from kubernetes import client as k8s_client, config as k8s_config
        from kserve import (
            constants,
            KServeClient,
            V1beta1InferenceService,
            V1beta1InferenceServiceSpec,
            V1beta1PredictorSpec,
            V1beta1SKLearnSpec,
        )
        ISVC_NAME = name
        namespace = utils.get_default_target_namespace()
        isvc = V1beta1InferenceService(
            api_version=constants.KSERVE_V1BETA1,
            kind=constants.KSERVE_KIND,
            metadata=V1ObjectMeta(
                name=ISVC_NAME,
                namespace=namespace,
                annotations={"sidecar.istio.io/inject": "false"}
            
            ),
            spec=V1beta1InferenceServiceSpec(
                predictor=V1beta1PredictorSpec(
                    service_account_name="kserve-controller-s3",
                    sklearn=V1beta1SKLearnSpec(
                        storage_uri=model_uri
                    )
                )
            )
        )
        client = KServeClient()
        try:
            client.create(isvc)
        except ApiException as e:
            if e.status == 409:
                # Handle the conflict error
                print("Inference service already exists.")
            else:
                #    Handle other ApiException errors
                print("An error occurred:", e)



    
    def GetModelUrl(modelName:str):
        """
        Retrieve the URL of a deployed model.

        Args:
            modelName (str): Name of the deployed model.

        Returns:
            str: URL of the deployed model.
        """
        client = KServeClient()
        namespace = utils.get_default_target_namespace()
        isvc_resp = client.get(modelName)
        isvc_url = isvc_resp['status']['address']['url']
        @retry(
        wait=wait_exponential(multiplier=2, min=1, max=10),
        stop=stop_after_attempt(30),
        reraise=True,
        )
        def _assert_isvc_created(client, isvc_name):
            """Wait for the Inference Service to be created successfully."""
            assert client.is_isvc_ready(isvc_name), f"Failed to create Inference Service {isvc_name}."
        
        _assert_isvc_created(client, modelName)
        return isvc_url
    
    

        


