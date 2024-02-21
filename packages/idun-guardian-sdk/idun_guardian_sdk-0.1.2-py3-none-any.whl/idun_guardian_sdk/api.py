import os
import warnings
from requests.auth import AuthBase
from datetime import datetime, timezone, timedelta
import uuid
import requests
import websocket
import certifi
import time
import threading
import json
import base64
from typing import Callable, Union


WS_IDENTIFIER: str = "wss://wpcg36nil5.execute-api.eu-central-1.amazonaws.com/v1/"
REST_API_LOGIN: str = "https://d3pq71txhb.execute-api.eu-central-1.amazonaws.com"


class TokenAuth(AuthBase):
    def __init__(self, token, auth_scheme="Bearer"):
        self.token = token
        self.auth_scheme = auth_scheme

    def __call__(self, request):
        request.headers["Authorization"] = f"{self.auth_scheme} {self.token}"
        return request


class GuardianAPI:
    """API Class.

    Handles communication with the Guardian cloud API.

    Todo:
        Not yet implemented:

        * Fetch single recording info
        * Fetch more than 200 recordings
    """

    def __init__(self, device_id: str, api_key: str = None):
        """*Constructor*

        Args:
            device_id: MAC address as written on sticker on device.
            api_key: Optional. Can also be specified via IDUN_API_KEY environment variable.

        Raises:
            Exception: _description_
        """
        self.wsa = None
        self.ongoing_recording_id = None
        self.start_time = datetime.now(timezone.utc)
        self.device_id: str = device_id
        self.package_counter = 0
        self.increment = timedelta(milliseconds=80)
        self._rt_callback = None

        if api_key:
            self.api_key = api_key
        else:
            self.api_key = os.environ.get("IDUN_API_KEY")
        if not self.api_key:
            raise Exception("Missing API Key")

    def start_recording(
        self,
        callback: Union[Callable[[dict], None], None] = None,
        filtered_stream: bool = False,
        raw_stream: bool = False,
    ) -> str:
        """Register a recording on the cloud.

        Args:
            callback: Callback function to be executed on data reception. Is only ever called if at least one of the following parameters is set to True.
            filtered_stream: Enable filtered data stream.
            raw_stream: Enable raw data stream.

        Returns:
            ID of new recording

        """
        self.ongoing_recording_id = "pl-" + str(uuid.uuid4())
        myobj = {
            "recordingID": self.ongoing_recording_id,
            "deviceID": self.device_id,
            "displayName": self.ongoing_recording_id,
            "config": {
                "data_stream_subscription": {
                    "bp_filter_eeg": filtered_stream == True,
                    "raw_eeg": raw_stream == True,
                }
            },
        }
        x = requests.post(
            REST_API_LOGIN + f"/devices/{self.device_id}/recordings",
            json=myobj,
            auth=TokenAuth(token=self.api_key, auth_scheme=""),
        )
        # print(x.text)
        # websocket.enableTrace(True)
        # TODO: handle ongoing recording
        self.wsa = websocket.WebSocketApp(
            WS_IDENTIFIER + "?authorization=" + self.api_key,
            on_message=self._ws_filter(callback),
        )  # TODO: auto reconnect

        sslopt = {"ca_certs": certifi.where()}
        self.wst = threading.Thread(
            target=self.wsa.run_forever, kwargs={"sslopt": sslopt}
        )
        self.wst.daemon = True
        self.wst.start()
        while not self.wsa.sock:
            time.sleep(0.1)
        while not self.wsa.sock.connected:
            time.sleep(0.1)
        return self.ongoing_recording_id

    def stop_recording(self, recording_id: str = None):
        """Finalize an ongoing recording.

        Args:
            recording_id: Optional. Defaults to most recently started recording during object lifetime.
        """
        if recording_id:
            self.ongoing_recording_id = recording_id
        myobj = {"stopped": "true"}
        x = requests.put(
            REST_API_LOGIN
            + f"/devices/{self.device_id}/recordings/{self.ongoing_recording_id}/status",
            json=myobj,
            auth=TokenAuth(token=self.api_key, auth_scheme=""),
        )
        # print(x.text)
        self.wsa.close()
        self.wst.join(timeout=10)
        self.ongoing_recording_id = None

    def get_recordings(self) -> list:
        """Get list of recordings.

        Returns:
            _description_
        """
        warnings.warn("Currently only returns first 200 recordings.", Warning)
        x = requests.get(
            REST_API_LOGIN + f"/devices/{self.device_id}/recordings",
            headers={"accept": "application/json"},
            auth=TokenAuth(token=self.api_key, auth_scheme=""),
            params={
                "limit": "200"
            },  # cursor={recordingID}, filter_status=[NOT_STARTED, ONGOING, PROCESSING, COMPLETED, FAILED]
        )
        return json.loads(x.text)
        # print(x.text)

    def download_recording(
        self,
        recording_id: str,
        filename: str = None,
        eeg: bool = True,
        imu: bool = False,
        sleep_report: bool = False,
    ) -> bool:
        """Download recording data. Only available after finalization.

        Args:
            recording_id: _description_
            filename: _description_. Defaults to None.
            eeg: _description_. Defaults to True.
            imu: _description_. Defaults to False.
            sleep_report: _description_. Defaults to False.

        Returns:
            True if successful, else False.
        """
        # TODO: add timeout
        if not filename:
            filename = recording_id

        s = True
        if eeg:
            s &= self._download_file(recording_id, filename + "_eeg.csv", type="eeg")
        if imu:
            s &= self._download_file(recording_id, filename + "_imu.csv", type="imu")
        if sleep_report:
            self._download_file(
                recording_id,
                filename + "_sleep_report-v0.2.2-EXPERIMENTAL.pdf",
                type="sleep_report/v0.2.2-EXPERIMENTAL",
            )

        return s

    def delete_recording(self, recording_id: str):
        """Delete a recording.

        Args:
            recording_id: _description_
        """
        x = requests.delete(
            REST_API_LOGIN + f"/devices/{self.device_id}/recordings/{recording_id}",
            headers={"accept": "application/json"},
            auth=TokenAuth(token=self.api_key, auth_scheme=""),
        )
        # print(x.text)

    def _download_file(self, recording_id: str, filename: str, type="eeg"):
        x = requests.get(
            REST_API_LOGIN
            + f"/devices/{self.device_id}/recordings/{recording_id}/download/{type}",
            headers={"accept": "application/json"},
            auth=TokenAuth(token=self.api_key, auth_scheme=""),
        )
        res = json.loads(x.text)
        url = res.get("url")
        # TODO: check if url is valid
        if url:
            r = requests.get(url, allow_redirects=True)
            open(filename, "wb").write(r.content)
            return True
        else:
            return False

    @property
    def callback(self):
        """To be passed to :meth:`GuardianBLE.start_recording` as data callback."""

        def _callback(data):
            if self.package_counter == 0:
                self.start_time = datetime.now(timezone.utc)
            self.package_counter += 1

            calculated_time = self.start_time + self.package_counter * self.increment
            time_diff = datetime.now(timezone.utc) - calculated_time

            if abs(time_diff) > timedelta(
                seconds=3
            ):  # TODO: determine good value for this
                self.start_time = datetime.now(timezone.utc)
                calculated_time = (
                    self.start_time + self.package_counter * self.increment
                )
            myobj = {
                "payload": base64.b64encode(data).decode("utf-8"),
                "deviceTimestamp": (calculated_time).isoformat(timespec="milliseconds"),
                "deviceID": self.device_id,
                "recordingID": self.ongoing_recording_id,
            }
            self.wsa.send(json.dumps(myobj))
            # TODO: check if ws is connected, else buffer data (flush later)

        return _callback

    def subscribe_rt(
        self, predictions: list[str], callback: Union[Callable[[dict], None], None]
    ):
        """Subscribe to real-time predictions

        Args:
            predictions: List of classifiers to run.
            callback: Function to call on classifier output reception.

        Caution:
            Experimental feature
        """
        # TODO: sanitize predictions argument
        warnings.warn("Realtime predictions are an experimental feature.", Warning)
        self._rt_callback = callback
        message = {
            "action": "subscribeRealtimePredictions",
            "predictions": predictions,
            "deviceId": self.device_id,
            "deviceTs": int(round(time.time() * 1000)),
        }
        self.wsa.send(json.dumps(message))

    def unsubscribe_rt(self):
        """Unsubscribe from real-time predictions. Also clears any registered callback."""
        message = {
            "action": "unsubscribeRealtimePredictions",
            "deviceId": self.device_id,
            "deviceTs": int(round(time.time() * 1000)),
        }
        self.wsa.send(json.dumps(message))
        self._rt_callback = None

    def _ws_filter(self, callback):
        def _ws_cb(ws, message):
            if "bp_filter_eeg" in message and callback:  # raw and filtered data streams
                data = json.loads(message)
                callback(data)
            elif self._rt_callback:  # realtime predictions
                data = base64.b64decode(message).decode("utf-8")
                if data:
                    data_d = json.loads(data)
                    if "predictionResponse" in data_d:  # JAW_CLENCH
                        data_p = data_d.get("predictionResponse")
                        data_r = ("JAW_CLENCH", data_p)
                    elif "stateless_z_scores" in data_d:  # FFT
                        data_p = data_d.get("stateless_z_scores")
                        data_r = ("FFT", data_p)
                    if data_r:
                        self._rt_callback(data_r)

        return _ws_cb
