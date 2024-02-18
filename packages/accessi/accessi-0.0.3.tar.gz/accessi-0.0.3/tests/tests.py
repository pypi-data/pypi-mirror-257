"""
Usage example and tests to make sure the library works.
Siemens Access-i simulator should be running for this to work (or real MRI system with appropriate IP-address).
"""
import json
from asyncio import LifoQueue
from types import SimpleNamespace
from src import accessi as Access
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
# Find interactive template
i = 0
template = Access.TemplateExecution.get_templates().value[i]
while not template.isInteractive:
    i += 1
    template = Access.TemplateExecution.get_templates().value[i]
print(f"get_template [{i}]: {template.label}")
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


async def demo_callback_function(queue: asyncio.Queue):
    while True:
        image_data = await queue.get()
        while not queue.empty():
            await queue.get()
        if "imageStream" in image_data:
            image_data = json.loads(json.dumps(image_data), object_hook=lambda d: SimpleNamespace(**d))
            print(f"Websocket callback image dimensions: "
                  f"{image_data[2].value.image.dimensions.columns},"
                  f"{image_data[2].value.image.dimensions.rows} ")


async def main():
    lifo_queue = LifoQueue()

    # Run websocket
    websocket_connected_event = asyncio.Event()
    asyncio.create_task(Access.connect_websocket(lifo_queue, websocket_connected_event))
    await websocket_connected_event.wait()

    # Connect the image service to websocket
    websocket = Access.Image.connect_to_default_web_socket()
    print(f"connect_to_default_web_socket: {websocket}")
    assert websocket.result.success is True

    # Start template
    output = Access.TemplateExecution.start(template_id).result.success
    print(f"start: {output}")
    assert output is True

    # Start image processing thread
    asyncio.create_task(demo_callback_function(lifo_queue))

    while True:
        await asyncio.sleep(5)

        """
        Done, cleanup
        """
        print("Tests done, cleaning up")
        Access.TemplateExecution.stop()
        Access.TemplateModification.close()
        Access.HostControl.release_host_control()
        Access.Authorization.deregister()
        print("It works!")
        raise SystemExit


print("Running websocket for 5 seconds")
asyncio.run(main())
