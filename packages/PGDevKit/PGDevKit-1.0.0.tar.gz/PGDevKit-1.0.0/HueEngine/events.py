#  Hue Engine ©️
#  2023-2024 Setoichi Yumaden <setoichi.dev@gmail.com>
#
#  This software is provided 'as-is', without any express or implied
#  warranty.  In no event will the authors be held liable for any damages
#  arising from the use of this software.
#
#  Permission is granted to anyone to use this software for any purpose,
#  including commercial applications, and to alter it and redistribute it
#  freely, subject to the following restrictions:
#
#  1. The origin of this software must not be misrepresented; you must not
#     claim that you wrote the original software. If you use this software
#     in a product, an acknowledgment in the product documentation would be
#     appreciated but is not required.
#  2. Altered source versions must be plainly marked as such, and must not be
#     misrepresented as being the original software.
#  3. This notice may not be removed or altered from any source distribution.

from HueEngine.core import pg,sys,_ANY
import HueEngine

class Processor:
    priority = 0

    def Process(self, *args: _ANY, **kwargs: _ANY) -> None: raise NotImplementedError

class CustomEvent:
    def __init__(self, name, **attributes):
        self.name = name
        self.attributes = attributes
        # Generate a unique event type if not already done
        if not hasattr(CustomEvent, 'CUSTOM_EVENT_COUNT'):
            CustomEvent.CUSTOM_EVENT_COUNT = pg.USEREVENT
        self.type = CustomEvent.CUSTOM_EVENT_COUNT
        CustomEvent.CUSTOM_EVENT_COUNT += 1  # Prepare the next unique event type
        self.pgEvent = pg.event.Event(self.type, **attributes)

    def Post(self):
        pg.event.post(self.pgEvent)

class EventSystem:
    def __init__(self) -> None:
        self.quit = 0

    def _GetEvents(self):
        for event in pg.event.get():
            if (event): return event

    def Post(self, event):
        try:
            pg.event.post(event)
        except pg.error as e:
            print(f"Error Posting EVENT: [{event}]. Error: {e}")

    def Emit(self, *args: _ANY, **kwargs: _ANY) -> None:
        event = self._GetEvents()
        if (event):
            [listener(event) for listener in HueEngine.LISTENERS.get(event.type, [])]

def _registerEvent(eventType):
    if (not HueEngine.LISTENERS.__contains__(eventType)): HueEngine.LISTENERS[eventType] = []
    else: return f"Event {eventType} Already Registered!"

def registerListenerRAW(eventType, listener:_ANY):
    _registerEvent(eventType)
    if (not HueEngine.LISTENERS[eventType].__contains__(listener)): HueEngine.LISTENERS[eventType].append(listener)
    else: return f"Listener {listener} Already Registered!"

def registerListener(event_type):
    def decorator(listener_function):
        # Register the listener function for the specified event type
        _registerEvent(event_type)  # Ensure the event type is registered
        if listener_function not in HueEngine.LISTENERS[event_type]:
            HueEngine.LISTENERS[event_type].append(listener_function)
        else:
            print(f"Warning: Listener {listener_function.__name__} is already registered for event {event_type}.")

        return listener_function
    return decorator

def QuitListener(event:_ANY) -> None:
    if (event.type == HueEngine.QUIT):
        pg.quit()
        sys.exit()

def registerProcessorRAW(processor:_ANY, stage:str="Fixed"):
    if (not HueEngine.PROCESSORS[stage].__contains__(processor)):
        HueEngine.PROCESSORS[stage].append(processor)

def registerProcessor(stage, priority):
    def decorator(processor):
        if isinstance(processor, type):
            # It's a class, instantiate it and set priority
            instance = processor()
            instance.priority = priority
            if (not HueEngine.PROCESSORS[stage].__contains__(processor)):
                HueEngine.PROCESSORS[stage].append(processor)
        else:
            # Wrap the function in a class to maintain consistency
            class FunctionProcessorWrapper:
                def __init__(self, func):
                    self.func = func

                def Process(self, *args, **kwargs):
                    return self.func(*args, **kwargs)

            # Assign the priority to the wrapper class instance
            wrapper = FunctionProcessorWrapper(processor)
            wrapper.priority = priority

            if (not HueEngine.PROCESSORS[stage].__contains__(wrapper)):
                HueEngine.PROCESSORS[stage].append(wrapper)

        return processor
    return decorator

