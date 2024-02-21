from colanderalchemy import SQLAlchemySchemaNode
from endi.models.price_study import PriceStudy

from endi import forms
from endi.forms.custom_types import QuantityType


def get_price_study_add_edit_schema():
    result = SQLAlchemySchemaNode(
        PriceStudy,
        includes=[
            "general_overhead",
            "mask_hours",
        ],
    )
    forms.customize_field(result, "general_overhead", typ=QuantityType(), missing=None)
    return result
