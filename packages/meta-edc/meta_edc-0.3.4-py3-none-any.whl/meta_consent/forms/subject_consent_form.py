from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from edc_consent.form_validators import SubjectConsentFormValidatorMixin
from edc_consent.modelform_mixins import ConsentModelFormMixin
from edc_form_validators import FormValidator, FormValidatorMixin
from edc_sites.forms import SiteModelFormMixin

from ..models import SubjectConsent


class SubjectConsentFormValidator(SubjectConsentFormValidatorMixin, FormValidator):
    def validate_identity(self) -> None:
        """Override to validate `identity_type` is a hospital
        number and `identity` matches the screening form.
        """
        if self.cleaned_data.get("identity_type") != "hospital_no":
            raise forms.ValidationError({"identity_type": _("Expected 'hospital number'.")})

        if self.subject_screening.hospital_identifier != (
            self.cleaned_data.get("identity") or getattr(self.instance, "identity", "")
        ):
            raise forms.ValidationError(
                {
                    "identity": (
                        _("The hospital identifier does not match that reported at screening.")
                    )
                }
            )

    def validate_consent_datetime(self):
        if getattr(settings, "EDC_CONSENT_BYPASS_CONSENT_DATETIME_VALIDATION", False):
            return None
        return super().validate_consent_datetime()


class SubjectConsentForm(
    SiteModelFormMixin, ConsentModelFormMixin, FormValidatorMixin, forms.ModelForm
):
    form_validator_cls = SubjectConsentFormValidator

    def validate_gender_of_consent(self):
        return None

    def validate_guardian_and_dob(self):
        return None

    class Meta:
        model = SubjectConsent
        fields = "__all__"
        help_texts = {
            "identity": (
                _(
                    "Use Country ID Number, Passport number, driver's license "
                    "number or Country ID receipt number"
                )
            ),
            "witness_name": (
                _(
                    "Required only if participant is illiterate. "
                    "Format is 'LASTNAME, FIRSTNAME'. "
                    "All uppercase separated by a comma."
                )
            ),
            "screening_identifier": _("(read-only)"),
        }
        widgets = {
            "screening_identifier": forms.TextInput(attrs={"readonly": "readonly"}),
        }
