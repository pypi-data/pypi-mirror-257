from django import forms
from django.db import transaction

from nautobot.dcim.models import Device, Interface
from nautobot.extras.models import Status
from nautobot.core.forms import DynamicModelChoiceField


class MoveForm(forms.Form):
    to = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        display_field="display_name",
        query_params={
            "status": "Planned",
        }
    )
    delete_existing = forms.BooleanField(
        label="Remove connections",
        help_text="Should existing connections on the moved device be deleted?",
        required=False,
    )

    add_interfaces = forms.BooleanField(
        label="Add missing interfaces",
        help_text="Interfaces on planned device will be added to moved device",
        required=False,
    )

    def __init__(self, *args, instance=None, **kwargs):
        self.instance = instance
        self.component_types = [
            "console_ports",
            "console_server_ports",
            "power_ports",
            "power_outlets",
            "interfaces",
            "rear_ports",
            "front_ports",
            "device_bays",
        ]
        self.connectable_component_types = [
            "console_ports",
            "console_server_ports",
            "power_ports",
            "power_outlets",
            "interfaces",
            "rear_ports",
            "front_ports",
        ]

        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        other = Device.objects.get(pk=self.cleaned_data.get("to").pk)
        add_interfaces = self.cleaned_data.get("add_interfaces")
        delete_existing = self.cleaned_data.get("delete_existing")

        if self.instance == other:
            raise forms.ValidationError(
                "The device to move is equal to the selected one"
            )

        if self.instance.device_type != other.device_type:
            move_devicetype = str(self.instance.device_type.manufacturer) + " " + str(self.instance.device_type)
            planned_devicetype = str(other.device_type.manufacturer) + " " + str(other.device_type)
            raise forms.ValidationError(
                f"The DeviceType of planned ({move_devicetype}) and moved ({planned_devicetype}) device must be equal"
            )

        if not delete_existing:
            for component_type in self.connectable_component_types:
                prop = getattr(self.instance, component_type)
                if prop.filter(cable__isnull=False).exists():
                    raise forms.ValidationError(
                        f"The device to move still has connected {component_type}."
                    )

        if self.instance.device_bays.filter(installed_device__isnull=False).exists():
            raise forms.ValidationError(
                "The device to move still has connected device bays."
            )

        for component_type in self.component_types:
            this_prop = getattr(self.instance, component_type)
            other_prop = getattr(other, component_type)
            # it is allowed to skip this check if add_interfaces is true, the missing devices should be synced in save()
            if not (add_interfaces and component_type == "interfaces"):

                if this_prop.count() != other_prop.count():
                    raise forms.ValidationError(
                        f"The devices are incompatible: the number of {component_type} doesn’t match."
                    )

                for component in this_prop.all():
                    if not other_prop.filter(name=component.name).exists():
                        raise forms.ValidationError(
                            f"The devices are incompatible: the {component_type} named {component.name} doesn’t exist on the device {other.name}."
                        )

    def save(self):
        other = self.cleaned_data.get("to")
        delete_existing = self.cleaned_data.get("delete_existing")
        add_interfaces = self.cleaned_data.get("add_interfaces")

        with transaction.atomic():

            if other.interfaces.count() > 0:
                for interface in other.interfaces.all():
                    # do the following only, if sync was requested
                    if add_interfaces:
                        # Check if interface is available by name in self.instance
                        try:
                            self.instance.interfaces.get(name=interface.name)
                        except Interface.DoesNotExist:
                            # ...if not move it from other.instance
                            interface.device = self.instance
                            interface.validated_save()
                            if interface.cable or interface.cable_id:
                                interface.cable.save()
                            # possibily remove interfaces from self.instance if wanted, for now only additive sync is supported

                    self_interface = self.instance.interfaces.get(name=interface.name)

                    # set "active" as default status if previously not set -> mandatory from nautobot v1.4.0+
                    self_interface.status = Status.objects.get_for_model(Interface).get(name="Active")
                    # equalize status
                    if interface.status:
                        self_interface.status = interface.status
                    self_interface.validated_save()

                    # Transfer ip address information. The set() function adds ip addresses from planned device to the moved one
                    # and disassociates ip addresses which were previously on the interface
                    for ip_address in interface.ip_addresses.all():
                        ip_address.assigned_object = self_interface
                        # if one of the ip addresses is defined for use as primary address set it for the moved device
                        if ip_address == other.primary_ip4:
                            # primary_ip4 has to be removed from planned device first for satisfying constraint
                            other.primary_ip4 = None
                            other.validated_save()
                            self.instance.primary_ip4 = ip_address
                        ip_address.validated_save()
                        self_interface.tags.set(interface.tags.all())
                    # Add VLANs to moved device if exist
                    if interface.mode:
                        self_interface.mode = interface.mode
                        self_interface.untagged_vlan = interface.untagged_vlan
                        if interface.mode == "tagged":
                            self_interface.tagged_vlans.set(interface.tagged_vlans.all())
                        self_interface.validated_save()

            for component_type in self.connectable_component_types:
                for component in getattr(other, component_type).all():
                    this_component = getattr(self.instance, component_type).get(
                        name=component.name
                    )
                    if this_component.cable and delete_existing:
                        this_component.cable.delete()
                    if not component.cable_id:
                        continue
                    component.cable.delete()
                    if component.cable.termination_a == component:
                        component.cable.termination_a = this_component
                    if component.cable.termination_b == component:
                        component.cable.termination_b = this_component

                    component.cable.pk = None
                    component.cable.save()

            self.instance.device_bays.all().delete()
            other.device_bays.all().update(device=self.instance)

            self.instance.name = other.name
            self.instance.platform = other.platform
            self.instance.status = other.status
            self.instance.role = other.role
            self.instance.location = other.location
            self.instance.rack = other.rack
            self.instance.position = other.position
            self.instance.face = other.face
            self.instance.tags.set(other.tags.all())
            for custom_field in other.cf:
                self.instance.cf[custom_field] = other.cf[custom_field]

            # add bgp routing instances
            if hasattr(other, "bgp_routing_instances"):
                for bgp_routing_instance in other.bgp_routing_instances.all():
                    bgp_routing_instance.device = self.instance
                    bgp_routing_instance.validated_save()

            other.delete()
            self.instance.validated_save()

        return self.instance
