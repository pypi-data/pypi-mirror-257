import colander

from endi import forms
from endi.models.task.invoice import get_invoice_years


class NovaStatsSchema(colander.MappingSchema):
    year = forms.year_filter_node(
        name="year",
        query_func=get_invoice_years,
        title="Année des prestations",
        default=forms.deferred_default_year,
        missing=colander.required,
    )
