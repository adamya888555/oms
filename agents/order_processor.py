import json
import os
from pydantic import BaseModel
from typing import Dict
from enum import Enum
from order_types import OrderState
from langchain_core.messages import SystemMessage
from langchain_ollama import ChatOllama
from data.storage import OrderStorage
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class OrderProcessor:
    """
    LangChain agent for orchestrating LLM calls to process order queries and small talk.
    Uses Ollama Mistral and prompt files for dynamic processing.
    """
    def __init__(self, storage: OrderStorage):
        self.storage = storage
        self.llm = ChatOllama(model="neural-chat",temperature=0)
        # Set prompt_dir to AIRTEL OMS/prompts/ from project root
        

    

    def render_prompt(self, prompt_template: str, **kwargs) -> str:
        all_fields = [
            'order_id', 'role', 'user_input', 'lob', 'order_type', 'order_subtype'
            , 'system_statuses', 'order_data', 'intent'
        ]
        def enum_to_val(val):
            if isinstance(val, Enum):
                return val.value
            if isinstance(val, dict):
                return {enum_to_val(k): enum_to_val(v) for k, v in val.items()}
            return val

        # Build safe_kwargs with all fields, convert None to empty string
        safe_kwargs = {k: "" for k in all_fields}
        safe_kwargs.update(**{k: enum_to_val(v) if v is not None else "" for k, v in kwargs.items()})

        try:
            return prompt_template.format(**safe_kwargs)
        except KeyError as e:
            missing_key = str(e).strip('"')
            logger.info(f"Prompt template: {prompt_template}")  # Debugging line
            logger.warning(f"Missing key in prompt template: {missing_key}. Available keys: {list(safe_kwargs.keys())}")
            raise
        except TypeError as e:
            logger.error(f"TypeError during prompt formatting: {e}. safe_kwargs: {safe_kwargs}")
            raise
    def parsing_input(self, user_input: str , role: str) -> Dict:
        logger.info(f"[process_input] user_input: {user_input}, role: {role}")
        parser_prompt = f"""You are an expert order assistant. Parse the user's message and extract the following fields for a structured order system:

- intent: One of "order_status" or "small_talk" (for casual chat), matching the user's request.
- If the intent is "small_talk", set all other fields to null.
- order_id: The order identifier, matching the format NN-NNNNN... (e.g., 21-3983223455, 21-8675555), or null if not present/invalid.
- lob: Either "broadband" or "postpaid", or null if not present.
- type: One of "new", "shift", "changeplan", "pause", "resume", or null if not present/invalid.
- subtype: One of "new", "migration", "intra", "inter", "upgrade", "downgrade", "addon", "voluntary", "involuntary", "temporary", "permanent", or null if not present/invalid.

If the intent is "small_talk", set all other fields to null.

Return ONLY a valid JSON object with these exact keys and values in lowercase as shown.  
Do not include any explanation, extra text, labels, or formatting except the JSON itself.  
Do NOT include 'Input:', 'Output:', or any other text. Only output the JSON object.

Examples:

{{"order_id": "21-247827", "lob": "broadband", "type": "new", "subtype": "new", "intent": "order_status"}}
{{"order_id": "21-7348579387", "lob": null, "type": null, "subtype": null, "intent": "order_status"}}
{{"order_id": null, "lob": null, "type": null, "subtype": null, "intent": "small_talk"}}

ALWAYS return only the valid JSON object, with all five keys present and nothing else.

The user said: {user_input}
"""

        message = [SystemMessage(content=parser_prompt)]
        logger.info(f"[process_input] Parser prompt: {parser_prompt}")
        try: 
            parsed_response = self.llm.invoke(message)
            parsed = json.loads(parsed_response.content.strip())
            logger.info(f"[parsing_input] LLM Parsed: {parsed}")

            return parsed
        except Exception as e:
            logger.exception(f"[parsing_input] Error while calling LLM or parsing JSON: {e}")
            return {
            "intent": "unknown",
            "order_id": None,
            "lob": None,
            "type": None,
            "subtype": None
        }
    
    def coerce_to_order_state(self, d: dict) -> OrderState:
        # Only keep keys that are in OrderState
        allowed_keys = {'user_input', 'role', 'order_data', 'response', 'intent', 'order_lob', 'order_id', 'order_type', 'order_subtype', 'system_statuses'}
        return OrderState(**{k: d[k] for k in allowed_keys if k in d})






    


