import atexit
from typing import Dict, List, Optional, TypedDict

from gantry.logger.log_location import EvalReportLog, FileLog, OutputLog, StreamLog


class Record(TypedDict):
    inputs: Dict
    outputs: Dict
    steps: List[Dict]


class EvalLogger:
    _record: Record

    def __init__(self, log_location: OutputLog) -> None:
        self._output = log_location
        self._output.open()

        atexit.register(self.close)

    def start_record(
        self,
        query: str,
        chat_history: Optional[List[Dict]] = None,
        session_id: Optional[str] = None,
        **kwargs,
    ):
        if not isinstance(query, str):
            raise TypeError(f"query must be a string, not {type(query)}")
        if not isinstance(chat_history, list) and chat_history is not None:
            raise TypeError(
                f"chat_history must be a list of dicts, not {type(chat_history)}"
            )

        self._record = {"inputs": {}, "outputs": {}, "steps": []}

        inputs: Dict = {"query": query}
        if chat_history:
            inputs["chat_history"] = chat_history
        if session_id:
            self._record["session_id"] = session_id
        inputs.update(kwargs)

        self.add_inputs(**inputs)

    def add_inputs(self, **kwargs):
        self._record["inputs"].update(kwargs)

    def add_outputs(self, **kwargs):
        self._record["outputs"].update(kwargs)

    def add_retrieval_step(self, query: str, documents: List[Dict]):
        self._record["steps"].append(
            {
                "type": "retrieval",
                "query": query,
                "documents": documents,
            }
        )

    def add_function_step(self, name: str, args: Dict, output: str):
        self._record["steps"].append(
            {
                "type": "function",
                "name": name,
                "args": args,
                "output": output,
            }
        )

    def add_llm_step(
        self, messages: List[Dict], response: str, params: Optional[Dict] = None
    ):
        self._record["steps"].append(
            {
                "type": "llm",
                "messages": list(messages),  # make a copy
                "response": response,
                "params": params,
            }
        )

    def add_custom_step(self, data: Dict):
        self._record["steps"].append(
            {
                "type": "custom",
                "data": data,
            }
        )

    def end_record(self, response: str, **kwargs):
        if not isinstance(response, str):
            raise TypeError(f"response must be a string, not {type(response)}")

        self.add_outputs(response=response, **kwargs)

        self._write_record(self._record)  # type: ignore

        self._record = None  # type: ignore

    def _write_record(self, record: Dict):
        self._output.write(record)

    def close(self):
        self._output.close()


class FileLogger(EvalLogger):
    _output: FileLog

    def __init__(self, path: str) -> None:
        super().__init__(FileLog(path))


class EvalReportLogger(EvalLogger):
    _output: EvalReportLog

    def __init__(self, name: str, api_key: Optional[str] = None) -> None:
        super().__init__(EvalReportLog(name=name, api_key=api_key))

    def create_evaluation_report(self):
        """Creates the evaluation report"""
        return self._output.create_evaluation_report()


class StreamLogger(EvalLogger):
    _output: StreamLog

    def __init__(
        self,
        source_name: str,
        api_key: Optional[str] = None,
        send_in_background: bool = True,
    ) -> None:
        super().__init__(
            StreamLog(
                source_name=source_name,
                api_key=api_key,
                send_in_background=send_in_background,
            )
        )
