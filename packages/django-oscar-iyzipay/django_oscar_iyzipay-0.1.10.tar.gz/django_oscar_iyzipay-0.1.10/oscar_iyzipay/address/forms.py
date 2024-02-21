from oscar.apps.address import forms as base_forms
from oscar.core.loading import get_model

UserAddress = get_model("address", "useraddress")


class UserAddressForm(base_forms.UserAddressForm):

    class Meta(base_forms.UserAddressForm.Meta):
        model = UserAddress
        fields = [
            "first_name",
            "last_name",
            "TCKN",
            "line1",
            "line2",
            "line3",
            "line4",
            "state",
            "postcode",
            "country",
            "phone_number",
            "notes",
        ]

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.user = user
