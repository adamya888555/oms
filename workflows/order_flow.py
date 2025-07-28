from order_types import OrderState, Lob, OrderType, SubType
from langgraph.graph import StateGraph, END
import json
from agents.order_processor import OrderProcessor, generate_order_status_summary, crm_summarizer
from data.storage import OrderStorage
from typing import TypedDict, Optional, Dict,  Any
from tools.tool_mapper import get_tools_for_order
from tools import siebel_tools, ldap_tools, nokia_tools, fx_tools, optimus_tools
import random



import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OrderWorkflow:
    """
    LangGraph state machine for managing order processing workflow.
    Uses OrderProcessor to handle LLM calls.
    """
    def __init__(self, storage: OrderStorage):
        self.order_processor = OrderProcessor(storage)
        self.graph: Any = self._build_graph()

    def _build_graph(self) -> Any:
        """Build the LangGraph state machine."""
        workflow = StateGraph(OrderState)

        # Add nodes
        workflow.add_node("parse_input", self.parse_input)
        workflow.add_node("handle_small_talk", self.handle_small_talk)
        workflow.add_node("validate_input", self.validate_input)
        workflow.add_node("tool_executor", self.tool_executor)
        workflow.add_node("format_output", self.format_output)
     
       
        # Add edges
        workflow.add_conditional_edges(
            "parse_input",
            self.route_after_parse,
            {
                "small_talk": "handle_small_talk",
                "order_status": "validate_input"
            }
        )
        workflow.add_conditional_edges(
            "validate_input",
            self.route_after_validate,
            {
                "order_status": "tool_executor",
            }
        )
        workflow.add_edge("handle_small_talk", END)
        workflow.add_edge("tool_executor", "format_output")
        
        workflow.add_edge("format_output", END)

        # Set entry point
        workflow.set_entry_point("parse_input")
        return workflow.compile()

    def parse_input(self, state: OrderState) -> OrderState:
        logger.info("[parse_input] ENTRY: state = %s", state)

        # Call the LLM parsing function
        parsed = self.order_processor.parsing_input(
            user_input=state.get("user_input", ""),
            role=state.get("role", "")
        )

        logger.info("[parse_input] LLM parsed = %s", parsed)

        # Update state with parsed values
        new_state = {
            **state,
            "intent": parsed.get("intent"),
            "order_id": parsed.get("order_id"),
            "order_lob": parsed.get("lob"),
            "order_type": parsed.get("type"),
            "subtype": parsed.get("subtype"),
            # Any additional values from parsed if needed
            "response": None,
            "order_data": None,
            "system_statuses": None
        }

        logger.info("[parse_input] Output state: %s", new_state)
        return OrderState(**new_state)
    
    
