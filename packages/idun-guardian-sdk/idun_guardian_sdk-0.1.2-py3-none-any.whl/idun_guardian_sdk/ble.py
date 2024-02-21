import simplepyble
import platform
from typing import Callable, Union


UUID_SERVICE: str = "beffd56c-c915-48f5-930d-4c1feee0fcc3"
UUID_ID: str = "beffd56c-c915-48f5-930d-4c1feee0fccb"
UUID_MEAS_EEGIMU: str = "beffd56c-c915-48f5-930d-4c1feee0fcc4"
UUID_CMD: str = "beffd56c-c915-48f5-930d-4c1feee0fcca"
START_CMD: str = "M"  #'\x62' #b -> start measurement
STOP_CMD: str = "S"  # '\x73' #s -> stop measurement
START_IMP_CMD: str = "Z"  # '\x7a' #z -> start impedance
STOP_IMP_CMD: str = "X"  # '\x78' #x -> stop impedance
UUID_MEAS_IMP: str = "beffd56c-c915-48f5-930d-4c1feee0fcc8"
UUID_BATTERY_SERVICE: str = "0000180f-0000-1000-8000-00805f9b34fb"
UUID_BATTERY_ID: str = "00002a19-0000-1000-8000-00805f9b34fb"


class GuardianBLE:
    """Bluetooth Low Energy Class.

    Handles communication to Guardian Earbuds over BLE.

    Todo:
        Not yet implemented:

        * LED on/off
        * Change Z filter setting
    """

    _device_id = None
    _adapter = None
    _peripheral = None
    is_recording_eeg = False
    is_recording_impedance = False
    is_recording_battery = False
    _data_callback = None
    _impedance_callback = None
    _battery_callback = None
    _mac = None

    def __init__(self, device_id=None):
        """*Constructor*

        Args:
            device_id: Optional. Autoconnect to the passed device.
                If not specified, the class will show an interactive selector if more than one device is found.

        Caution:
            deviceID is *not* the Earbud MAC address on macOS!
        """
        if device_id:
            self._device_id = device_id.replace("-", ":").lower()
        self._adapter = self._set_adapter()
        self._connect()
        self.is_recording_eeg = False

    def __del__(self):
        self._disconnect()

    def _set_adapter(self):
        adapters = simplepyble.Adapter.get_adapters()
        if len(adapters) == 0:
            print("No adapters found")
            return False

        choice = None
        if len(adapters) > 1:
            # Query the user to pick an adapter
            print("Please select an adapter:")
            for i, adapter in enumerate(adapters):
                print(f"{i}: {adapter.identifier()} [{adapter.address()}]")
            choice = int(input("Enter choice: "))
        adapter = adapters[choice or 0]
        print(f"Selected adapter: {adapter.identifier()} [{adapter.address()}]")
        # adapter.set_callback_on_scan_start(lambda: print("Scan started."))
        # adapter.set_callback_on_scan_stop(lambda: print("Scan complete."))
        return adapter

    def _connect(self):
        if self._peripheral:
            return
        # Scan for 2.5 seconds
        self._adapter.scan_for(2500)
        peripherals = self._adapter.scan_get_results()

        igebs = (
            list(
                filter(
                    lambda peripheral: (peripheral.address() == self._device_id)
                    if self._device_id
                    else (peripheral.identifier() == "IGEB"),
                    peripherals,
                )  # TODO: move magic str to constant/config
            )
            if platform.system() != "Darwin"
            else list(
                filter(
                    lambda peripheral: (peripheral.identifier() == "IGEB"), peripherals
                )
            )
        )
        # TODO: on macos, try to get deviceID from additional characteristic

        choice = None
        if len(igebs) != 1:
            # Query the user to pick a peripheral
            print("Please select a peripheral:")
            for i, peripheral in enumerate(igebs):
                print(f"{i}: {peripheral.identifier()} [{peripheral.address()}]")
            choice = int(input("Enter choice: "))

        self._peripheral = igebs[choice or 0]
        self._peripheral.set_callback_on_disconnected(self._on_disconnected())
        self._peripheral.set_callback_on_connected(self._on_connected())

        print(
            f"Connecting to: {self._peripheral.identifier()} [{self._peripheral.address()}]"
        )
        self._peripheral.connect()
        self._device_id = self._peripheral.address()

        if platform.system() == "Darwin":
            id_str = self._peripheral.read(UUID_SERVICE, UUID_ID)
            self._mac = id_str.decode("utf-8").replace(":", "-")
        else:
            self._mac = self._peripheral.address().replace(":", "-")

    @property
    def device_id(self):
        """MAC Address of Guardian device.
        """
        return self._mac.upper()  # needs to be uppercase for the API

    def _on_connected(self):
        def _connect():
            print("connected")
            self._restore_state()

        return _connect

    def _on_disconnected(self):
        def _reconnect():
            print("disconnected")
            self._peripheral.connect()

        return _reconnect

    def _disconnect(self):
        if not self._peripheral:
            return
        self._peripheral.set_callback_on_disconnected(lambda: None)
        self._peripheral.set_callback_on_connected(lambda: None)
        self._peripheral.disconnect()
        self._peripheral = None

    def start_recording(self, callback: Union[Callable[[bytes], None], None]):
        """Start data stream from Guardian device.

        Hint:
            In normal operation, the callback should be set to :meth:`GuardianAPI.callback`

            .. code-block:: python

                ble = GuardianBLE()
                api = GuardianAPI(...)
                api.start_recording(...)
                ble.start_recording(api.callback)

        Args:
            callback: Always pass :meth:`GuardianAPI.callback` for normal operation.
        """
        self._data_callback = callback
        contents = self._peripheral.notify(
            UUID_SERVICE, UUID_MEAS_EEGIMU, lambda data: self._data_callback(data)
        )
        self._peripheral.write_command(
            UUID_SERVICE, UUID_CMD, START_CMD.encode("ascii")
        )
        self.is_recording_eeg = True

    def stop_recording(self):
        """Stop data stream from Guardian device. Also clears any callback.
        """
        # TODO: check if actually still connected
        self._peripheral.write_command(UUID_SERVICE, UUID_CMD, STOP_CMD.encode("ascii"))
        try:
            self._peripheral.unsubscribe(UUID_SERVICE, UUID_MEAS_EEGIMU)
        except:
            pass
        self.is_recording_eeg = False
        self._data_callback = None

    def start_impedance(self, callback: Union[Callable[[int], None], None]):
        """Start impedance measurement on Guardian device.

        Args:
            callback: Function to call on reception of impedance value.
        """
        # TODO: notch filter selection
        self._impedance_callback = callback
        contents = self._peripheral.notify(
            UUID_SERVICE,
            UUID_MEAS_IMP,
            lambda data: self._impedance_callback(self._zconv(data)),
        )
        self._peripheral.write_command(
            UUID_SERVICE, UUID_CMD, START_IMP_CMD.encode("ascii")
        )
        self.is_recording_impedance = True

    def stop_impedance(self):
        """Stop impedance measurement.
        """
        self._peripheral.write_command(
            UUID_SERVICE, UUID_CMD, STOP_IMP_CMD.encode("ascii")
        )
        self._peripheral.unsubscribe(UUID_SERVICE, UUID_MEAS_IMP)
        self.is_recording_impedance = False
        self._impedance_callback = None

    def get_battery(self) -> int:
        """Read current battery level of Guardian device.

        Returns:
            Battery level (percent).
        """
        contents = self._peripheral.read(UUID_BATTERY_SERVICE, UUID_BATTERY_ID)
        return int.from_bytes(contents, byteorder="little")

    def start_battery(self, callback: Union[Callable[[int], None], None]):
        """Start continuous battery level monitoring.

        Args:
            callback: Function to call on battery level update.
        """
        self._battery_callback = callback
        self._peripheral.notify(
            UUID_BATTERY_SERVICE,
            UUID_BATTERY_ID,
            lambda data: self._battery_callback(
                int.from_bytes(data, byteorder="little")
            ),
        )
        self.is_recording_battery = True

    def stop_battery(self):
        """Stop continuous battery level monitoring. Also clears any callback.
        """
        self._peripheral.unsubscribe(UUID_BATTERY_SERVICE, UUID_BATTERY_ID)
        self.is_recording_battery = False
        self._battery_callback = None

    def _restore_state(self):
        if self.is_recording_eeg:
            self.start_recording(self._data_callback)

        if self.is_recording_impedance:
            self.start_impedance(self._impedance_callback)

        if self.is_recording_battery:
            self.start_battery(self._battery_callback)

    def _zconv(self, data):
        return int.from_bytes(data, byteorder="little")
