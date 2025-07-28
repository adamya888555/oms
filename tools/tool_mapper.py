from typing import List
from order_types import OrderType, SubType, Lob

TOOL_MAPPING = {
    (Lob.POSTPAID,OrderType.NEW, SubType.MIGRATION): [
        "optimus_check_postpaid_new_migration",
        "siebel_check_postpaid_new_migration",
        "ldap_check_postpaid_new_migration",
        "fx_check_postpaid_new_migration",
        "nokia_check_postpaid_new_migration"
    ],
    (Lob.POSTPAID, OrderType.CHANGEPLAN, SubType.ADDON): [
        "optimus_check_broadband_changeplan_addon",
        "siebel_check_broadband_changeplan_addon",
        "ldap_check_broadband_changeplan_addon",
        "fx_check_broadband_changeplan_addon",
        "nokia_check_broadband_changeplan_addon"
    ],
    (Lob.POSTPAID, OrderType.NEW, SubType.NEW): [
        "optimus_check_postpaid_new_new",
        "siebel_check_postpaid_new_new",
        "ldap_check_postpaid_new_new",
        "fx_check_postpaid_new_new",
        "nokia_check_postpaid_new_new"
    ],
    (Lob.POSTPAID, OrderType.SHIFT, SubType.INTRA): [
        "optimus_check_postpaid_shift_intra",
        "siebel_check_postpaid_shift_intra",
        "ldap_check_postpaid_shift_intra",
        "fx_check_postpaid_shift_intra",
        "nokia_check_postpaid_shift_intra"
    ],
    (Lob.POSTPAID, OrderType.SHIFT, SubType.INTER): [
        "optimus_check_postpaid_shift_inter",
        "siebel_check_postpaid_shift_inter",
        "ldap_check_postpaid_shift_inter",
        "fx_check_postpaid_shift_inter",
        "nokia_check_postpaid_shift_inter"
    ],
    (Lob.POSTPAID, OrderType.CHANGEPLAN, SubType.UPGRADE): [
        "optimus_check_postpaid_changeplan_upgrade",
        "siebel_check_postpaid_changeplan_upgrade",
        "ldap_check_postpaid_changeplan_upgrade",
        "fx_check_postpaid_changeplan_upgrade",
        "nokia_check_postpaid_changeplan_upgrade"
    ],
    (Lob.POSTPAID, OrderType.CHANGEPLAN, SubType.DOWNGRADE): [
        "optimus_check_postpaid_changeplan_downgrade",
        "siebel_check_postpaid_changeplan_downgrade",
        "ldap_check_postpaid_changeplan_downgrade",
        "fx_check_postpaid_changeplan_downgrade",
        "nokia_check_postpaid_changeplan_downgrade"
    ],
    (Lob.POSTPAID, OrderType.CHANGEPLAN, SubType.ADDON): [
        "optimus_check_postpaid_changeplan_addon",
        "siebel_check_postpaid_changeplan_addon",
        "ldap_check_postpaid_changeplan_addon",
        "fx_check_postpaid_changeplan_addon",
        "nokia_check_postpaid_changeplan_addon"
    ],
    (Lob.POSTPAID, OrderType.PAUSE, SubType.VOLUNTARY): [
        "optimus_check_postpaid_pause_voluntary",
        "siebel_check_postpaid_pause_voluntary",
        "ldap_check_postpaid_pause_voluntary",
        "fx_check_postpaid_pause_voluntary",
        "nokia_check_postpaid_pause_voluntary"
    ],
    (Lob.POSTPAID, OrderType.PAUSE, SubType.INVOLUNTARY): [
        "optimus_check_postpaid_pause_involuntary",
        "siebel_check_postpaid_pause_involuntary",
        "ldap_check_postpaid_pause_involuntary",
        "fx_check_postpaid_pause_involuntary",
        "nokia_check_postpaid_pause_involuntary"
    ],
    (Lob.POSTPAID, OrderType.PAUSE, SubType.TEMPORARY): [
        "optimus_check_postpaid_pause_temporary",
        "siebel_check_postpaid_pause_temporary",
        "ldap_check_postpaid_pause_temporary",
        "fx_check_postpaid_pause_temporary",
        "nokia_check_postpaid_pause_temporary"
    ],
    (Lob.POSTPAID, OrderType.PAUSE, SubType.PERMANENT): [
        "optimus_check_postpaid_pause_permanent",
        "siebel_check_postpaid_pause_permanent",
        "ldap_check_postpaid_pause_permanent",
        "fx_check_postpaid_pause_permanent",
        "nokia_check_postpaid_pause_permanent"
    ],
    (Lob.POSTPAID, OrderType.RESUME, SubType.VOLUNTARY): [
        "optimus_check_postpaid_resume_voluntary",
        "siebel_check_postpaid_resume_voluntary",
        "ldap_check_postpaid_resume_voluntary",
        "fx_check_postpaid_resume_voluntary",
        "nokia_check_postpaid_resume_voluntary"
    ],
    (Lob.POSTPAID, OrderType.RESUME, SubType.INVOLUNTARY): [
        "optimus_check_postpaid_resume_involuntary",
        "siebel_check_postpaid_resume_involuntary",
        "ldap_check_postpaid_resume_involuntary",
        "fx_check_postpaid_resume_involuntary",
        "nokia_check_postpaid_resume_involuntary"
    ],
    (Lob.POSTPAID, OrderType.RESUME, SubType.INVOLUNTARY): [
        "optimus_check_broadband_resume_involuntary",
        "siebel_check_broadband_resume_involuntary",
        "ldap_check_broadband_resume_involuntary",
        "fx_check_broadband_resume_involuntary",
        "nokia_check_broadband_resume_involuntary"
    ],
    (Lob.POSTPAID, OrderType.RESUME, SubType.VOLUNTARY): [
        "optimus_check_broadband_resume_voluntary",
        "siebel_check_broadband_resume_voluntary",
        "ldap_check_broadband_resume_voluntary",
        "fx_check_broadband_resume_voluntary",
        "nokia_check_broadband_resume_voluntary"
    ],
    (Lob.BROADBAND, OrderType.RESUME, SubType.INVOLUNTARY): [
        "optimus_check_broadband_resume_involuntary",
        "siebel_check_broadband_resume_involuntary",
        "ldap_check_broadband_resume_involuntary",
        "fx_check_broadband_resume_involuntary",
        "nokia_check_broadband_resume_involuntary"
    ],
    (Lob.BROADBAND, OrderType.RESUME, SubType.VOLUNTARY): [
        "optimus_check_broadband_resume_voluntary",
        "siebel_check_broadband_resume_voluntary",
        "ldap_check_broadband_resume_voluntary",
        "fx_check_broadband_resume_voluntary",
        "nokia_check_broadband_resume_voluntary"
    ],
    (Lob.BROADBAND, OrderType.PAUSE, SubType.PERMANENT): [
        "optimus_check_broadband_pause_permanent",
        "siebel_check_broadband_pause_permanent",
        "ldap_check_broadband_pause_permanent",
        "fx_check_broadband_pause_permanent",
        "nokia_check_broadband_pause_permanent"
    ],
    (Lob.BROADBAND, OrderType.PAUSE, SubType.TEMPORARY): [
        "optimus_check_broadband_pause_temporary",
        "siebel_check_broadband_pause_temporary",
        "ldap_check_broadband_pause_temporary",
        "fx_check_broadband_pause_temporary",
        "nokia_check_broadband_pause_temporary"
    ],
    (Lob.BROADBAND, OrderType.PAUSE, SubType.INVOLUNTARY): [
        "optimus_check_broadband_pause_involuntary",
        "siebel_check_broadband_pause_involuntary",
        "ldap_check_broadband_pause_involuntary",
        "fx_check_broadband_pause_involuntary",
        "nokia_check_broadband_pause_involuntary"
    ],
    (Lob.BROADBAND, OrderType.PAUSE, SubType.VOLUNTARY): [
        "optimus_check_broadband_pause_voluntary",
        "siebel_check_broadband_pause_voluntary",
        "ldap_check_broadband_pause_voluntary",
        "fx_check_broadband_pause_voluntary",
        "nokia_check_broadband_pause_voluntary"
    ],
    (Lob.BROADBAND, OrderType.CHANGEPLAN, SubType.ADDON): [
        "optimus_check_broadband_changeplan_addon",
        "siebel_check_broadband_changeplan_addon",
        "ldap_check_broadband_changeplan_addon",
        "fx_check_broadband_changeplan_addon",
        "nokia_check_broadband_changeplan_addon"
    ],
    (Lob.BROADBAND, OrderType.CHANGEPLAN, SubType.DOWNGRADE): [
        "optimus_check_broadband_changeplan_downgrade",
        "siebel_check_broadband_changeplan_downgrade",
        "ldap_check_broadband_changeplan_downgrade",
        "fx_check_broadband_changeplan_downgrade",
        "nokia_check_broadband_changeplan_downgrade"
    ],
    (Lob.BROADBAND, OrderType.CHANGEPLAN, SubType.UPGRADE): [
        "optimus_check_broadband_changeplan_upgrade",
        "siebel_check_broadband_changeplan_upgrade",
        "ldap_check_broadband_changeplan_upgrade",
        "fx_check_broadband_changeplan_upgrade",
        "nokia_check_broadband_changeplan_upgrade"
    ],
    (Lob.BROADBAND, OrderType.SHIFT, SubType.INTER): [
        "optimus_check_broadband_shift_inter",
        "siebel_check_broadband_shift_inter",
        "ldap_check_broadband_shift_inter",
        "fx_check_broadband_shift_inter",
        "nokia_check_broadband_shift_inter"
    ],
    (Lob.BROADBAND, OrderType.SHIFT, SubType.INTRA): [
        "optimus_check_broadband_shift_intra",
        "siebel_check_broadband_shift_intra",
        "ldap_check_broadband_shift_intra",
        "fx_check_broadband_shift_intra",
        "nokia_check_broadband_shift_intra"
    ],
    (Lob.BROADBAND, OrderType.NEW, SubType.NEW): [
        "optimus_check_broadband_new_new",
        "siebel_check_broadband_new_new",
        "ldap_check_broadband_new_new",
        "fx_check_broadband_new_new",
        "nokia_check_broadband_new_new"
    ],
    (Lob.BROADBAND, OrderType.NEW, SubType.MIGRATION): [
        "optimus_check_broadband_new_migration",
        "siebel_check_broadband_new_migration",
        "ldap_check_broadband_new_migration",
        "fx_check_broadband_new_migration",
        "nokia_check_broadband_new_migration"
    ],

}

def get_tools_for_order(LOB , order_type,subtype) -> List[str]:
    return TOOL_MAPPING.get((LOB , order_type, subtype), [])

