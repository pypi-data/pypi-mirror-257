from collections import defaultdict

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View

from nautobot.dcim.models import (
    ConsolePort, ConsoleServerPort, Device, DeviceBay, FrontPort, Interface,
    PowerOutlet, PowerPort, RearPort
)
from nautobot.core.views.mixins import GetReturnURLMixin


class ReapplyView(PermissionRequiredMixin, GetReturnURLMixin, View):
    permission_required = 'dcim.edit_device'
    mappings = {
        'console_port': ConsolePort,
        'console_server_port': ConsoleServerPort,
        'power_port': PowerPort,
        'power_outlet': PowerOutlet,
        'interface': Interface,
        'rear_port': RearPort,
        'front_port': FrontPort,
        'device_bay': DeviceBay,
    }

    def get_edits(self, existing, templates):
        edits = defaultdict(list)
        keys = set(existing.keys()).intersection(set(templates.keys()))

        for key in keys:
            reality = existing[key]
            data = templates[key]

            for field in data._meta.fields:
                if field.name in ["device_type", "id", "created", "last_updated"]:
                    continue
                if getattr(reality, field.name) != getattr(data, field.name):
                    edits[key].append(field.name)

        return dict(edits)

    def get_mutations(self, device, additive=False):
        ty = device.device_type

        res = {}

        for name, model in self.mappings.items():
            existing = {e.name: e for e in getattr(device, "{}s".format(name)).all()}
            templates = {e.name: e for e in getattr(ty, "{}_templates".format(name)).all()}
            res[name] = {}
            res[name]['add'] = [
                v for k, v in templates.items() if k not in existing
            ]
            if not additive:
                res[name]['edits'] = self.get_edits(existing, templates)
                res[name]['delete'] = [
                    v for k, v in existing.items() if k not in templates
                ]

        return res

    def mutate(self, device, additive=False):
        ty = device.device_type

        res = {}

        for name, model in self.mappings.items():
            existing = {e.name: e for e in getattr(device, "{}s".format(name)).all()}
            templates = {e.name: e for e in getattr(ty, "{}_templates".format(name)).all()}
            model.objects.bulk_create([
                v.instantiate(device) for k, v in templates.items()
                if k not in existing
            ])
            if not additive:
                for k, v in existing.items():
                    if k not in templates:
                        v.delete()
                for k, values in self.get_edits(existing, templates).items():
                    to_modify = existing[k]
                    template = templates[k]
                    for v in values:
                        setattr(to_modify, v, getattr(template, v))
                    to_modify.save()

        return res

    def get(self, request, pk=None):
        device = get_object_or_404(Device, pk=pk)

        if not device.device_type:
            messages.warning("Device has no type.")
            return redirect(self.get_return_url(request, device))

        mutations = self.get_mutations(device, additive=request.GET.get("additive"))

        return render(request, 'nautobot_type_reapply/confirm.html', {
            'mutations': mutations,
            'return_url': self.get_return_url(request, device),
            'device': device,
        })

    def post(self, request, pk=None):
        device = get_object_or_404(Device, pk=pk)

        if not device.device_type:
            messages.warning("Device has no type.")
        else:
            self.mutate(device, additive=request.GET.get("additive"))

        return redirect(self.get_return_url(request, device))
