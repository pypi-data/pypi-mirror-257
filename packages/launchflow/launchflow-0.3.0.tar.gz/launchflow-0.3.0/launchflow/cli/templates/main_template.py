from typing import List

from launchflow.cli.project_gen import Framework, Resource

# TODO: look at adding templates for using the provided resources
FAST_API_TEMPLATE = """\
from fastapi import FastAPI{resources}

app = FastAPI()

@app.get("/")
def root():
    return {{"message": "Hello World"}}
"""


def template(framework: Framework, resources: List[Resource]):
    lf_resources_import_str = ""
    if resources:
        lf_resources_import_str = "\nfrom infra import " + ", ".join(
            [r.get_var_name() for r in resources]
        )

    if framework == Framework.FASTAPI:
        return FAST_API_TEMPLATE.format(resources=lf_resources_import_str)
