from flask import Blueprint
from flask import request
from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.cpu import CPU,CPUSchema
from api.models.scaled_cpu import ScaledCPU,ScaledCPUSchema
from api.models.gpu import GPU,GPUSchema
from api.models.scaled_gpu import ScaledGPU,ScaledGPUSchema
from api.models.notebook import Notebook,NotebookSchema
from api.models.scaled_notebook import ScaledNotebook,ScaledNotebookSchema
from api.models.last_build import LastBuild,LastBuildSchema


db_update_routes=Blueprint("db_update_routes")

@db_update_routes.route("/cpu",methods=["GET"])
def get_cpu_dump():
    fetched=CPU.query.all()
    cpus_schema=CPUSchema(many=True)
    cpus, _ = cpus_schema.dump(fetched)
    return response_with(resp.SUCCESS_200,values={"cpus":cpus})

@db_update_routes.route("/scaled-cpu",methods=["GET"])
def get_scaled_cpu_dump():
    fetched=ScaledCPU.query.all()
    scaled_cpus_schema=ScaledCPUSchema(many=True)
    scaled_cpus, _ = scaled_cpus_schema.dump(fetched)
    return response_with(resp.SUCCESS_200,values={"scaled_cpus":scaled_cpus})

@db_update_routes.route("/gpu",methods=["GET"])
def get_cpu_dump():
    fetched=GPU.query.all()
    gpus_schema=GPUSchema(many=True)
    gpus, _ = gpus_schema.dump(fetched)
    return response_with(resp.SUCCESS_200,values={"gpus":gpus})

@db_update_routes.route("/scaled-gpu",methods=["GET"])
def get_scaled_cpu_dump():
    fetched=ScaledGPU.query.all()
    scaled_gpus_schema=ScaledGPUSchema(many=True)
    scaled_gpus, _ = scaled_gpus_schema.dump(fetched)
    return response_with(resp.SUCCESS_200,values={"scaled_gpus":scaled_gpus})

@db_update_routes.route("/notebook",methods=["GET"])
def get_cpu_dump():
    fetched=Notebook.query.all()
    notebooks_schema=NotebookSchema(many=True)
    notebooks, _ = notebooks_schema.dump(fetched)
    return response_with(resp.SUCCESS_200,values={"notebooks":notebooks})

@db_update_routes.route("/scaled-notebook",methods=["GET"])
def get_scaled_cpu_dump():
    fetched=ScaledNotebook.query.all()
    scaled_notebooks_schema=ScaledNotebookSchema(many=True)
    scaled_notebooks, _ = scaled_notebooks_schema.dump(fetched)
    return response_with(resp.SUCCESS_200,values={"scaled_notebooks":scaled_notebooks})

@db_update_routes.route("/build-number",methods=["GET"])
def get_build_number_dump():
    fetched=LastBuild.query.first()
    last_build_schema=LastBuildSchema()
    build_number, _ = last_build_schema.dump(fetched)
    return response_with(resp.SUCCESS_200,values={"build number":build_number})