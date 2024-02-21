import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message


class IsIn:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        script_handler.script.append("\n# IS_IN")

        df_S: pd.DataFrame = pin["Src"].copy()
        df_V: pd.DataFrame = pin["Val"].copy()
        source: str = settings["source"] if "source" in settings and settings["source"] else None
        values: str = settings["values"] if "values" in settings and settings["values"] else None

        try:
            if "not_in" in settings and settings["not_in"]:
                df = df_S[~df_S[source].isin(df_V[values])].reset_index(drop=True)
            else:
                df = df_S[df_S[source].isin(df_V[values])].reset_index(drop=True)
            script_handler.script.append("df = df[df_S[{}].isin(df_V[{}])].reset_index(drop=True)".format(source, values))
        except Exception as e:
            msg = app_message.dataprep["nodes"]["exception"](node_key, str(e))
            return bug_handler.default_node_log(flow_id, node_key, msg, f"{e.__class__.__name__}({', '.join(e.args)})")

        cache_handler.update_node(
            flow_id,
            node_key,
            {
                "pout": {"Out": df},
                "config": json.dumps(settings, sort_keys=True),
                "script": script,
            },
        )

        script_handler.script += script
        return {"Out": df}
