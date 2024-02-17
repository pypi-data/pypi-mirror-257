import json
import os
import uuid
from datetime import datetime

from adminboundarymanager.models import AdminBoundarySettings
from django.conf import settings
from django.contrib.gis.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from shapely.geometry import shape
from wagtail import blocks
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.admin.panels import MultiFieldPanel, FieldPanel, InlinePanel
from wagtail.contrib.settings.models import BaseSiteSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.fields import StreamField
from wagtail.models import Page, Site, Orderable
from wagtailiconchooser.widgets import IconChooserWidget

from capeditor.blocks import (
    AlertInfo,
    AudienceTypeBlock,
    SENDER_NAME_HELP_TEXT,
    CONTACT_HELP_TEXT,
    AUDIENCE_HELP_TEXT,
    AlertAddress,
    AlertReference,
    AlertIncident,
    ContactBlock
)
from capeditor.constants import SEVERITY_MAPPING, URGENCY_MAPPING, CERTAINTY_MAPPING
from capeditor.forms.widgets import HazardEventTypeWidget
from capeditor.shareable.png import cap_geojson_to_image, CapAlertCardImage


@register_setting
class CapSetting(BaseSiteSetting, ClusterableModel):
    sender = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("CAP Sender Identifier"),
                              help_text=_("Can be the website link or email of the sending institution"))
    sender_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("CAP Sender Name"),
                                   help_text=_("Name of the sending institution"))
    logo = models.ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+",
                             verbose_name=_("Logo of the sending institution"))

    contacts = StreamField([
        ("contact", ContactBlock(label=_("Contact")))
    ], use_json_field=True, blank=True, null=True, verbose_name=_("Contact Details"),
        help_text=_("Contact for follow-up and confirmation of the alert message"))

    audience_types = StreamField([
        ("audience_type", AudienceTypeBlock(label=_("Audience Type")))
    ], use_json_field=True, blank=True, null=True, verbose_name=_("Audience Types"),
        help_text=_("Target audiences for published alerts"))

    class Meta:
        verbose_name = _("CAP Settings")

    panels = [
        FieldPanel("sender_name"),
        FieldPanel("sender"),
        FieldPanel("logo"),
        FieldPanel("contacts"),
        InlinePanel("hazard_event_types", heading=_("Hazard Types"), label=_("Hazard Type"),
                    help_text=_("Hazards monitored by the institution")),
        FieldPanel("audience_types"),
    ]


class HazardEventTypes(Orderable):
    setting = ParentalKey(CapSetting, on_delete=models.PROTECT, related_name="hazard_event_types")
    is_in_wmo_event_types_list = models.BooleanField(default=True,
                                                     verbose_name=_("Select from WMO list of Hazards Event Types"))
    event = models.CharField(max_length=255, unique=True, verbose_name=_("Hazard"), help_text=_("Name of Hazard"))
    icon = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Icon"), help_text=_("Matching icon"))

    panels = [
        FieldPanel("is_in_wmo_event_types_list"),
        FieldPanel("event", widget=HazardEventTypeWidget),
        FieldPanel("icon", widget=IconChooserWidget),
    ]

    def __str__(self):
        return self.event


def get_cap_setting():
    try:
        site = Site.objects.get(is_default_site=True)
        if site:
            return CapSetting.for_site(site)
    except Exception:
        pass
    return None


def get_default_sender():
    cap_setting = get_cap_setting()
    if cap_setting and cap_setting.sender:
        return cap_setting.sender
    return None


