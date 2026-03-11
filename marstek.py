import socket
import json
from typing import Dict, Any, Optional


class MarstekClient:
    def __init__(self, ip: str, port: int = 30000, timeout: float = 2.0):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(timeout)
        self._request_id = 1

    def _send_request(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        request = {"id": self._request_id, "method": method, "params": params or {}}
        self._request_id += 1
        self.sock.sendto(json.dumps(request).encode(), (self.ip, self.port))
        data, _ = self.sock.recvfrom(2048)
        return json.loads(data.decode())

    # WiFi
    def wifi_get_status(self, device_id: int = 0) -> Dict[str, Any]:
        """Get WiFi network information."""
        return self._send_request("Wifi.GetStatus", {"id": device_id}).get("result", {})

    # Bluetooth
    def ble_get_status(self, device_id: int = 0) -> Dict[str, Any]:
        """Get Bluetooth status."""
        return self._send_request("BLE.GetStatus", {"id": device_id}).get("result", {})

    # Battery
    def bat_get_status(self, device_id: int = 0) -> Dict[str, Any]:
        """Get battery information (SOC, temperature, capacity, etc)."""
        return self._send_request("Bat.GetStatus", {"id": device_id}).get("result", {})

    # PV (Photovoltaic)
    def pv_get_status(self, device_id: int = 0) -> Dict[str, Any]:
        """Get solar panel power, voltage, and current."""
        return self._send_request("PV.GetStatus", {"id": device_id}).get("result", {})

    # Energy System
    def es_get_status(self, device_id: int = 0) -> Dict[str, Any]:
        """Get energy system status (power, SOC, energy totals)."""
        return self._send_request("ES.GetStatus", {"id": device_id}).get("result", {})

    def es_get_mode(self, device_id: int = 0) -> Dict[str, Any]:
        """Get current operating mode."""
        return self._send_request("ES.GetMode", {"id": device_id}).get("result", {})

    def es_set_mode_auto(self, device_id: int = 0) -> bool:
        """Set Auto mode."""
        result = self._send_request("ES.SetMode", {
            "id": device_id,
            "config": {"mode": "Auto", "auto_cfg": {"enable": 1}}
        })
        print(f"DEBUG: Server response: {result}")
        return result.get("set_result", False)

    def es_set_mode_ai(self, device_id: int = 0) -> bool:
        """Set AI mode."""
        result = self._send_request("ES.SetMode", {
            "id": device_id,
            "config": {"mode": "AI", "ai_cfg": {"enable": 1}}
        })
        return result.get("set_result", False)

    def es_set_mode_manual(self, device_id: int = 0, time_num: int = 0, 
                          start_time: str = "08:00", end_time: str = "20:00",
                          week_set: int = 127, power: int = 100) -> bool:
        """Set Manual mode with time schedule."""
        result = self._send_request("ES.SetMode", {
            "id": device_id,
            "config": {
                "mode": "Manual",
                "manual_cfg": {
                    "time_num": time_num,
                    "start_time": start_time,
                    "end_time": end_time,
                    "week_set": week_set,
                    "power": power,
                    "enable": 1
                }
            }
        })
        return result.get("set_result", False)

    def es_set_mode_passive(self, device_id: int = 0, power: int = 100, cd_time: int = 300) -> bool:
        """Set Passive mode with power and countdown."""
        old_timeout = self.sock.gettimeout()
        self.sock.settimeout(10.0)
        try:
            result = self._send_request("ES.SetMode", {
                "id": device_id,
                "config": {
                    "mode": "Passive",
                    "passive_cfg": {"power": power, "cd_time": cd_time}
                }
            })
            print(f"DEBUG: Server response: {result}")
            return result.get("set_result", False)
        finally:
            self.sock.settimeout(old_timeout)

    # Energy Meter
    def em_get_status(self, device_id: int = 0) -> Dict[str, Any]:
        """Get energy meter/CT status and power data."""
        return self._send_request("EM.GetStatus", {"id": device_id}).get("result", {})

    def close(self):
        self.sock.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
