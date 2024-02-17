import struct
import time
import json

from .. import Packet
from ..timer import Timer


class HousekeepingReport:
    def __init__(self, report_id, interval, enabled, parameter_ids):
        self.report_id = report_id
        self.interval = interval
        self.enabled = enabled
        self.parameter_ids = parameter_ids
        self.last_sent = 0
        self.encoding = ""

    def __repr__(self):
        return f"HousekeepingStructure({self.report_id}, {self.interval}, {self.enabled}, {self.parameter_ids})"

    def decode(self, data):
        encoding = (
            self.encoding if self.encoding.startswith("!") else "!" + self.encoding
        )
        return struct.unpack(encoding, data)


class HousekeepingService:
    def __init__(self, parent):
        self.parent = parent
        self.housekeeping_reports = {}

    def define_housekeeping_report(
        self, report_id, interval, enabled, parameter_ids, **others
    ):
        self.housekeeping_reports[report_id] = HousekeepingReport(
            report_id, interval, enabled, parameter_ids
        )
        for parameter_id in parameter_ids:
            parameter = self.parent.parameter_management.get_parameter(parameter_id)
            self.housekeeping_reports[report_id].encoding += parameter.encoding

    def get_housekeeping_report(self, report_id):
        return self.housekeeping_reports.get(report_id)


class HousekeepingServiceController(HousekeepingService):

    def add_housekeeping_reports_from_file(self, filepath, node_id):
        with open(filepath, "r", encoding="utf-8") as f:
            x = json.load(f)
        list_of_dicts = x["housekeeping_reports"]

        for y in list_of_dicts:
            y["report_id"] = (node_id, y["report_id"])
            new_parameter_ids = []
            for z in y["parameter_ids"]:
                new_parameter_ids.append((node_id, z))
            y["parameter_ids"] = new_parameter_ids

        for kwargs in list_of_dicts:
            self.define_housekeeping_report(**kwargs)

    def process(self, service, subtype, data, node_id):
        case = (service, subtype)

        if case == (3, 25):
            report_id = (node_id, data.pop(0))
            housekeeping_report = self.get_housekeeping_report(report_id)
            decoded_data = housekeeping_report.decode(data)
            report = {}
            for i, value in enumerate(decoded_data):
                parameter_id = housekeeping_report.parameter_ids[i]
                report[parameter_id] = value
            self.received_housekeeping_report(node_id, report_id, report)

    def send_enable_period_housekeeping_reports(self, node_id, report_ids):
        self.parent.send(Packet([3, 5] + [len(report_ids)] + report_ids), node_id)

    def send_disable_period_housekeeping_reports(self, node_id, report_ids):
        self.parent.send(Packet([3, 6] + [len(report_ids)] + report_ids), node_id)

    def send_single_shot_housekeeping_reports(self, node_id, report_ids):
        self.parent.send(Packet([3, 27] + [len(report_ids)] + report_ids), node_id)

    def received_housekeeping_report(self, node_id, report_id, report):
        # to be overwritten
        pass


class HousekeepingServiceResponder(HousekeepingService):
    def __init__(self, parent):
        self.parent = parent
        self.housekeeping_reports = {}

        self._timer = None

    def add_housekeeping_reports_from_file(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            x = json.load(f)
        list_of_dicts = x["housekeeping_reports"]

        for kwargs in list_of_dicts:
            self.define_housekeeping_report(**kwargs)

        self._update_housekeeping_timer()

    def _update_housekeeping_timer(self):
        enabled = False
        for report in self.housekeeping_reports.values():
            if report.enabled:
                enabled = True
                break

        if enabled is True and self._timer is None:
            self._timer = Timer(1, self._timer_expired)
            self._timer.start()
        elif enabled is False and self._timer is not None:
            self._timer.stop()
            self._timer = None

    def _timer_expired(self):
        self._timer = Timer(1, self._timer_expired)
        self._timer.start()

        for report in self.housekeeping_reports.values():
            if report.enabled and report.last_sent + report.interval <= time.time():
                report.last_sent = time.time()
                self.send_housekeeping_report(report.report_id)

    def process(self, service, subtype, data, node_id):
        case = (service, subtype)

        # enable periodic housekeeping report
        if case == (3, 5):
            report_ids = self._extract_report_ids(data)
            if report_ids is None:
                # send fail acceptance report
                self.parent.request_verification.send_fail_acceptance_report(
                    [service, subtype]
                )
                return

            # send success acceptance report
            self.parent.request_verification.send_success_acceptance_report(
                [service, subtype]
            )

            for report_id in report_ids:
                report = self.get_housekeeping_report(report_id)
                report.enabled = True

            self._update_housekeeping_timer()

            # send success completion report
            self.parent.request_verification.send_success_completion_execution_report(
                [service, subtype]
            )

        # disable periodic housekeeping report
        elif case == (3, 6):
            report_ids = self._extract_report_ids(data)
            if report_ids is None:
                # send fail acceptance report
                self.parent.request_verification.send_fail_acceptance_report(
                    [service, subtype]
                )
                return

            # send success acceptance report
            self.parent.request_verification.send_success_acceptance_report(
                [service, subtype]
            )

            for report_id in report_ids:
                report = self.get_housekeeping_report(report_id)
                report.enabled = False

            self._update_housekeeping_timer()

            # send success completion report
            self.parent.request_verification.send_success_completion_execution_report(
                [service, subtype]
            )

        elif case == (3, 27):
            report_ids = self._extract_report_ids(data)
            if report_ids is None:
                # send fail acceptance report
                self.parent.request_verification.send_fail_acceptance_report(
                    [service, subtype]
                )
                return

            # send success acceptance report
            self.parent.request_verification.send_success_acceptance_report(
                [service, subtype]
            )

            for report_id in report_ids:
                self.send_housekeeping_report(report_id)

            # send success completion report
            self.parent.request_verification.send_success_completion_execution_report(
                [service, subtype]
            )

    def _extract_report_ids(self, data):
        try:
            n = data.pop(0)
            report_ids = list(x for x in data)
            if n != len(report_ids):
                raise ValueError
            for report_id in report_ids:
                if report_id not in self.housekeeping_reports:
                    raise ValueError
        except (IndexError, ValueError):
            return None
        return report_ids

    def send_housekeeping_report(self, report_id):
        try:
            report = self.get_housekeeping_report(report_id)
            data = bytearray()
            for parameter_id in report.parameter_ids:
                parameter = self.parent.parameter_management.get_parameter(parameter_id)
                data += parameter.encode()
        except (ValueError, KeyError):
            return False
        self.parent.send(Packet(bytes([3, 25, report_id]) + data))
        return True
