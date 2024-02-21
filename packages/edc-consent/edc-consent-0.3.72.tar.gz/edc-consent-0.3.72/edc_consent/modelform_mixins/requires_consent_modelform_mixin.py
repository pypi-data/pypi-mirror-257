from __future__ import annotations

from typing import TYPE_CHECKING

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from edc_sites import site_sites
from edc_utils import floor_secs, formatted_date, formatted_datetime
from edc_utils.date import to_local, to_utc
from edc_visit_schedule.site_visit_schedules import site_visit_schedules

from .. import NotConsentedError
from ..exceptions import ConsentDefinitionDoesNotExist

if TYPE_CHECKING:
    from ..model_mixins import ConsentModelMixin

__all__ = ["RequiresConsentModelFormMixin"]


class RequiresConsentModelFormMixin:
    """Model form mixin for CRF or PRN forms to access the consent.

    Use with CrfModelMixin, etc
    """

    def clean(self):
        cleaned_data = super().clean()
        self.validate_against_consent()
        return cleaned_data

    def validate_against_consent(self) -> None:
        """Raise an exception if the report datetime doesn't make
        sense relative to the consent.
        """
        if self.report_datetime:
            try:
                model_obj = self.get_consent_or_raise()
            except ConsentDefinitionDoesNotExist as e:
                raise forms.ValidationError(e)
            except NotConsentedError as e:
                raise forms.ValidationError(e)
            else:
                if floor_secs(to_utc(self.report_datetime)) < floor_secs(
                    model_obj.consent_datetime
                ):
                    dte_str = formatted_datetime(to_local(model_obj.consent_datetime))
                    raise forms.ValidationError(
                        f"Report datetime cannot be before consent datetime. Got {dte_str}."
                    )
                if to_utc(self.report_datetime).date() < model_obj.dob:
                    dte_str = formatted_date(model_obj.dob)
                    raise forms.ValidationError(
                        f"Report datetime cannot be before DOB. Got {dte_str}"
                    )

    @property
    def consent_model(self) -> str:
        return site_visit_schedules.get_consent_model(
            visit_schedule_name=self.visit_schedule_name,
            schedule_name=self.schedule_name,
            site=site_sites.get(self.site.id),
        )

    def get_consent_or_raise(self) -> ConsentModelMixin:
        """Return an instance of the consent model"""
        if getattr(self, "related_visit", None):
            cdef = self.related_visit.schedule.get_consent_definition(
                site=site_sites.get(self.site.id),
                report_datetime=self.report_datetime,
            )
        else:
            cdef = self.schedule.get_consent_definition(
                site=site_sites.get(self.site.id),
                report_datetime=self.report_datetime,
            )
        try:
            obj = cdef.get_consent_for(
                subject_identifier=self.get_subject_identifier(),
                report_datetime=self.report_datetime,
            )
        except ObjectDoesNotExist:
            raise forms.ValidationError(
                f"`{cdef.model_cls._meta.verbose_name}` does not exist "
                f"to cover this subject on {formatted_datetime(self.report_datetime)}"
            )
        return obj
