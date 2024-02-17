import jpype
import jpype.imports
import jpype.types
from urllib import request
from pathlib import Path
from airflow.hooks.base import BaseHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.plugins_manager import AirflowPlugin


class OnetableHook(BaseHook):
    def sync(
        self,
        config: Path,
        catalog: Path = None,
    ):

        # Launch the JVM
        path = Path(__file__).resolve().parent
        jpype.startJVM(classpath=path / "jars/*")
        run_sync = jpype.JPackage("io").onetable.utilities.RunSync.main

        # call java class
        if catalog:
            run_sync(["--datasetConfig", config, "--icebergCatalogConfig", catalog])

        else:
            run_sync(["--datasetConfig", config])

        # shutdown
        jpype.shutdownJVM()

    def setup(self):
        # paths
        path = Path(__file__).resolve().parent / "jars"
        path.mkdir(exist_ok=True)

        # vars
        jars = {
            "iceberg-spark-runtime-3.4_2.12-1.4.2.jar": "https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-3.4_2.12/1.4.2/iceberg-spark-runtime-3.4_2.12-1.4.2.jar",
            "iceberg-aws-bundle-1.4.2.jar": "https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-aws-bundle/1.4.2/iceberg-aws-bundle-1.4.2.jar",
            "utilities-0.1.0-SNAPSHOT-bundled.jar": "https://d1bjpw1aruo86w.cloudfront.net/05eb631ce7f32184ac864b6f1cc81db8/utilities-0.1.0-SNAPSHOT-bundled.jar",
        }

        # download jars
        for jar, url in jars.items():
            if not (path / jar).exists():
                print(f"Downloading {jar} ...")
                request.urlretrieve(
                    url,
                    path / jar,
                )


class OnetableOperator(BaseOperator):

    @apply_defaults
    def __init__(self, config, *args, **kwargs):
        super(OnetableOperator, self).__init__(*args, **kwargs)
        self.config = Path(config)

    def execute(self, context):
        hook = OnetableHook()
        hook.sync(config=self.config)


class OnetablePlugin(AirflowPlugin):
    # The name of your plugin (str)
    name = "onetable"
    operators = [OnetableOperator]
    hooks  = [OnetableHook]

    # A callback to perform actions when airflow starts and the plugin is loaded.
    # NOTE: Ensure your plugin has *args, and **kwargs in the method definition
    #   to protect against extra parameters injected into the on_load(...)
    #   function in future changes
    def on_load(*args, **kwargs):
        # ... perform Plugin boot actions
        hook = OnetableHook()
        hook.setup()