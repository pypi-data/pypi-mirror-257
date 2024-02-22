from nautobot.core.api import WritableNestedSerializer, CustomFieldModelSerializerMixin, BaseModelSerializer
from nautobot.dcim.api.serializers import ManufacturerSerializer, DeviceSerializer
from nautobot.tenancy.api.serializers import TenantSerializer
from rest_framework import serializers
from nautobot_sfp_inventory.models import SFPType, SFP


class NestedSFPTypeSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:nautobot_sfp_inventory-api:sfptype-detail")

    class Meta:
        model = SFPType
        fields = ["id", "url", "name", "display"]


class SFPTypeSerializer(CustomFieldModelSerializerMixin, BaseModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:nautobot_sfp_inventory-api:sfptype-detail")

    class Meta:
        model = SFPType
        fields = [
            "id",
            "url",
            "name",
            "display",
            "comments",
            "custom_fields",
            "created",
            "last_updated",
        ]


class SFPSerializer(CustomFieldModelSerializerMixin, BaseModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:nautobot_sfp_inventory-api:sfp-detail")
    tenant = TenantSerializer()
    type = NestedSFPTypeSerializer()
    supplier = ManufacturerSerializer(required=False, allow_null=True)
    assigned_device = DeviceSerializer(required=False, allow_null=True)

    class Meta:
        model = SFP
        fields = [
            "id",
            "url",
            "serial_number",
            "display",
            "type",
            "dc_tag",
            "asset_tag",
            "tenant",
            "assigned",
            "assigned_device",
            "supplier",
            "procurement_ident",
            "end_of_manufacturer_support",
            "comments",
            "custom_fields",
            "created",
            "last_updated",
        ]