#          ^^^^^^^^^^^^^^^^

    def handle_small_talk(self, state: OrderState) -> OrderState:
        logger.info("[handle_small_talk] ENTRY: state = %s", state)
        user_input = state.get("user_input")
        response = self.order_processor.llm.invoke(user_input)
        logger.info("[handle_small_talk] Output state: %s", response)
        state["response"] = response.content  # Add the response to the state
        return state  # Return the whole updated dictionary



    def validate_input(self, state: OrderState) -> OrderState:
        logger.info("[validate_input] ENTRY: state = %s", state)
        LOB_TYPE_SUBTYPE_MAP = {
            "broadband": {
                "new": ["new", "migration"],
                "shift": ["intra", "inter"],
                "changeplan": ["upgrade", "downgrade","addon"],
                "pause": ["voluntary","involuntary","temporary","permanent"],
                "resume": ["voluntary","involuntary"]
            },
            "postpaid": {
                "new": ["new", "migration"],
                "shift": ["intra", "inter"],
                "changeplan": ["upgrade", "downgrade","addon"],
                "pause": ["voluntary","involuntary","temporary","permanent"],
                "resume": ["voluntary","involuntary"]
            },
        }

        order_id = state.get("order_id")
        intent = state.get("intent")
        order_lob = state.get("order_lob")
        order_type = state.get("order_type")
        subtype = state.get("subtype")

        if not order_id or intent != "order_status":
            raise ValueError(f"[validate_input] Missing or invalid order_id/intent! order_id: {order_id}, intent: {intent}")

        # Step 2: Fill missing fields logically and randomly
        if not order_lob:
            order_lob = random.choice(list(LOB_TYPE_SUBTYPE_MAP.keys()))
        type_map = LOB_TYPE_SUBTYPE_MAP[order_lob]

        if not order_type:
            order_type = random.choice(list(type_map.keys()))
            
        if not subtype:
            subtype = random.choice(type_map[order_type])
        logger.info("[validate_input] Validated values — order_lob: %s, order_type: %s, subtype: %s",
                    order_lob, order_type, subtype)

        # Update OrderState
        new_state = {
            **state,
            "order_lob": order_lob,
            "order_type": order_type,
            "subtype": subtype,
            "response": None,              # We'll generate response later
            "order_data": None,            # Fetched next node
            "system_statuses": None        # Will be populated in process_order_status node
        }

        logger.info("[validate_input] EXIT: state = %s", new_state)
        return OrderState(**new_state)


    def tool_executor(self, state: OrderState) -> OrderState:
        logger.info("[multi_tool_executor] ENTRY State : %s", state )
        
        order_id = state.get("order_id")
        lob = state.get("order_lob")
        order_type = state.get("order_type")
        subtype = state.get("subtype")

        
        try:
            lob_enum = Lob(lob.lower())
            order_type_enum = OrderType(order_type.lower())
            subtype_enum = SubType(subtype.lower())
        except ValueError as e:
            logger.exception("Enum coercion failed: %s", e)
            return OrderState(**{
                **state,
                "response": "Invalid values for lob, type or subtype"
            })

        tools_to_call = get_tools_for_order(lob_enum, order_type_enum, subtype_enum)
        
        if not tools_to_call:
            logger.warning("No tools mapped for (%s, %s, %s)", lob, order_type, subtype)
            return OrderState(**{
                **state,
                "response": f"No tools configured for ({lob}, {order_type}, {subtype})"
            })
        
        tool_modules = [optimus_tools, fx_tools, siebel_tools, ldap_tools, nokia_tools]
        available_tools =[]

        for func_name in tools_to_call:
            found = False
            for mod in tool_modules:
                if hasattr(mod, func_name):
                    func = getattr(mod, func_name)
                    found = True
                    available_tools.append(func)
                if not found:
                    logger.warning("No tool found bro")
                

        if not available_tools:
            logger.warning("No registered tool functions found for: %s", tools_to_call)
            return OrderState(**{
                **state,
                "response": f"No registered tool functions for: {tools_to_call}"
            })

        logger.info("Tools are %s",tools_to_call)

        logger.info("Tools are %s",available_tools)
        tool_responses = {}

        for tool in available_tools:
            try:
                result = tool.invoke({"order_id": order_id})
                tool_responses[tool.name] = result
                logger.info("✓ Tool %s → %s", tool.name, result)
            except Exception as e:
                tool_responses[tool.name] = f"Error: {e}"
                logger.warning("⚠️ Tool %s failed: %s", tool.name, e)

        new_state = {
            **state,
            "order_lob": lob,
            "order_type": order_type,
            "subtype": subtype,
            "response": None,              
            "order_data": None,            
            "system_statuses": tool_responses      
        }

        logger.info("[multi_tool_executor] EXIT: state = %s", new_state)
        return OrderState(**new_state)



    def format_output(self, state: OrderState) -> OrderState:
        order_info = {
            "name": "xyz",               # Replace with real customer data if you have it
            "address": "jjajdhsjhalh...", 
            "order_id": state.get("order_id", ""),
            "lob": state.get("order_lob", ""),
            "order_type": state.get("order_type", ""),
            "subtype": state.get("subtype", ""),
        }
        system_statuses = state.get("system_statuses", {})
        role = state.get("role", "customer")

        summary = generate_order_status_summary(
            self.order_processor.llm,
            order_info,
            system_statuses,
            role,
        )

        logger.info(f"Final summary JSON: {json.dumps(summary.dict(), indent=2)}")
        
        crm_message = crm_summarizer(self.order_processor.llm, summary)

        logger.info(f"final: %s",crm_message)

        return OrderState(**{**state, "response": crm_message})



    def route_after_parse(self, state: OrderState) -> str:
        logger.info("[route_after_parse] ENTRY: state = %s", state)
        logger.info("[route_after_parse] Routing intent: %s", state.get("intent"))
        if state.get("intent") == "small_talk":
            logger.info("[route_after_parse] EXIT: next = small_talk")
            return "small_talk"
        logger.info("[route_after_parse] EXIT: next = order_status")
        return "order_status"

    def route_after_validate(self, state: OrderState) -> str:
        logger.info("[route_after_validate] ENTRY: state = %s", state)
        if state.get("intent") == "order_status" and state.get("order_id") and (state.get("order_type") and state.get("subtype")):
            logger.info("[route_after_validate] EXIT: next = order_status")
            return "order_status"
        logger.info("[route_after_validate] EXIT: next = prompt_again")
        return "prompt_again"

    def run(self, user_input: str, role: str) -> tuple[str, Optional[Dict]]:
        logger.info("[run] ENTRY: user_input = %s, role = %s", user_input, role)
        initial_state = {
            "user_input": user_input,
            "role": role,
            "order_data": None,
            "response": "",
            "intent": None,
            "order_id": None,
            "order_type": None,
            "subtype": None,
            "system": None,
            "new_status": None
        }
        logger.info("[run] Initial state: %s", initial_state)
        final_state = self.graph.invoke(initial_state)
        logger.info("[run] FINAL STATE: %s", final_state)
        return final_state["response"], final_state["order_data"]