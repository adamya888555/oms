from typing import TypedDict, Optional, Dict
from enum import Enum

class Lob(Enum):
    BROADBAND = "broadband"
    POSTPAID = "postpaid"

class OrderType(Enum):
    NEW = "new"
    SHIFT = "shift"
    CHANGEPLAN = "changeplan"
    PAUSE = "pause"
    RESUME = "resume"

class SubType(Enum):
    NEW = "new"
    MIGRATION = "migration"
    INTRA = "intra"
    INTER = "inter"
    UPGRADE = "upgrade"
    DOWNGRADE = "downgrade"
    ADDON = "addon"
    VOLUNTARY = "voluntary"
    INVOLUNTARY = "involuntary"
    TEMPORARY = "temporary"
    PERMANENT = "permanent"
   
   

class SystemStatus(Enum):
    PENDING = "pending"
    COMPLETE = "complete"
    FAILED = "failed"

class System(Enum):
    SIEBEL = "siebel"
    NOKIA = "nokia"
    LDAP = "ldap"
    FX = "fx"
    OPTIMUS = "optimus"

class IntentType(Enum):
    SMALL_TALK = "small_talk"
    ORDER_STATUS = "order_status"

class OrderState(TypedDict):
    user_input: str
    role: str
    order_data: Optional[Dict]
    response: str
    intent: IntentType
    order_lob: Optional[Lob]
    order_id: str
    order_type: Optional[OrderType]
    subtype: Optional[SubType]
    system_statuses: Optional[Dict[System, SystemStatus]] 



   