"""
Decision Graph — NetworkX directed graph for cross-meeting decision tracking.
Nodes: items (decisions, actions), people, deadlines, meetings.
Edges: depends_on, supersedes, assigned_to, due_on.
"""
from __future__ import annotations

import json
import logging
from typing import Any

import networkx as nx

from .meeting_record import Edge, Item, MeetingRecord

logger = logging.getLogger(__name__)


class DecisionGraph:
    """
    A small knowledge graph of confirmed meeting items.
    Only confirmed/edited items enter the graph.
    """

    def __init__(self):
        self.G: nx.DiGraph = nx.DiGraph()

    # ── Building the graph ───────────────────────────────────────────────────

    def add_meeting(self, record: MeetingRecord) -> None:
        """Add confirmed items from a meeting record to the graph."""
        # Add meeting node
        self.G.add_node(
            f"meeting:{record.meeting_id}",
            type="meeting",
            title=record.title or record.meeting_id,
            created_at=str(record.created_at),
        )

        for item in record.confirmed_items():
            node_id = f"item:{item.id}"
            self.G.add_node(
                node_id,
                type=item.type,
                text=item.text,
                owner=item.owner,
                deadline=item.deadline,
                status=item.status,
                meeting_id=record.meeting_id,
            )
            # Link item → meeting
            self.G.add_edge(
                node_id,
                f"meeting:{record.meeting_id}",
                type="from_meeting",
            )

            # Add owner as a person node
            if item.owner:
                person_id = f"person:{item.owner.lower().strip()}"
                if not self.G.has_node(person_id):
                    self.G.add_node(person_id, type="person", name=item.owner)
                self.G.add_edge(node_id, person_id, type="assigned_to")

        # Add confirmed edges
        item_ids = {i.id for i in record.confirmed_items()}
        for edge in record.edges:
            if edge.status == "confirmed":
                from_node = f"item:{edge.from_id}"
                to_node   = f"item:{edge.to_id}"
                if from_node in self.G and to_node in self.G:
                    self.G.add_edge(from_node, to_node, type=edge.type)

    # ── Conflict flagging ────────────────────────────────────────────────────

    def flag_conflicts(self, new_item: Item, threshold: float = 0.3) -> list[dict]:
        """
        Find existing confirmed items that may conflict with a new decision.
        Uses simple keyword overlap heuristic.
        Returns list of {node_id, text, meeting_id, overlap_score}.
        """
        new_words = set(new_item.text.lower().split())
        conflicts = []

        for node, data in self.G.nodes(data=True):
            if data.get("type") not in ("decision", "action"):
                continue
            existing_words = set(data.get("text", "").lower().split())
            overlap = len(new_words & existing_words) / max(len(new_words), 1)
            if overlap >= threshold:
                conflicts.append({
                    "node_id": node,
                    "text": data.get("text"),
                    "meeting_id": data.get("meeting_id"),
                    "overlap_score": round(overlap, 2),
                })

        conflicts.sort(key=lambda x: x["overlap_score"], reverse=True)
        return conflicts[:5]

    # ── Impact analysis ──────────────────────────────────────────────────────

    def impact_analysis(self, item_id: str) -> list[dict]:
        """
        Given an item that changed, find all items that depend on it (reachable via edges).
        Returns list of affected items with path.
        """
        node_id = f"item:{item_id}"
        if node_id not in self.G:
            return []

        affected = []
        try:
            descendants = nx.descendants(self.G, node_id)
            for desc in descendants:
                data = self.G.nodes[desc]
                if data.get("type") in ("decision", "action"):
                    path = nx.shortest_path(self.G, node_id, desc)
                    edge_types = [
                        self.G.edges[path[i], path[i+1]].get("type", "?")
                        for i in range(len(path)-1)
                    ]
                    affected.append({
                        "node_id": desc,
                        "text": data.get("text"),
                        "owner": data.get("owner"),
                        "deadline": data.get("deadline"),
                        "meeting_id": data.get("meeting_id"),
                        "path": path,
                        "edge_types": edge_types,
                    })
        except nx.NetworkXError:
            pass

        return affected

    # ── What-if query ────────────────────────────────────────────────────────

    def what_if_deadline_changes(self, item_id: str) -> dict:
        """
        Advisory: what tasks/owners would be affected if this item's deadline changes?
        """
        node_id = f"item:{item_id}"
        if node_id not in self.G:
            return {"affected": [], "advisory": "Item not found in graph."}

        affected = self.impact_analysis(item_id)
        owners = list({a["owner"] for a in affected if a.get("owner")})

        return {
            "item_id": item_id,
            "affected_items": affected,
            "affected_owners": owners,
            "advisory": (
                f"Changing this deadline may affect {len(affected)} dependent item(s) "
                f"and {len(owners)} owner(s). Review paths for full context."
                if affected
                else "No downstream dependencies found."
            ),
        }

    # ── Serialization ────────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Serialize graph to node-link JSON for D3.js visualization."""
        data = nx.node_link_data(self.G, edges="links")
        # Ensure both 'links' and 'edges' keys exist for compatibility
        if "links" in data and "edges" not in data:
            data["edges"] = data["links"]
        elif "edges" in data and "links" not in data:
            data["links"] = data["edges"]
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "DecisionGraph":
        g = cls()
        g.G = nx.node_link_graph(data, edges="edges")
        return g


# ── Module-level singleton ────────────────────────────────────────────────────

_GRAPH: DecisionGraph | None = None


def get_graph() -> DecisionGraph:
    global _GRAPH
    if _GRAPH is None:
        _GRAPH = DecisionGraph()
    return _GRAPH


def reset_graph() -> None:
    global _GRAPH
    _GRAPH = DecisionGraph()
