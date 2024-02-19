import enum
from typing import Optional, Union
from pydantic import BaseModel

from dpt.processor import Task, TaskOutputRef, Workflow


class WorkflowNodeType(enum.Enum):
    TASK = "TASK"
    COLLECTION = "COLLECTION"
    VALUE = "VALUE"


class WorkflowNode(BaseModel):
    id: str
    title: Optional[str] = None
    node_type: WorkflowNodeType


class WorkflowTaskNode(WorkflowNode):
    name: str
    module: str
    processor: str


class WorkflowCollectionNode(WorkflowNode):
    name: str


class WorkflowValueNode(WorkflowNode):
    value: Union[dict, list]


class WorkflowEdgeType(enum.Enum):
    DATA = "DATA"


class WorkflowEdge(BaseModel):
    id: str = ""
    from_node: str
    to_node: str
    from_port: Optional[str] = None
    to_port: Optional[str] = None
    edge_type: WorkflowEdgeType


class WorkflowGraph(BaseModel):
    nodes: list[Union[WorkflowTaskNode, WorkflowCollectionNode, WorkflowValueNode]] = []
    edges: list[WorkflowEdge] = []


def _get_task_id(item: Task):
    return f"{WorkflowNodeType.TASK.value}: {item.get_name()}"


def _get_collection_id(item: str):
    return f"{WorkflowNodeType.COLLECTION.value}: {item}"


def _add_edge(graph: WorkflowGraph, item: WorkflowEdge):
    id = str(len(graph.edges))
    item.id = id
    graph.edges.append(item)


def workflow_to_graph(workflow: Workflow):
    graph = WorkflowGraph()
    for task in workflow.tasks.values():
        task.apply_default_binding()

    for task in workflow.tasks.values():
        node = WorkflowTaskNode(
            id=_get_task_id(task),
            name=task.get_name(),
            title=task.get_title(),
            module=task.processor.module.name,
            processor=task.processor.name,
            node_type=WorkflowNodeType.TASK,
        )
        graph.nodes.append(node)

    collections = set()
    for task in workflow.tasks.values():

        def collect(ports, type):
            for name in ports:
                value = ports[name]
                if isinstance(value, str):
                    collections.add(value)
                    if type == "input":
                        edge = WorkflowEdge(
                            from_node=_get_collection_id(value),
                            to_node=_get_task_id(task),
                            to_port=name,
                            edge_type=WorkflowEdgeType.DATA,
                        )
                    else:
                        edge = WorkflowEdge(
                            from_node=_get_task_id(task),
                            to_node=_get_collection_id(value),
                            from_port=name,
                            edge_type=WorkflowEdgeType.DATA,
                        )
                    _add_edge(graph, edge)
                elif isinstance(value, (dict, list)):
                    node_id = f"{WorkflowNodeType.VALUE.value}:{task.get_name()}.{name}"
                    node = WorkflowValueNode(
                        id=node_id,
                        value=value,
                        node_type=WorkflowNodeType.VALUE,
                    )
                    graph.nodes.append(node)
                    edge = WorkflowEdge(
                        from_node=node_id,
                        to_node=_get_task_id(task),
                        to_port=name,
                        edge_type=WorkflowEdgeType.DATA,
                    )
                    _add_edge(graph, edge)
                elif isinstance(value, TaskOutputRef):
                    edge = WorkflowEdge(
                        from_node=_get_task_id(value.task),
                        to_node=_get_task_id(task),
                        from_port=value.name,
                        to_port=name,
                        edge_type=WorkflowEdgeType.DATA,
                    )
                    _add_edge(graph, edge)
        collect(task.get_input_binding_info(), "input")
        collect(task.get_output_binding_info(), "output")
    for item in collections:
        node = WorkflowCollectionNode(
            id=_get_collection_id(item),
            name=item,
            node_type=WorkflowNodeType.COLLECTION,
        )
        graph.nodes.append(node)

    return graph
