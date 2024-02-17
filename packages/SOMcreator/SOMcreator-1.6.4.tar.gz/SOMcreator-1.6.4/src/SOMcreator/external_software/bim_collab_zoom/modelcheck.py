from __future__ import annotations

import datetime
import logging
import os
import uuid

from lxml import etree

from ...constants import value_constants
from ... import classes
from . import condition as c
from . import constants as const
from . import rule

REQUIRED_DATA_DICT = dict[classes.Object, dict[classes.PropertySet, list[classes.Attribute]]]

def _write_header(xml_header: etree.Element) -> None:
    etree.SubElement(xml_header, const.VERSION).text = "6"
    etree.SubElement(xml_header, const.APPVER).text = "Win - Version: 6.8 (build 6.8.26.0)"


def _write_smartview(property_set: classes.PropertySet, attribute_list: list[classes.Attribute],
                     author: str) -> etree.Element:
    def write_smartview_basics():
        sv = etree.Element(const.SVIEW)
        etree.SubElement(sv, const.TITLE).text = property_set.name
        etree.SubElement(sv, const.DESCRIPTION).text = f"Checks {property_set.name} for correct Values"
        etree.SubElement(sv, const.CREATOR).text = "christoph.mellueh@deutschebahn.com"
        etree.SubElement(sv, const.CREATIONDATE).text = str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
        etree.SubElement(sv, const.MODIFIER).text = author
        etree.SubElement(sv, const.MODIFICATIONDATE).text = str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
        etree.SubElement(sv, const.GUID).text = str(uuid.uuid4())
        return sv

    xml_smart_view = write_smartview_basics()
    xml_rules = etree.SubElement(xml_smart_view, const.RULES)
    pset_name = property_set.name
    ident_attrib = property_set.object.ident_attrib
    rule_list: list[etree.Element] = list()

    for attribute in attribute_list:
        if attribute == ident_attrib:
            continue
        if attribute.data_type in (value_constants.INTEGER, value_constants.REAL):
            if not attribute.value:
                rule_list += rule.add_if_not_existing(attribute.name, pset_name, c.DATATYPE_DICT[attribute.data_type])
            elif attribute.value_type == value_constants.LIST:
                rule_list += rule.numeric_list(attribute.name, pset_name, attribute.value)
            elif attribute.value_type == value_constants.RANGE:
                rule_list += rule.numeric_range(attribute.name, pset_name, attribute.value)
            else:
                logging.error(f"No Function defined for {attribute.name} ({attribute.value_type}x{attribute.data_type}")

        elif attribute.data_type == value_constants.LABEL:
            if attribute.value_type == value_constants.FORMAT:
                rule_list += rule.add_if_not_existing(attribute.name, pset_name, c.DATATYPE_DICT[attribute.data_type])
                continue

            if attribute.value:
                rule_list += rule.add_if_not_in_string_list(attribute.name, pset_name, attribute.value)
            else:
                rule_list += rule.add_if_not_existing(attribute.name, pset_name, c.DATATYPE_DICT[attribute.data_type])

        elif attribute.data_type == value_constants.BOOLEAN:
            rule_list += rule.add_if_not_existing(attribute.name, pset_name, c.DATATYPE_DICT[attribute.data_type])
        else:
            logging.error(f"No Function defined for {attribute.name} ({attribute.value_type}x{attribute.data_type}")

    rule_list += rule.remove_if_not_in_string_list(ident_attrib.name, ident_attrib.property_set.name,
                                                   ident_attrib.value)
    for xml_rule in rule_list:
        xml_rules.append(xml_rule)
    return xml_smart_view


def _write_smartviewset(obj: classes.Object, pset_dict: dict[classes.PropertySet, list[classes.Attribute]],
                        author: str) -> etree.Element:
    smartview_set = etree.Element(const.SMVSET)
    etree.SubElement(smartview_set, const.TITLE).text = obj.name
    etree.SubElement(smartview_set, const.DESCRIPTION).text = "generated by SOMcreator"
    etree.SubElement(smartview_set, const.GUID).text = str(uuid.uuid4())
    etree.SubElement(smartview_set, const.MODIFICATIONDATE).text = str(
        datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
    smartviews = etree.SubElement(smartview_set, const.SVIEWS)

    for property_set, attribute_list in pset_dict.items():
        smartviews.append(_write_smartview(property_set, attribute_list, author))
    return smartview_set


def _write_smartviewsets(required_data_dict:REQUIRED_DATA_DICT,
                         author: str) -> etree.Element:
    smartviewsets = etree.Element(const.SMVSETS)
    for obj, pset_dict in required_data_dict.items():
        if obj.is_concept:
            continue
        smartviewsets.append(_write_smartviewset(obj, pset_dict, author))
    return smartviewsets


def export(required_data_dict: REQUIRED_DATA_DICT,
           save_path: os.PathLike | str, author="") -> None:
    header = etree.Element(const.BCSVF)
    _write_header(header)
    svs = _write_smartviewsets(required_data_dict, author)

    with open(save_path, "wb") as file:
        file.write(etree.tostring(header, pretty_print=True))
        file.write(etree.tostring(svs, pretty_print=True))

def build_full_required_data_dict(project:classes.Project)-> REQUIRED_DATA_DICT:
    required_data = dict()
    for obj in list(project.objects):
        required_data[obj] = dict()
        for pset in obj.property_sets:
            required_data[obj][pset] = [attribute for attribute in pset.attributes]
    return required_data