class OrderStatusSummary(BaseModel):
    name: str       # Customer name
    address: str    # Customer address
    order_id: str
    lob: str
    order_type: str
    subtype: str
    overall_status: str
    detailed_statuses: dict  # e.g. {"Siebel": "complete", "Optimus": "pending"}

def generate_order_status_summary(
    llm: ChatOllama,
    order_info: dict,
    system_statuses: dict,
    role: str,
) -> OrderStatusSummary:
    import json
    system_lines = "\n".join(f"{k.split('_')[0].capitalize()}: {v}" for k, v in system_statuses.items())

    prompt = f"""
You are an assistant tasked with summarizing the broadband order status for a user.

Role: {role}
Customer name: Generate a random name
Address: Generate a random address
Order ID: {order_info.get('order_id')}
LOB: {order_info.get('lob')}
Order type: {order_info.get('order_type')}
Subtype: {order_info.get('subtype')}

System statuses:  
{system_lines}

Please respond with a JSON object containing the following keys:  
- name  
- address  
- order_id  
- lob  
- order_type  
- subtype  
- detailed_statuses (dictionary with system names capitalized as keys and statuses as values)

The output must be valid JSON only, no other text.
"""

    response = llm.invoke(prompt)
    content = response.content if hasattr(response, "content") else str(response)
    
    try:
        parsed_json = json.loads(content)
    except json.JSONDecodeError as e:
        # handle exception as needed
        raise

    # Compute overall_status in code:
    detailed_statuses = parsed_json.get("detailed_statuses", {})
    if any(str(v).lower() == "pending" for v in detailed_statuses.values()):
        overall_status = "pending"
    else:
        overall_status = "complete"

    parsed_json["overall_status"] = overall_status  # Add to final output

    summary = OrderStatusSummary.parse_obj(parsed_json)
    return summary



def crm_summarizer(llm, summary: "OrderStatusSummary") -> str:
    """
    Uses an LLM (e.g., ChatOllama) to create a customer relationship manager style
    summary based on the detailed order status summary.

    Args:
        llm: Your LLM instance (e.g., self.order_processor.llm)
        summary: An OrderStatusSummary Pydantic model instance

    Returns:
        str: A polished customer-friendly summary string.
    """
    # Prepare detailed statuses as a readable list
    detailed_list = "\n".join(
        f"- {system}: {status.capitalize()}"
        for system, status in summary.detailed_statuses.items()
    )
    
    # Compose prompt for CRM-style summary
    prompt = f"""You are an L1 support agent assistant tasked with providing a professional, concise summary of a customer's order status.

Given the following order details, generate a response that meets these requirements:

- Display the Customer Name and Address clearly at the top.
- List the Order details (Order ID, LOB, Order Type, Subtype) as clean bullet points with one space after the dash, right after the customer info.
- On the next line after the order details, provide the Overall Status on its own line, starting with "Overall Status:" followed by the status capitalized.
- From the next line, list each system's status in the following "sub status" format, one per line:
  - Begin each line with a dash and an arrow and a space "->", followed immediately by the system name (capitalized), a colon, a space, then the status capitalized.
  
Example of sub status lines:
-> Optimus: Pending
-> Siebel: Complete
-> Ldap: Complete
-> Fx: Complete
-> Nokia: Complete

- Use professional, concise language without salutations, filler phrases, or next-step suggestions.
- Make sure there is only one blank line between each major section (customer info, order details, overall status, detailed statuses).
- At the end create a one or two line summary only including the order id and the systems where its pending. Include a sample emailadress for  resolving issues.
- The output should be easy to read and suitable for quick comprehension by an L1 agent.

Input details:

Customer Name: {summary.name}  
Address: {summary.address}

Order Details:
- Order ID: {summary.order_id}  
- LOB: {summary.lob}  
- Order Type: {summary.order_type}  
- Subtype: {summary.subtype}

Overall Status: {summary.overall_status.capitalize()}

Detailed System Statuses:
{detailed_list}

"""


    try:
        response = llm.invoke(prompt)
        final_message = response.content if hasattr(response, "content") else str(response)
    except Exception as e:
        logger.error(f"Error invoking LLM in crm_summarizer: {e}")
        final_message = f"Your order status is: {summary.overall_status.capitalize()}. Detailed statuses are available in your account."

    logger.info(f"[crm_summarizer] Generated message: {final_message}")

    return final_message
   
        

   