class CapAlertPageForm(WagtailAdminPageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        cap_setting = get_cap_setting()

        # the following code gets pres-saved common options from settings and
        # makes presents them as selectable dropdowns instead of the composer to type each time
        # they are creating a new alert
        if cap_setting:
            default_sender_name = cap_setting.sender_name
            contacts = cap_setting.contacts
            audience_types = cap_setting.audience_types

            if default_sender_name:
                info_field = self.fields.get("info")
                for block_type, block in info_field.block.child_blocks.items():
                    if block_type == "alert_info":
                        field_name = "senderName"
                        sender_block = info_field.block.child_blocks[block_type].child_blocks[field_name]

                        label = sender_block.label or field_name
                        name = sender_block.name

                        info_field.block.child_blocks[block_type].child_blocks[field_name] = blocks.CharBlock(
                            default=default_sender_name, required=False, help_text=SENDER_NAME_HELP_TEXT)
                        info_field.block.child_blocks[block_type].child_blocks[field_name].name = name
                        info_field.block.child_blocks[block_type].child_blocks[field_name].label = label

            if contacts:
                contact_choices = []
                for block in contacts:
                    contact = block.value.get("contact")
                    contact_choices.append((contact, contact))

                info_field = self.fields.get("info")
                for block_type, block in info_field.block.child_blocks.items():
                    if block_type == "alert_info":
                        field_name = "contact"
                        contact_block = info_field.block.child_blocks[block_type].child_blocks[field_name]

                        label = contact_block.label or field_name
                        name = contact_block.name

                        info_field.block.child_blocks[block_type].child_blocks[field_name] = blocks.ChoiceBlock(
                            choices=contact_choices, required=False, help_text=CONTACT_HELP_TEXT)
                        info_field.block.child_blocks[block_type].child_blocks[field_name].name = name
                        info_field.block.child_blocks[block_type].child_blocks[field_name].label = label

            if audience_types:
                audience_type_choices = []

                for block in audience_types:
                    audience = block.value.get("audience")
                    audience_type_choices.append((audience, audience))

                info_field = self.fields.get("info")
                for block_type, block in info_field.block.child_blocks.items():
                    if block_type == "alert_info":
                        field_name = "audience"
                        audience_block = info_field.block.child_blocks[block_type].child_blocks[field_name]
                        label = audience_block.label or field_name
                        name = audience_block.name
                        info_field.block.child_blocks[block_type].child_blocks[field_name] = blocks.ChoiceBlock(
                            choices=audience_type_choices, required=False, help_text=AUDIENCE_HELP_TEXT)
                        info_field.block.child_blocks[block_type].child_blocks[field_name].name = name
                        info_field.block.child_blocks[block_type].child_blocks[field_name].label = label


class AbstractCapAlertPage(Page):
    base_form_class = CapAlertPageForm

    exclude_fields_in_copy = ["identifier"]

    STATUS_CHOICES = (
        ("Draft", _("Draft - A preliminary template or draft, not actionable in its current form")),
        ("Actual", _("Actual - Actionable by all targeted recipients")),
        ("Test", _("Test - Technical testing only, all recipients disregard")),
        ("Exercise", _("Exercise - Actionable only by designated exercise participants; "
                       "exercise identifier SHOULD appear in note")),
        ("system", _("System - For messages that support alert network internal functions")),
    )

    MESSAGE_TYPE_CHOICES = (
        ('Alert', _("Alert - Initial information requiring attention by targeted recipients")),
        ('Update', _("Update - Updates and supersedes the earlier message(s) identified in referenced alerts")),
        ('Cancel', _("Cancel - Cancels the earlier message(s) identified in references")),
        ('Ack', _("Acknowledge - Acknowledges receipt and acceptance of the message(s) "
                  "identified in references field")),
        ('Error', _("Error -  Indicates rejection of the message(s) identified in references; "
                    "explanation SHOULD appear in note field")),
    )

    SCOPE_CHOICES = (
        ('Public', _("Public - For general dissemination to unrestricted audiences")),
        ('Restricted', _("Restricted - For dissemination only to users with a known operational "
                         "requirement as in the restriction field")),
        ('Private', _("Private - For dissemination only to specified addresses"
                      " as in the addresses field in the alert")),
    )

    identifier = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name=_("Identifier"),
                                  help_text=_("Unique ID. Auto generated on creation."), unique=True)
    sender = models.CharField(max_length=255, verbose_name=_("Sender"), default=get_default_sender,
                              help_text=_("Identifies the originator of an alert. "
                                          "For example the website address of the institution"))
    sent = models.DateTimeField(default=timezone.now, verbose_name=_("Sent"),
                                help_text=_("Time and date of origination of the alert"))
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Actual", verbose_name=_("Status"),
                              help_text=_("The code denoting the appropriate handling of the alert"))
    msgType = models.CharField(max_length=100, choices=MESSAGE_TYPE_CHOICES, default="Alert",
                               verbose_name=_("Message Type"),
                               help_text=_("The code denoting the nature of the alert message"))
    scope = models.CharField(max_length=100, choices=SCOPE_CHOICES, default="Public", verbose_name=_("Scope"),
                             help_text=_("The code denoting the intended distribution of the alert message"))
    source = models.TextField(blank=True, null=True, verbose_name=_("Source"),
                              help_text=_("The text identifying the source of the alert message"))
    restriction = models.TextField(blank=True, null=True,
                                   help_text=_("The text describing the rule for limiting distribution of the "
                                               "restricted alert message. Used when scope value is Restricted"),
                                   verbose_name=_("Restriction"))
    code = models.CharField(max_length=100, blank=True, null=True,
                            help_text=_("The code denoting the special handling of the alert message"),
                            verbose_name=_("Code"))
    note = models.TextField(blank=True, null=True,
                            help_text=_("The text describing the purpose or significance of the alert message."
                                        "The message note is primarily intended for use with "
                                        "<status> 'Exercise' and <msgType> 'Error'"), verbose_name=_("Note"))
    info = StreamField([
        ("alert_info", AlertInfo(label=_("Alert Information")))
    ], block_counts={
        'alert_info': {'min_num': 1},
    }, use_json_field=True, blank=True,
        null=True, verbose_name=_("Alert Information"), )

    addresses = StreamField([
        ("recipient", AlertAddress(label=_("Recipient")))
    ], use_json_field=True, blank=True,
        null=True, verbose_name=_("Addresses"),
        help_text=_("The group listing of intended recipients of the alert message, if scope is Private"))

    references = StreamField([
        ("reference", AlertReference(label=_("Reference Alert")))
    ], use_json_field=True, blank=True,
        null=True, verbose_name=_("Reference Alerts"))

    incidents = StreamField([
        ("incident", AlertIncident(label=_("Incident")))
    ], use_json_field=True, blank=True,
        null=True, verbose_name=_("Incidents"))

    class Meta:
        abstract = True

    content_panels = [
        MultiFieldPanel([
            FieldPanel('sender'),
            FieldPanel('sent'),
            FieldPanel('status'),
            FieldPanel('msgType'),
            FieldPanel("references", classname="cap-alert__panel-references"),
            FieldPanel('note', classname="cap-alert__panel-note"),
            FieldPanel('scope'),
            FieldPanel('restriction', classname="cap-alert__panel-restriction"),
        ], heading=_("Alert Identification")),
        FieldPanel("addresses", classname="cap-alert__panel-addresses"),
        FieldPanel("info"),
        FieldPanel("incidents"),
    ]

    @cached_property
    def feature_collection(self):
        fc = {"type": "FeatureCollection", "features": []}
        for info in self.info:
            if info.value.features:
                for feature in info.value.features:
                    feature.get("properties", {}).update({"info-id": info.id})
                    fc["features"].append(feature)
        return fc

    @cached_property
    def geojson(self):
        return json.dumps(self.feature_collection)

    @cached_property
    def bounds(self):
        geojson_data = self.feature_collection
        bounds = None
        for feature in geojson_data['features']:
            geometry = shape(feature['geometry'])
            if bounds is None:
                bounds = geometry.bounds
            else:
                bounds = (
                    min(bounds[0], geometry.bounds[0]),
                    min(bounds[1], geometry.bounds[1]),
                    max(bounds[2], geometry.bounds[2]),
                    max(bounds[3], geometry.bounds[3])
                )

        return list(bounds)

    @property
    def xml_link(self):
        return None

    @cached_property
    def infos(self):
        alert_infos = []
        for info in self.info:
            start_time = info.value.get("effective") or self.sent

            if info.value.get('expires').date() < datetime.today().date():
                status = "Expired"
            elif timezone.now() > start_time:
                status = "Ongoing"
            else:
                status = "Expected"

            area_desc = [area.get("areaDesc") for area in info.value.area]
            area_desc = ", ".join(area_desc)

            event = f"{info.value.get('event')} ({area_desc})"
            severity = SEVERITY_MAPPING[info.value.get("severity")]
            urgency = URGENCY_MAPPING[info.value.get("urgency")]
            certainty = CERTAINTY_MAPPING[info.value.get("certainty")]

            effective = start_time
            expires = info.value.get('expires')
            url = self.url
            event_icon = info.value.event_icon

            alert_info = {
                "info": info,
                "status": status,
                "url": self.url,
                "event": event,
                "event_icon": event_icon,
                "severity": severity,
                "utc": start_time,
                "urgency": urgency,
                "certainty": certainty,
                "effective": effective,
                "expires": expires,
                "properties": {
                    "id": self.identifier,
                    "event": event,
                    "event_type": info.value.get('event'),
                    "headline": info.value.get("headline"),
                    "severity": info.value.get("severity"),
                    "urgency": info.value.get("urgency"),
                    "certainty": info.value.get("certainty"),
                    "severity_color": severity.get("color"),
                    "sent": self.sent,
                    "onset": info.value.get("onset"),
                    "expires": expires,
                    "web": url,
                    "description": info.value.get("description"),
                    "instruction": info.value.get("instruction"),
                    "event_icon": event_icon,
                    "area_desc": area_desc,
                }
            }

            alert_infos.append(alert_info)

        return alert_infos

    def get_geojson_features(self, request=None):
        features = []
        for info_item in self.infos:
            info = info_item.get("info")
            if info.value.geojson:
                properties = info_item.get("properties")
                if request:
                    web = request.build_absolute_uri(properties.get("web"))
                    properties.update({
                        "web": web
                    })

                info_features = info.value.features
                for feature in info_features:
                    feature["properties"].update(**properties)
                    features.append(feature)

        return features

    def generate_alert_card_image(self):

        site = Site.objects.get(is_default_site=True)

        abm_settings = AdminBoundarySettings.for_site(site)
        cap_settings = CapSetting.for_site(site)
        abm_extents = abm_settings.combined_countries_bounds

        info = self.infos[0]

        features = self.get_geojson_features()
        if features:
            feature_coll = {
                "type": "FeatureCollection",
                "features": features,
            }

            if abm_extents:
                # format to what matplotlib expects
                abm_extents = [abm_extents[0], abm_extents[2], abm_extents[1], abm_extents[3]]

            cap_detail = {
                "title": self.title,
                "event": info.get("event"),
                "sent_on": self.sent,
                "org_name": cap_settings.sender_name,
                "severity": info.get("severity"),
                "properties": info.get("properties"),
            }

            org_logo = cap_settings.logo
            if org_logo:
                cap_detail.update({
                    "org_logo_file": os.path.join(settings.MEDIA_ROOT, org_logo.file.path)
                })

                map_img_buffer = cap_geojson_to_image(feature_coll, abm_extents)

                image_content_file = CapAlertCardImage(map_img_buffer, cap_detail,
                                                       f"{self.identifier}.png").render()

                return image_content_file

        return None
