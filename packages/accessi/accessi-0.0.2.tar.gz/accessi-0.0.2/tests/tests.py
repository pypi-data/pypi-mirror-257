"""
Usage example and tests to make sure the library works.
Siemens Access-i simulator should be running for this to work (or real MRI system with appropriate IP-address).
"""
import json
from types import SimpleNamespace

import src as Access
import threading
import asyncio
import time


Access.config.ip_address = "127.0.0.1"
Access.config.version = "v2"

"""
Remote Service
"""
output = Access.Remote.get_is_active().result.success
print(f"get_is_active: {output}")
assert output

output = Access.Remote.get_version().value
print(f"get_version: {output}")
assert output is not None

"""
Authorization Service
"""
output = Access.Authorization.register().result.success
print(f"register: {output}")
assert output is True

output = Access.Authorization.get_is_registered().result.success
print(f"get_is_registered: {output}")
assert output is True

output = Access.Authorization.deregister().result.success
print(f"register: {output}")
assert output is True

output = Access.Authorization.get_is_registered().result.success
print(f"get_is_registered: {output}")
assert output is False

output = Access.Authorization.register().result.success
print(f"register: {output}")

"""
Host Control Service
"""
output = Access.HostControl.get_state().value.canRequestControl
print(f"get_state can request control: {output}")
assert output is True

output = Access.HostControl.request_host_control().result.success
print(f"request_host_control: {output}")
assert output is True

output = Access.HostControl.release_host_control().result.success
print(f"release_host_control: {output}")
assert output is True

output = Access.HostControl.request_host_control().result.success
print(f"request_host_control: {output}")

"""
System Information Service
"""
output = Access.SystemInformation.get_system_info().value
print(f"get_system_info: {output}")
assert output is not None

output = Access.SystemInformation.get_isocenter_position().value
print(f"get_isocenter_position: {output}")
assert output is not None

output = Access.SystemInformation.get_handball_state().value
print(f"get_handball_state: {output}")
assert output is not None

output = Access.SystemInformation.get_serial_number().value
print(f"get_serial_number: {output}")
assert output is not None

"""
Template Execution Service
"""
template = Access.TemplateExecution.get_templates().value[0]
print(f"get_template [0]: {template.label}")
template_id = template.id
assert template_id is not None

output = Access.TemplateExecution.get_state().value.canStart
print(f"get_state can start template: {output}")
assert output is True

Access.TemplateModification.open(template_id)
output = Access.TemplateExecution.start(template_id).result.success
print(f"start: {output}")
assert output is True

output = Access.TemplateExecution.get_remaining_measurement_time_in_seconds().value
print(f"get_remaining_measurement_time_in_seconds: {output}")
assert output is not None

output = Access.TemplateExecution.stop().result.success
print(f"stop: {output}")
assert output is True

Access.TemplateModification.close()

"""
Template Modification Service
"""
output = Access.TemplateModification.get_state()
print(f"template modification get_state: {output}")
assert output is not None

output = Access.TemplateModification.open(template_id).result.success
print(f"open template: {output}")
assert output is True

output = Access.TemplateModification.close().result.success
print(f"close template: {output}")
assert output is True

"""
Parameter Standard Service
"""
output = Access.TemplateModification.open(template_id).result.success
print(f"open template: {output}")
assert output is True

output = Access.ParameterStandard.get_slice_thickness().value
print(f"get_slice_thickness: {output}")
assert output is not None

output = Access.ParameterStandard.set_slice_thickness(15).valueSet
print(f"set_slice_thickness: {output}")
assert output == 15

print("Interactive parameter changing")
output = Access.TemplateExecution.start(template_id).result.success
print(f"start: {output}")
assert output is True

output = Access.ParameterStandard.get_slice_position_dcs()
print(f"get_slice_position_dcs: {output}")
assert output is not None

output = Access.ParameterStandard.set_slice_position_dcs(x=0, y=0, z=10)
print(f"set_slice_position_dcs: {output.valueSet}")
assert output.valueSet.z == 10

output = Access.ParameterStandard.set_slice_thickness(15)
print(f"set_slice_thickness: {output.valueSet}, {output}")
assert output.valueSet == 15

Access.TemplateExecution.stop()

"""
Image Service
"""
output = Access.Image.set_image_format("raw16bit").result.success
print(f"set_image_format: {output}")
assert output is True


async def demo_callback_function(image_data):
    if "imageStream" in image_data:
        image_data = json.loads(json.dumps(image_data), object_hook=lambda d: SimpleNamespace(**d))
        print(f"Websocket callback image dimensions: "
              f"{image_data[2].value.image.dimensions.columns},"
              f"{image_data[2].value.image.dimensions.rows} ")


def run_websocket_in_thread(config, callback_function):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(Access.connect_websocket(config, callback_function))
    except Exception as error:
        print(f"Websocket was unexpectedly closed (this is fine), {error}")


thread = threading.Thread(target=run_websocket_in_thread, args=(Access.config, demo_callback_function))
thread.start()

websocket = Access.Image.connect_to_default_web_socket()
print(f"connect_to_default_web_socket: {websocket}")
assert websocket.result.success is True

output = Access.TemplateExecution.start(template_id).result.success
print(f"start: {output}")
assert output is True

print("Sleeping 5 seconds")
time.sleep(5)

"""
Done, cleanup
"""

Access.TemplateExecution.stop()
Access.TemplateModification.close()
Access.HostControl.release_host_control()
Access.Authorization.deregister()
print("It works!")
SystemExit()
