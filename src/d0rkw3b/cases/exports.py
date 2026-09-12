"""Case projections retain provenance; graph edges come only from relationships."""

import csv
import io
import json
import xml.etree.ElementTree as ET
from datetime import datetime


def timeline(case):
    events = []
    for table, key, label in [
        ("entities", "created_at", "created_at"),
        ("runs", "created_at", "created_at"),
        ("notes", "created_at", "created_at"),
        ("evidence", "imported_at", "collected_at"),
        ("observations", "timestamp", "observed_at"),
        ("relationships", "observed_at", "observed_at"),
    ]:
        for row in case[table]:
            time_kind = (
                "created_at"
                if table == "observations" and row["kind"] == "generated_query"
                else label
            )
            events.append(
                {
                    "timestamp": row[key],
                    "time_kind": time_kind,
                    "record_type": table,
                    "record": row,
                }
            )
            collected = row.get("provenance", {}).get("collected_at")
            if collected and table in ("observations", "relationships"):
                events.append(
                    {
                        "timestamp": collected,
                        "time_kind": "collected_at",
                        "record_type": table,
                        "record": row,
                    }
                )
    return sorted(
        events,
        key=lambda e: (
            datetime.fromisoformat(e["timestamp"]),
            e["time_kind"],
            e["record_type"],
            json.dumps(e["record"], sort_keys=True),
        ),
    )


def records(case):
    yield {"record_type": "case", "record": case["case"]}
    for table in (
        "entities",
        "relationships",
        "observations",
        "runs",
        "notes",
        "evidence",
    ):
        for row in case[table]:
            yield {"record_type": table, "record": row}


def export_data(data, format="json"):
    if format == "json":
        return json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    rows = list(records(data)) if isinstance(data, dict) and "case" in data else data
    if format == "jsonl":
        return "".join(
            json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows
        )
    if format == "csv":
        out = io.StringIO(newline="")
        writer = csv.writer(out)
        writer.writerow(["record_type", "time_kind", "timestamp", "record_json"])
        for row in rows:
            writer.writerow(
                [
                    row["record_type"],
                    row.get("time_kind", ""),
                    row.get("timestamp", ""),
                    json.dumps(row["record"], ensure_ascii=False, sort_keys=True),
                ]
            )
        return out.getvalue()
    if format == "markdown":

        def cell(value):
            return (
                str(value)
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace("|", "&#124;")
                .replace("\n", " ")
            )

        return (
            "| Record | Time kind | Timestamp | Data |\n|---|---|---|---|\n"
            + "".join(
                f"| {cell(row['record_type'])} | {cell(row.get('time_kind', ''))} | {cell(row.get('timestamp', ''))} | {cell(json.dumps(row['record'], ensure_ascii=False))} |\n"
                for row in rows
            )
        )
    if format == "text":
        return (
            "\n".join(
                f"{row['record_type']}: {json.dumps(row, ensure_ascii=False, sort_keys=True)}"
                for row in rows
            )
            + "\n"
        )
    raise ValueError("unsupported case export format")


def graph(case, format="graphml"):
    if format not in ("graphml", "gexf"):
        raise ValueError("graph format must be graphml or gexf")
    namespace = (
        "http://graphml.graphdrawing.org/xmlns"
        if format == "graphml"
        else "http://www.gexf.net/1.2draft"
    )

    def element(parent, name, attrs=None):
        return ET.SubElement(parent, "{" + namespace + "}" + name, attrs or {})

    root = ET.Element("{" + namespace + "}" + format)
    if format == "graphml":
        element(
            root,
            "key",
            {
                "id": "record",
                "for": "all",
                "attr.name": "record_json",
                "attr.type": "string",
            },
        )
        graph_element = element(
            root, "graph", {"id": case["case"]["case_id"], "edgedefault": "directed"}
        )
        nodes_parent = edges_parent = graph_element
    else:
        root.set("version", "1.2")
        graph_element = element(
            root, "graph", {"mode": "static", "defaultedgetype": "directed"}
        )
        for cls in ("node", "edge"):
            attributes = element(graph_element, "attributes", {"class": cls})
            element(
                attributes,
                "attribute",
                {"id": "record", "title": "record_json", "type": "string"},
            )
        nodes_parent, edges_parent = (
            element(graph_element, "nodes"),
            element(graph_element, "edges"),
        )

    def data(node, value):
        encoded = json.dumps(value, ensure_ascii=False, sort_keys=True)
        if format == "graphml":
            element(node, "data", {"key": "record"}).text = encoded
        else:
            element(
                element(node, "attvalues"),
                "attvalue",
                {"for": "record", "value": encoded},
            )

    ids = {e["entity_id"] for e in case["entities"]}
    for entity in case["entities"]:
        attributes = {"id": entity["entity_id"]}
        if format == "gexf":
            attributes["label"] = entity["normalized_value"]
        data(element(nodes_parent, "node", attributes), entity)
    for relationship in case["relationships"]:
        if (
            relationship["subject_id"] not in ids
            or relationship["object_id"] not in ids
        ):
            raise ValueError("graph relationship refers to a missing entity")
        attributes = {
            "id": relationship["run_id"] + "_" + relationship["relationship_id"],
            "source": relationship["subject_id"],
            "target": relationship["object_id"],
        }
        if format == "gexf":
            attributes["label"] = relationship["predicate"]
        data(element(edges_parent, "edge", attributes), relationship)
    return ET.tostring(root, encoding="unicode", xml_declaration=True) + "\n"
