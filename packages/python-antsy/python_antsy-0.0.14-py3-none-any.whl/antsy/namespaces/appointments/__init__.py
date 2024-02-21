# -*- coding: UTF-8 -*-
import logging
from typing import List, Optional

from dateutil.parser import parse
from httpx import HTTPStatusError

from .models import QueueAppointment

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


class AppointmentsAPI:
    def __init__(self, antsy_client, version):
        self.__antsy_client = antsy_client
        self.__base_path = f"appointments/{version}"

    def get_queue_appointments(self, queue_uid: str) -> Optional[List[QueueAppointment]]:
        full_url = f"{self.__antsy_client.base_url}/{self.__base_path}/queue/{queue_uid}"

        try:
            response = self.__antsy_client.client.get(full_url).json()
        except HTTPStatusError as exc:
            logger.error(f"Error: {exc}")
            return None

        if response.get("status") != "ok":
            return None

        data = response.get("data")

        output: List[QueueAppointment] = []
        for appointment in data.get("appointments"):
            entry = {"uid": appointment.get("uid")}
            entry["day"] = parse(appointment.get("day")).date()
            entry["start_time"] = parse(appointment.get("start_time"))

            output.append(QueueAppointment.model_validate(entry))

        return output

    def create(self, queue_appointment_uid: str, customer_uid: str, **kwargs):
        pass
