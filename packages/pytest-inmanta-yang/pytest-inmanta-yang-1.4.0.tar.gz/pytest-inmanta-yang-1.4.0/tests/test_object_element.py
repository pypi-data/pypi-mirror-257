"""
    Copyright 2022 Inmanta

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Contact: code@inmanta.com
"""

import pytest
from lxml import objectify  # type: ignore

from pytest_inmanta_yang import ObjectElement

COMPLEX_MODEL = """
<data xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
    <configure xmlns="urn:nokia.com:sros:ns:yang:sr:conf">
        <router>
            <router-name>Base</router-name>
            <list-item>First</list-item>
            <list-item>Second</list-item>
            <bgp>
                <group nc:operation="replace">
                    <group-name>Europe</group-name>
                    <vpn-apply-import>true</vpn-apply-import>
                    <family>
                        <vpn-ipv4>true</vpn-ipv4>
                        <vpn-ipv6>true</vpn-ipv6>
                        <evpn>true</evpn>
                    </family>
                </group>
                <group nc:operation="replace">
                    <group-name>Asia</group-name>
                    <vpn-apply-import>true</vpn-apply-import>
                    <family>
                        <vpn-ipv4>true</vpn-ipv4>
                        <vpn-ipv6>true</vpn-ipv6>
                        <evpn>true</evpn>
                    </family>
                </group>
            </bgp>
        </router>
    </configure>
</data>
"""


def test_name_duplicate() -> None:
    cisco_namespace = "http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-bgp-cfg"
    openconfig_namespace = "http://openconfig.net/yang/bgp"
    model = f"""
        <data xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
            <bgp xmlns="{cisco_namespace}">
            </bgp>
            <bgp xmlns="{openconfig_namespace}">
            </bgp>
        </data>
    """
    object_tree = objectify.fromstring(model)
    data_element = ObjectElement(object_tree)

    assert data_element.get_subelement("bgp", cisco_namespace)
    assert data_element.get_subelement("bgp", openconfig_namespace)

    with pytest.raises(Exception) as e:
        data_element.get_subelement("bgp")

    assert (
        "Found multiple elements with similar tags: "
        f"['{{{cisco_namespace}}}bgp', '{{{openconfig_namespace}}}bgp']"
    ) in e.value.args


def test_get_attribute() -> None:
    object_tree = objectify.fromstring(COMPLEX_MODEL)
    data_element = ObjectElement(object_tree)

    router_element = data_element.relations.configure.relations.router
    assert router_element.attributes.router_name == "Base"

    with pytest.raises(AttributeError):
        router_element.relations.router_name


def test_get_relation() -> None:
    object_tree = objectify.fromstring(COMPLEX_MODEL)
    data_element = ObjectElement(object_tree)

    assert data_element.relations.configure is not None

    with pytest.raises(AttributeError):
        data_element.attributes.configure


def test_get_attribute_list() -> None:
    object_tree = objectify.fromstring(COMPLEX_MODEL)
    data_element = ObjectElement(object_tree)

    router_element = data_element.relations.configure.relations.router
    assert router_element.list_attributes.list_item == ["First", "Second"]
    assert router_element.list_relations.list_item == []

    with pytest.raises(Exception) as e:
        router_element.attributes.list_item

    assert "Found multiple elements for tag" in str(e)

    with pytest.raises(AttributeError):
        router_element.relations.list_item


def test_get_relation_list() -> None:
    object_tree = objectify.fromstring(COMPLEX_MODEL)
    data_element = ObjectElement(object_tree)

    bgp_element = data_element.relations.configure.relations.router.relations.bgp
    groups = bgp_element.list_relations.group
    assert len(groups) == 2
    group_names = [group.attributes.group_name for group in groups]
    assert group_names == ["Europe", "Asia"]

    assert bgp_element.list_attributes.group == []

    with pytest.raises(Exception) as e:
        bgp_element.relations.group

    assert "Found multiple elements for tag" in str(e)

    with pytest.raises(AttributeError):
        bgp_element.attributes.group
