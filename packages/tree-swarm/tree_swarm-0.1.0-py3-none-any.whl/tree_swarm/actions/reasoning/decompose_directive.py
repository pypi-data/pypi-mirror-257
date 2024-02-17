from pydantic import BaseModel, Field
from typing import List

from tree_swarm.swarm.types import Swarm, SwarmCommand, LifecycleCommand, BlockingOperation, NodeOutput


class DecomposeDirective(BaseModel):
    subdirectives: List[str] = Field(..., description="List of subdirectives to be executed in parallel.")


def main(swarm: Swarm, node_id: str, message: str) -> BlockingOperation:

        
    system_instructions = ('Generate subgoals based on available information, ensuring they are independent '
                           'and can be pursued simultaneously without relying on the completion of other goals. '
                           'Equip each subgoal with necessary details for immediate and independent'
                           'execution. Identify and list subgoals that can operate concurrently, excluding '
                           'sequential or interdependent tasks. You will be able to break down complex goals into '
                           'specific subgoals that can include anything, from asking the user questions, '
                           'writing code, doing research, browsing the internet etc. I want to emphasize that '
                           'the subgoals should be INDEPENDENT. You will be able to generate another set of '
                           'subgoals after completing the current set.')
    
    messages = [
        {
            "role": "system",
            "content": system_instructions
        },
        {
            "role": "user",
            "content": f'Directive: \n`{message}`'
        }
    ]
    
    return BlockingOperation(
        lifecycle_command=LifecycleCommand.BLOCKING_OPERATION,
        node_id=node_id,
        type="openai_instructor_completion",
        args={
            "messages": messages,
            "instructor_model": DecomposeDirective
        },
        context={
            "directive": message
        },
        next_function_to_call="subdirectives_to_swarm_commands"
    )
    

def subdirectives_to_swarm_commands(directive: str, completion: DecomposeDirective) -> NodeOutput:
    subdirectives = completion.subdirectives

    swarm_commands = []
    for subdirective in subdirectives:
        swarm_command = SwarmCommand(
            action_id='aga_swarm/actions/swarm/actions/route_to_action',
            message=subdirective
        )
        swarm_commands.append(swarm_command)
    
    return NodeOutput(
        lifecycle_command=LifecycleCommand.SPAWN,
        swarm_commands=swarm_commands,
        report=f'Decomposed directive: \n`{directive}`\n\nInto subdirectives:\n' + '\n'.join(subdirectives)
    )
