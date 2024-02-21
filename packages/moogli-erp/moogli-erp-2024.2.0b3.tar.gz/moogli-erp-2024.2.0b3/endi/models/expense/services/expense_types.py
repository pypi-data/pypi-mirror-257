import itertools

from sqlalchemy import (
    func,
    or_,
)

from endi_base.models.base import (
    DBSESSION,
)


class ExpenseTypeService:
    """Handle complex queries en ExpenseTypes"""

    @classmethod
    def _id_used_in(cls, *args):
        """
        Collects the ids of the ExpenseTypes linked to the elements of provided
        lists

        param *args: one or several iterables of elements having a
            `type_id` attr
        return: list of ExpenseTypes id (deduplicated)
        """
        return list({obj.type_id for obj in itertools.chain(*args)})

    @classmethod
    def active_or_used_in(cls, *args):
        """
        Returns the union of the enabled ExpenseTypes and those used
        by provided object lists.

        param *args: one or several iterables of elements having a
          `type_id` attr
        return: list of ExpenseTypes id (deduplicated)

        """
        from endi.models.expense.types import ExpenseType

        used_ids = cls._id_used_in(*args)
        query = ExpenseType.query().filter(
            or_(
                ExpenseType.active == True,  # noqa
                ExpenseType.id.in_(used_ids),
            )
        )
        query = query.order_by(ExpenseType.order)
        return query

    @staticmethod
    def get_by_label(cls, label: str, case_sensitive: bool = False):
        query = cls.query().filter(cls.active == True)  # noqa: E712
        exact_match = query.filter(cls.label == label).one_or_none()

        if exact_match or case_sensitive:
            return exact_match
        else:
            insensitive_match = query.filter(
                func.lower(cls.label) == func.lower(label)
            ).one_or_none()
            return insensitive_match

    @classmethod
    def allowed_driver(cls, user, year):
        """
        Applies the optional per-user restriction on ExpenseKmType

        :param user User: the user who declared this vehicle
        :param year: the year the vehicle is declared for
        :return: the allowed ExpenseTypeKm
        :rtype: list of ExpenseTypeKm
        """
        from endi.models.expense.types import ExpenseKmType

        query = DBSESSION().query(ExpenseKmType)
        query = query.filter_by(active=True)
        query = query.filter_by(year=year)

        if user.vehicle and "-" in user.vehicle:
            label, code = user.vehicle.rsplit("-", 1)
            query = query.filter_by(label=label).filter_by(code=code)

        return query

    @classmethod
    def allowed_driver_or_used_in(cls, user, year, *args):
        """
        Union of allowed_driver types and those already used in *args

        :param user User: the user who declared this vehicle
        :param year: the year the vehicle is declared for

        :return: the allowed ExpenseTypeKm
        :rtype: list of ExpenseTypeKm
        """
        from endi.models.expense.types import ExpenseKmType

        driver_allowed_ids = [i.id for i in cls.allowed_driver(user, year)]
        used_ids = cls._id_used_in(*args)

        # Either this is an already used and disabled (old expense), or we
        # require it to be allowed.
        return cls.active_or_used_in(*args).filter(
            or_(
                ExpenseKmType.active == False,  # noqa
                ExpenseKmType.id.in_(used_ids),
                ExpenseKmType.id.in_(driver_allowed_ids),
            )
        )

    @classmethod
    def find_internal(cls, etype_class):
        return etype_class.query().filter_by(internal=True).all()
