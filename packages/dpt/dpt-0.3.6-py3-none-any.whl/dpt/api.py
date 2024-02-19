import sys
from fastapi import FastAPI, HTTPException, Path, Query, Body
from dpt.processor import Project
from dpt.workflow_graph import WorkflowGraph
from dpt.workflow_graph import workflow_to_graph
import os
from importlib.util import spec_from_file_location, module_from_spec

app = FastAPI(port=8000, title="DPT Python API")

dpt_root = os.getenv("DPT_ROOT")
dpt_main_file = os.getenv("DPT_MAIN_FILE")
dpt_main_func = os.getenv("DPT_MAIN_FUNC")


def _run_function(root_path, file_path, func_name):
    if root_path not in sys.path:
        sys.path.append(root_path)
    file_full_path = os.path.join(root_path, file_path)
    spec = spec_from_file_location("module", file_full_path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    func = getattr(module, func_name)
    return func()


project: Project = _run_function(dpt_root, dpt_main_file, dpt_main_func)


# @app.get("/graph")
# async def get_graph1(workspace: str = Query(...)) -> WorkflowGraph:

#     processor = project.get_processor("siber", "match_substation_workflow")
#     workflow = processor.get_workflow()
#     graph = workflow_to_graph(workflow)
#     return graph


@app.get("/modules/{module_name}/processors/{processor_name}/graph")
async def get_graph(
    module_name: str = Path(...),
    processor_name: str = Path(...),
) -> WorkflowGraph:
    processor = project.get_processor(module_name, processor_name)
    workflow = processor.get_workflow()
    graph = workflow_to_graph(workflow)
    return graph
