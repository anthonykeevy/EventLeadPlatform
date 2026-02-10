"""
Knowledge Base (kb schema) service helpers.

This is an internal, SQL-authoritative knowledge base used by agents to:
- capture ideas without creating delivery work items too early
- maintain aspect dossiers and typed relationships
- generate compact "context packs" for reliable decision context
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

from sqlalchemy import text
from sqlalchemy.engine import Engine

from .database import engine as default_engine


KbId = int


class KbError(RuntimeError):
    pass


@dataclass(frozen=True)
class KbRef:
    table: str
    id_column: str
    code_column: str


KB_REFS: Dict[str, KbRef] = {
    "maturity": KbRef(table="kb.MaturityLevel", id_column="MaturityLevelID", code_column="LevelCode"),
    "aspect_state": KbRef(table="kb.AspectState", id_column="AspectStateID", code_column="StateCode"),
    "idea_status": KbRef(table="kb.IdeaStatus", id_column="IdeaStatusID", code_column="StatusCode"),
    "relation_type": KbRef(table="kb.RelationType", id_column="RelationTypeID", code_column="TypeCode"),
    "work_item_type": KbRef(table="kb.WorkItemType", id_column="WorkItemTypeID", code_column="TypeCode"),
    "review_task_status": KbRef(
        table="kb.ReviewTaskStatus", id_column="ReviewTaskStatusID", code_column="StatusCode"
    ),
}


def _as_int(value: Union[str, int, None]) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, int):
        return value
    v = value.strip()
    if not v:
        return None
    if v.isdigit():
        return int(v)
    return None


class KnowledgeBaseService:
    def __init__(self, db_engine: Optional[Engine] = None):
        self.engine: Engine = db_engine or default_engine

    # ---------------------------------------------------------------------
    # Health / primitives
    # ---------------------------------------------------------------------
    def assert_kb_ready(self) -> None:
        sql = "SELECT 1 FROM sys.schemas WHERE name = 'kb'"
        with self.engine.connect() as conn:
            exists = conn.execute(text(sql)).scalar()
        if not exists:
            raise KbError(
                "KB schema not found. Run the Alembic migration that creates schema [kb] "
                "(see backend/migrations/versions/036_kb_knowledge_base.py)."
            )

    def _get_ref_id(self, conn, ref: KbRef, code: str) -> int:
        sql = f"""
            SELECT {ref.id_column}
            FROM {ref.table}
            WHERE {ref.code_column} = :code
              AND IsDeleted = 0
        """
        rid = conn.execute(text(sql), {"code": code}).scalar()
        if rid is None:
            raise KbError(f"Reference not found: {ref.table}.{ref.code_column}='{code}'")
        return int(rid)

    def _get_relation_type(self, conn, type_code: str) -> Tuple[int, bool]:
        sql = """
            SELECT RelationTypeID, IsSymmetric
            FROM kb.RelationType
            WHERE TypeCode = :code AND IsDeleted = 0
        """
        row = conn.execute(text(sql), {"code": type_code}).fetchone()
        if not row:
            raise KbError(f"RelationType not found: '{type_code}'")
        return int(row[0]), bool(row[1])

    def _resolve_aspect_id(self, conn, aspect_key_or_id: Union[str, int]) -> int:
        maybe_id = _as_int(aspect_key_or_id)
        if maybe_id is not None:
            return maybe_id
        sql = "SELECT AspectID FROM kb.Aspect WHERE AspectKey = :k AND IsDeleted = 0"
        aid = conn.execute(text(sql), {"k": str(aspect_key_or_id)}).scalar()
        if aid is None:
            raise KbError(f"Aspect not found: '{aspect_key_or_id}'")
        return int(aid)

    def _resolve_idea_id(self, conn, idea_id: Union[str, int]) -> int:
        maybe_id = _as_int(idea_id)
        if maybe_id is None:
            raise KbError(f"Expected IdeaID (numeric), got: '{idea_id}'")
        return maybe_id

    # ---------------------------------------------------------------------
    # Writes
    # ---------------------------------------------------------------------
    def create_aspect(
        self,
        *,
        aspect_key: str,
        title: str,
        summary: Optional[str] = None,
        maturity_code: str = "M0",
        state_code: str = "active",
        owner: Optional[str] = None,
        created_by: Optional[int] = None,
    ) -> Dict[str, Any]:
        self.assert_kb_ready()
        normalized_key = aspect_key.strip()
        if not normalized_key:
            raise KbError("AspectKey is required")

        with self.engine.begin() as conn:
            maturity_id = self._get_ref_id(conn, KB_REFS["maturity"], maturity_code)
            state_id = self._get_ref_id(conn, KB_REFS["aspect_state"], state_code)

            sql = """
                INSERT INTO kb.Aspect (AspectKey, Title, Summary, MaturityLevelID, AspectStateID, Owner, CreatedBy, UpdatedBy)
                OUTPUT inserted.AspectID
                VALUES (:k, :t, :s, :maturity_id, :state_id, :owner, :created_by, :created_by)
            """
            try:
                new_id = conn.execute(
                    text(sql),
                    {
                        "k": normalized_key,
                        "t": title,
                        "s": summary,
                        "maturity_id": maturity_id,
                        "state_id": state_id,
                        "owner": owner,
                        "created_by": created_by,
                    },
                ).scalar()
            except Exception as e:
                raise KbError(f"Failed to create aspect: {e}") from e

            if new_id is None:
                raise KbError("Failed to create aspect: no AspectID returned")

            return {"AspectID": int(new_id), "AspectKey": normalized_key, "Title": title}

    def create_idea(
        self,
        *,
        title: str,
        problem_statement: Optional[str] = None,
        hypothesis: Optional[str] = None,
        impact_notes: Optional[str] = None,
        risks: Optional[str] = None,
        next_step: Optional[str] = None,
        decision_summary: Optional[str] = None,
        status_code: str = "captured",
        created_by: Optional[int] = None,
    ) -> Dict[str, Any]:
        self.assert_kb_ready()
        if not title.strip():
            raise KbError("Title is required")

        with self.engine.begin() as conn:
            status_id = self._get_ref_id(conn, KB_REFS["idea_status"], status_code)
            sql = """
                INSERT INTO kb.Idea (
                    Title, ProblemStatement, Hypothesis, ImpactNotes, Risks, NextStep, DecisionSummary,
                    IdeaStatusID, CreatedBy, UpdatedBy
                )
                OUTPUT inserted.IdeaID
                VALUES (
                    :title, :problem, :hypothesis, :impact, :risks, :next_step, :decision,
                    :status_id, :created_by, :created_by
                )
            """
            new_id = conn.execute(
                text(sql),
                {
                    "title": title,
                    "problem": problem_statement,
                    "hypothesis": hypothesis,
                    "impact": impact_notes,
                    "risks": risks,
                    "next_step": next_step,
                    "decision": decision_summary,
                    "status_id": status_id,
                    "created_by": created_by,
                },
            ).scalar()
            if new_id is None:
                raise KbError("Failed to create idea: no IdeaID returned")

            return {"IdeaID": int(new_id), "Title": title, "StatusCode": status_code}

    def set_idea_status(
        self,
        *,
        idea_id: Union[str, int],
        status_code: str,
        decision_summary: Optional[str] = None,
        updated_by: Optional[int] = None,
    ) -> Dict[str, Any]:
        self.assert_kb_ready()
        with self.engine.begin() as conn:
            iid = self._resolve_idea_id(conn, idea_id)
            status_id = self._get_ref_id(conn, KB_REFS["idea_status"], status_code)
            sql = """
                UPDATE kb.Idea
                SET IdeaStatusID = :status_id,
                    DecisionSummary = COALESCE(:decision_summary, DecisionSummary),
                    UpdatedBy = :updated_by
                WHERE IdeaID = :iid AND IsDeleted = 0
            """
            res = conn.execute(
                text(sql),
                {"status_id": status_id, "decision_summary": decision_summary, "updated_by": updated_by, "iid": iid},
            )
            if res.rowcount == 0:
                raise KbError(f"Idea not found or deleted: {iid}")
            return {"IdeaID": iid, "StatusCode": status_code}

    def link_idea_to_aspect(
        self,
        *,
        idea_id: Union[str, int],
        aspect_key_or_id: Union[str, int],
        notes: Optional[str] = None,
        created_by: Optional[int] = None,
    ) -> Dict[str, Any]:
        self.assert_kb_ready()
        with self.engine.begin() as conn:
            iid = self._resolve_idea_id(conn, idea_id)
            aid = self._resolve_aspect_id(conn, aspect_key_or_id)
            sql = """
                IF NOT EXISTS (
                    SELECT 1 FROM kb.IdeaAspect
                    WHERE IdeaID = :iid AND AspectID = :aid AND IsDeleted = 0
                )
                BEGIN
                    INSERT INTO kb.IdeaAspect (IdeaID, AspectID, Notes, CreatedBy, UpdatedBy)
                    VALUES (:iid, :aid, :notes, :created_by, :created_by)
                END
            """
            conn.execute(text(sql), {"iid": iid, "aid": aid, "notes": notes, "created_by": created_by})
            return {"IdeaID": iid, "AspectID": aid}

    def create_doc_ref(
        self,
        *,
        doc_path: str,
        anchor_id: Optional[str] = None,
        snapshot_commit_sha: Optional[str] = None,
        context_note: Optional[str] = None,
        created_by: Optional[int] = None,
        updated_by: Optional[int] = None,
    ) -> Dict[str, Any]:
        self.assert_kb_ready()
        normalized_path = doc_path.strip()
        if not normalized_path:
            raise KbError("DocPath is required")

        anchor = (anchor_id or "").strip() or None
        snapshot = (snapshot_commit_sha or "").strip() or None

        with self.engine.begin() as conn:
            # Audit semantics:
            # - On INSERT: CreatedBy and UpdatedBy should reflect the creating actor.
            # - On UPDATE (reuse): UpdatedBy should reflect the modifying actor, without
            #   overwriting CreatedBy (original creator).
            insert_user_id = created_by if created_by is not None else updated_by
            update_user_id = updated_by if updated_by is not None else created_by

            existing_id = conn.execute(
                text(
                    """
                    SELECT DocRefID
                    FROM kb.DocRef
                    WHERE DocPath = :p
                      AND ((AnchorID IS NULL AND :a IS NULL) OR AnchorID = :a)
                      AND ((SnapshotCommitSHA IS NULL AND :s IS NULL) OR SnapshotCommitSHA = :s)
                      AND IsDeleted = 0
                    """
                ),
                {"p": normalized_path, "a": anchor, "s": snapshot},
            ).scalar()

            if existing_id is not None:
                conn.execute(
                    text(
                        """
                        UPDATE kb.DocRef
                        SET ContextNote = COALESCE(:context_note, ContextNote),
                            UpdatedBy = COALESCE(:updated_by, UpdatedBy)
                        WHERE DocRefID = :id AND IsDeleted = 0
                        """
                    ),
                    {"context_note": context_note, "updated_by": update_user_id, "id": int(existing_id)},
                )
                return {
                    "DocRefID": int(existing_id),
                    "DocPath": normalized_path,
                    "AnchorID": anchor,
                    "SnapshotCommitSHA": snapshot,
                }

            sql = """
                INSERT INTO kb.DocRef (DocPath, AnchorID, SnapshotCommitSHA, ContextNote, CreatedBy, UpdatedBy)
                OUTPUT inserted.DocRefID
                VALUES (:p, :a, :s, :context_note, :user_id, :user_id)
            """
            new_id = conn.execute(
                text(sql),
                {
                    "p": normalized_path,
                    "a": anchor,
                    "s": snapshot,
                    "context_note": context_note,
                    "user_id": insert_user_id,
                },
            ).scalar()
            if new_id is None:
                raise KbError("Failed to create doc ref: no DocRefID returned")

            return {
                "DocRefID": int(new_id),
                "DocPath": normalized_path,
                "AnchorID": anchor,
                "SnapshotCommitSHA": snapshot,
            }

    def link_doc_ref_to_aspect(
        self,
        *,
        aspect_key_or_id: Union[str, int],
        doc_ref_id: Union[str, int],
        notes: Optional[str] = None,
        created_by: Optional[int] = None,
    ) -> Dict[str, Any]:
        self.assert_kb_ready()
        with self.engine.begin() as conn:
            aid = self._resolve_aspect_id(conn, aspect_key_or_id)
            drid = _as_int(doc_ref_id)
            if drid is None:
                raise KbError(f"Expected DocRefID (numeric), got: '{doc_ref_id}'")

            sql = """
                IF NOT EXISTS (
                    SELECT 1 FROM kb.AspectDocRef
                    WHERE AspectID = :aid AND DocRefID = :drid AND IsDeleted = 0
                )
                BEGIN
                    INSERT INTO kb.AspectDocRef (AspectID, DocRefID, Notes, CreatedBy, UpdatedBy)
                    VALUES (:aid, :drid, :notes, :created_by, :created_by)
                END
            """
            conn.execute(
                text(sql),
                {"aid": aid, "drid": drid, "notes": notes, "created_by": created_by},
            )
            return {"AspectID": aid, "DocRefID": drid}

    def link_doc_ref_to_idea(
        self,
        *,
        idea_id: Union[str, int],
        doc_ref_id: Union[str, int],
        notes: Optional[str] = None,
        created_by: Optional[int] = None,
    ) -> Dict[str, Any]:
        self.assert_kb_ready()
        with self.engine.begin() as conn:
            iid = self._resolve_idea_id(conn, idea_id)
            drid = _as_int(doc_ref_id)
            if drid is None:
                raise KbError(f"Expected DocRefID (numeric), got: '{doc_ref_id}'")

            sql = """
                IF NOT EXISTS (
                    SELECT 1 FROM kb.IdeaDocRef
                    WHERE IdeaID = :iid AND DocRefID = :drid AND IsDeleted = 0
                )
                BEGIN
                    INSERT INTO kb.IdeaDocRef (IdeaID, DocRefID, Notes, CreatedBy, UpdatedBy)
                    VALUES (:iid, :drid, :notes, :created_by, :created_by)
                END
            """
            conn.execute(
                text(sql),
                {"iid": iid, "drid": drid, "notes": notes, "created_by": created_by},
            )
            return {"IdeaID": iid, "DocRefID": drid}

    def link_aspects(
        self,
        *,
        from_aspect: Union[str, int],
        to_aspect: Union[str, int],
        relation_type_code: str,
        notes: Optional[str] = None,
        created_by: Optional[int] = None,
        auto_symmetric: bool = True,
    ) -> Dict[str, Any]:
        self.assert_kb_ready()
        with self.engine.begin() as conn:
            from_id = self._resolve_aspect_id(conn, from_aspect)
            to_id = self._resolve_aspect_id(conn, to_aspect)
            rel_id, is_symmetric = self._get_relation_type(conn, relation_type_code)

            if from_id == to_id:
                raise KbError("Cannot create a self-relation (FromAspectID == ToAspectID)")

            def _insert_edge(a: int, b: int) -> None:
                sql = """
                    IF NOT EXISTS (
                        SELECT 1
                        FROM kb.AspectRelation
                        WHERE FromAspectID = :a AND ToAspectID = :b AND RelationTypeID = :rel_id AND IsDeleted = 0
                    )
                    BEGIN
                        INSERT INTO kb.AspectRelation (
                            FromAspectID, ToAspectID, RelationTypeID, Notes, CreatedBy, UpdatedBy
                        )
                        VALUES (:a, :b, :rel_id, :notes, :created_by, :created_by)
                    END
                """
                conn.execute(
                    text(sql),
                    {"a": a, "b": b, "rel_id": rel_id, "notes": notes, "created_by": created_by},
                )

            _insert_edge(from_id, to_id)
            if auto_symmetric and is_symmetric:
                _insert_edge(to_id, from_id)

            return {
                "FromAspectID": from_id,
                "ToAspectID": to_id,
                "RelationTypeCode": relation_type_code,
                "SymmetricApplied": bool(auto_symmetric and is_symmetric),
            }

    def add_session_note(
        self,
        *,
        title: str,
        summary: Optional[str] = None,
        decisions: Optional[str] = None,
        source_type: Optional[str] = "cursor_chat",
        source_ref: Optional[str] = None,
        idea_ids: Optional[Sequence[Union[str, int]]] = None,
        aspect_ids_or_keys: Optional[Sequence[Union[str, int]]] = None,
        created_by: Optional[int] = None,
    ) -> Dict[str, Any]:
        self.assert_kb_ready()
        if not title.strip():
            raise KbError("Title is required")

        with self.engine.begin() as conn:
            sql = """
                INSERT INTO kb.SessionNote (Title, Summary, Decisions, SourceType, SourceRef, CreatedBy, UpdatedBy)
                OUTPUT inserted.SessionNoteID
                VALUES (:title, :summary, :decisions, :source_type, :source_ref, :created_by, :created_by)
            """
            sid = conn.execute(
                text(sql),
                {
                    "title": title,
                    "summary": summary,
                    "decisions": decisions,
                    "source_type": source_type,
                    "source_ref": source_ref,
                    "created_by": created_by,
                },
            ).scalar()
            if sid is None:
                raise KbError("Failed to create session note: no SessionNoteID returned")

            session_note_id = int(sid)

            # Link ideas
            for idea in idea_ids or []:
                iid = self._resolve_idea_id(conn, idea)
                conn.execute(
                    text(
                        """
                        IF NOT EXISTS (
                            SELECT 1 FROM kb.SessionNoteIdea
                            WHERE SessionNoteID = :sid AND IdeaID = :iid AND IsDeleted = 0
                        )
                        BEGIN
                            INSERT INTO kb.SessionNoteIdea (SessionNoteID, IdeaID, CreatedBy, UpdatedBy)
                            VALUES (:sid, :iid, :created_by, :created_by)
                        END
                        """
                    ),
                    {"sid": session_note_id, "iid": iid, "created_by": created_by},
                )

            # Link aspects
            for aspect in aspect_ids_or_keys or []:
                aid = self._resolve_aspect_id(conn, aspect)
                conn.execute(
                    text(
                        """
                        IF NOT EXISTS (
                            SELECT 1 FROM kb.SessionNoteAspect
                            WHERE SessionNoteID = :sid AND AspectID = :aid AND IsDeleted = 0
                        )
                        BEGIN
                            INSERT INTO kb.SessionNoteAspect (SessionNoteID, AspectID, CreatedBy, UpdatedBy)
                            VALUES (:sid, :aid, :created_by, :created_by)
                        END
                        """
                    ),
                    {"sid": session_note_id, "aid": aid, "created_by": created_by},
                )

            return {"SessionNoteID": session_note_id, "Title": title}

    def enqueue_related_aspect_reviews(
        self, *, aspect_key_or_id: Union[str, int], reason: str, created_by: Optional[int] = None
    ) -> Dict[str, Any]:
        self.assert_kb_ready()
        if not reason.strip():
            raise KbError("Reason is required")
        with self.engine.begin() as conn:
            aid = self._resolve_aspect_id(conn, aspect_key_or_id)
            conn.execute(
                text("EXEC kb.EnqueueRelatedAspectReviews :AspectID, :Reason, :CreatedBy"),
                {"AspectID": aid, "Reason": reason, "CreatedBy": created_by},
            )
            return {"AspectID": aid, "Enqueued": True}

    # ---------------------------------------------------------------------
    # Reads
    # ---------------------------------------------------------------------
    def list_open_ideas(
        self,
        *,
        exclude_status_codes: Sequence[str] = ("rejected", "validated"),
    ) -> Dict[str, Any]:
        """
        List ideas considered "open" and include their linked aspects.

        Default definition of "open": IdeaStatus not in ('rejected', 'validated').
        """
        self.assert_kb_ready()

        excluded = [c for c in exclude_status_codes if str(c).strip()]
        params: Dict[str, Any] = {}
        where_excluded = ""
        if excluded:
            placeholders: List[str] = []
            for idx, code in enumerate(excluded):
                key = f"s{idx}"
                placeholders.append(f":{key}")
                params[key] = code
            where_excluded = f"AND s.StatusCode NOT IN ({', '.join(placeholders)})"

        sql = f"""
            SELECT
                i.IdeaID,
                i.Title,
                s.StatusCode AS StatusCode,
                i.DecisionSummary,
                i.CreatedDate,
                i.UpdatedDate,
                a.AspectID,
                a.AspectKey,
                a.Title AS AspectTitle
            FROM kb.Idea i
            JOIN kb.IdeaStatus s
              ON s.IdeaStatusID = i.IdeaStatusID
             AND s.IsDeleted = 0
            LEFT JOIN kb.IdeaAspect ia
              ON ia.IdeaID = i.IdeaID
             AND ia.IsDeleted = 0
            LEFT JOIN kb.Aspect a
              ON a.AspectID = ia.AspectID
             AND a.IsDeleted = 0
            WHERE i.IsDeleted = 0
              {where_excluded}
            ORDER BY i.UpdatedDate DESC, i.IdeaID DESC, a.AspectKey
        """

        with self.engine.connect() as conn:
            rows = conn.execute(text(sql), params).mappings().all()

        ideas: List[Dict[str, Any]] = []
        by_id: Dict[int, Dict[str, Any]] = {}
        for r in rows:
            iid = int(r["IdeaID"])
            idea = by_id.get(iid)
            if idea is None:
                idea = {
                    "IdeaID": iid,
                    "Title": r["Title"],
                    "StatusCode": r["StatusCode"],
                    "DecisionSummary": r["DecisionSummary"],
                    "CreatedDate": r["CreatedDate"],
                    "UpdatedDate": r["UpdatedDate"],
                    "Aspects": [],
                }
                by_id[iid] = idea
                ideas.append(idea)

            if r.get("AspectID") is not None:
                idea["Aspects"].append(
                    {
                        "AspectID": int(r["AspectID"]),
                        "AspectKey": r["AspectKey"],
                        "Title": r["AspectTitle"],
                    }
                )

        return {"excludedStatusCodes": list(excluded), "ideas": ideas}

    def get_idea_pack(self, *, idea_id: Union[str, int]) -> Dict[str, Any]:
        """
        Return a compact but complete "idea pack" suitable for recall:
        - idea core fields (including problem/hypothesis/risks/next steps)
        - linked aspects
        - linked session notes
        - linked doc refs
        - linked work items
        """
        self.assert_kb_ready()
        with self.engine.connect() as conn:
            iid = self._resolve_idea_id(conn, idea_id)

            idea = conn.execute(
                text(
                    """
                    SELECT
                        i.IdeaID,
                        i.Title,
                        i.ProblemStatement,
                        i.Hypothesis,
                        i.ImpactNotes,
                        i.Risks,
                        i.NextStep,
                        i.DecisionSummary,
                        s.StatusCode AS StatusCode,
                        i.CreatedDate,
                        i.UpdatedDate
                    FROM kb.Idea i
                    JOIN kb.IdeaStatus s ON s.IdeaStatusID = i.IdeaStatusID
                    WHERE i.IdeaID = :iid AND i.IsDeleted = 0
                    """
                ),
                {"iid": iid},
            ).mappings().fetchone()
            if not idea:
                raise KbError(f"Idea not found or deleted: {iid}")

            aspects = conn.execute(
                text(
                    """
                    SELECT
                        a.AspectID,
                        a.AspectKey,
                        a.Title,
                        a.Summary,
                        ml.LevelCode AS MaturityLevelCode,
                        st.StateCode AS AspectStateCode
                    FROM kb.IdeaAspect ia
                    JOIN kb.Aspect a ON a.AspectID = ia.AspectID
                    JOIN kb.MaturityLevel ml ON ml.MaturityLevelID = a.MaturityLevelID
                    JOIN kb.AspectState st ON st.AspectStateID = a.AspectStateID
                    WHERE ia.IdeaID = :iid
                      AND ia.IsDeleted = 0
                      AND a.IsDeleted = 0
                    ORDER BY a.AspectKey
                    """
                ),
                {"iid": iid},
            ).mappings().all()

            session_notes = conn.execute(
                text(
                    """
                    SELECT
                        sn.SessionNoteID,
                        sn.Title,
                        sn.Summary,
                        sn.Decisions,
                        sn.SourceType,
                        sn.SourceRef,
                        sn.CreatedDate
                    FROM kb.SessionNoteIdea sni
                    JOIN kb.SessionNote sn ON sn.SessionNoteID = sni.SessionNoteID
                    WHERE sni.IdeaID = :iid
                      AND sni.IsDeleted = 0
                      AND sn.IsDeleted = 0
                    ORDER BY sn.CreatedDate DESC
                    """
                ),
                {"iid": iid},
            ).mappings().all()

            doc_refs = conn.execute(
                text(
                    """
                    SELECT
                        dr.DocRefID,
                        dr.DocPath,
                        dr.AnchorID,
                        dr.SnapshotCommitSHA,
                        dr.ContextNote,
                        idr.Notes
                    FROM kb.IdeaDocRef idr
                    JOIN kb.DocRef dr ON dr.DocRefID = idr.DocRefID
                    WHERE idr.IdeaID = :iid
                      AND idr.IsDeleted = 0
                      AND dr.IsDeleted = 0
                    ORDER BY dr.DocPath, dr.AnchorID
                    """
                ),
                {"iid": iid},
            ).mappings().all()

            work_items = conn.execute(
                text(
                    """
                    SELECT
                        w.WorkItemID,
                        t.TypeCode AS TypeCode,
                        w.ExternalSystem,
                        w.ExternalKey,
                        w.Url,
                        w.Status,
                        w.Title,
                        w.Description,
                        w.UpdatedDate
                    FROM kb.IdeaWorkItem iw
                    JOIN kb.WorkItem w ON w.WorkItemID = iw.WorkItemID
                    JOIN kb.WorkItemType t ON t.WorkItemTypeID = w.WorkItemTypeID
                    WHERE iw.IdeaID = :iid
                      AND iw.IsDeleted = 0
                      AND w.IsDeleted = 0
                    ORDER BY w.UpdatedDate DESC
                    """
                ),
                {"iid": iid},
            ).mappings().all()

            return {
                "idea": dict(idea),
                "aspects": [dict(a) for a in aspects],
                "sessionNotes": [dict(s) for s in session_notes],
                "docRefs": [dict(d) for d in doc_refs],
                "workItems": [dict(w) for w in work_items],
            }

    def get_aspect_context_pack(self, *, aspect_key_or_id: Union[str, int]) -> Dict[str, Any]:
        """
        Return a compact context pack suitable for agent prompting:
        - aspect core fields
        - direct related aspects (typed edges)
        - linked ideas and their statuses
        - linked work items
        - linked session notes
        - linked doc refs
        - open review tasks
        """
        self.assert_kb_ready()
        with self.engine.connect() as conn:
            aid = self._resolve_aspect_id(conn, aspect_key_or_id)

            aspect = conn.execute(
                text(
                    """
                    SELECT
                        a.AspectID, a.AspectKey, a.Title, a.Summary,
                        ml.LevelCode AS MaturityLevelCode,
                        st.StateCode AS AspectStateCode,
                        a.Owner, a.LastReviewedDate, a.NextReviewDate,
                        a.CreatedDate, a.UpdatedDate
                    FROM kb.Aspect a
                    JOIN kb.MaturityLevel ml ON ml.MaturityLevelID = a.MaturityLevelID
                    JOIN kb.AspectState st ON st.AspectStateID = a.AspectStateID
                    WHERE a.AspectID = :aid AND a.IsDeleted = 0
                    """
                ),
                {"aid": aid},
            ).mappings().fetchone()
            if not aspect:
                raise KbError(f"Aspect not found or deleted: {aid}")

            related = conn.execute(
                text(
                    """
                    SELECT
                        ar.AspectRelationID,
                        ar.FromAspectID,
                        ar.ToAspectID,
                        rt.TypeCode AS RelationTypeCode,
                        CASE WHEN ar.FromAspectID = :aid THEN 'out' ELSE 'in' END AS Direction,
                        other.AspectID AS RelatedAspectID,
                        other.AspectKey AS RelatedAspectKey,
                        other.Title AS RelatedTitle,
                        ar.Notes
                    FROM kb.AspectRelation ar
                    JOIN kb.RelationType rt ON rt.RelationTypeID = ar.RelationTypeID
                    JOIN kb.Aspect other
                      ON other.AspectID = CASE WHEN ar.FromAspectID = :aid THEN ar.ToAspectID ELSE ar.FromAspectID END
                    WHERE ar.IsDeleted = 0
                      AND other.IsDeleted = 0
                      AND (ar.FromAspectID = :aid OR ar.ToAspectID = :aid)
                    ORDER BY rt.SortOrder, other.AspectKey
                    """
                ),
                {"aid": aid},
            ).mappings().all()

            ideas = conn.execute(
                text(
                    """
                    SELECT
                        i.IdeaID,
                        i.Title,
                        s.StatusCode AS StatusCode,
                        i.DecisionSummary,
                        i.CreatedDate,
                        i.UpdatedDate
                    FROM kb.IdeaAspect ia
                    JOIN kb.Idea i ON i.IdeaID = ia.IdeaID
                    JOIN kb.IdeaStatus s ON s.IdeaStatusID = i.IdeaStatusID
                    WHERE ia.AspectID = :aid
                      AND ia.IsDeleted = 0
                      AND i.IsDeleted = 0
                    ORDER BY i.UpdatedDate DESC
                    """
                ),
                {"aid": aid},
            ).mappings().all()

            work_items = conn.execute(
                text(
                    """
                    SELECT
                        w.WorkItemID,
                        t.TypeCode AS TypeCode,
                        w.ExternalSystem,
                        w.ExternalKey,
                        w.Url,
                        w.Status,
                        w.Title,
                        w.Description,
                        w.UpdatedDate
                    FROM kb.AspectWorkItem aw
                    JOIN kb.WorkItem w ON w.WorkItemID = aw.WorkItemID
                    JOIN kb.WorkItemType t ON t.WorkItemTypeID = w.WorkItemTypeID
                    WHERE aw.AspectID = :aid
                      AND aw.IsDeleted = 0
                      AND w.IsDeleted = 0
                    ORDER BY w.UpdatedDate DESC
                    """
                ),
                {"aid": aid},
            ).mappings().all()

            session_notes = conn.execute(
                text(
                    """
                    SELECT
                        sn.SessionNoteID,
                        sn.Title,
                        sn.Summary,
                        sn.Decisions,
                        sn.SourceType,
                        sn.SourceRef,
                        sn.CreatedDate
                    FROM kb.SessionNoteAspect sna
                    JOIN kb.SessionNote sn ON sn.SessionNoteID = sna.SessionNoteID
                    WHERE sna.AspectID = :aid
                      AND sna.IsDeleted = 0
                      AND sn.IsDeleted = 0
                    ORDER BY sn.CreatedDate DESC
                    """
                ),
                {"aid": aid},
            ).mappings().all()

            doc_refs = conn.execute(
                text(
                    """
                    SELECT
                        dr.DocRefID,
                        dr.DocPath,
                        dr.AnchorID,
                        dr.SnapshotCommitSHA,
                        dr.ContextNote,
                        adr.Notes
                    FROM kb.AspectDocRef adr
                    JOIN kb.DocRef dr ON dr.DocRefID = adr.DocRefID
                    WHERE adr.AspectID = :aid
                      AND adr.IsDeleted = 0
                      AND dr.IsDeleted = 0
                    ORDER BY dr.DocPath, dr.AnchorID
                    """
                ),
                {"aid": aid},
            ).mappings().all()

            open_reviews = conn.execute(
                text(
                    """
                    SELECT
                        rt.ReviewTaskID,
                        rt.Reason,
                        s.StatusCode AS StatusCode,
                        rt.DueDate,
                        rt.CreatedDate,
                        rt.CompletedDate,
                        rt.TriggeredByAspectID
                    FROM kb.ReviewTask rt
                    JOIN kb.ReviewTaskStatus s ON s.ReviewTaskStatusID = rt.ReviewTaskStatusID
                    WHERE rt.AspectID = :aid
                      AND rt.IsDeleted = 0
                      AND rt.CompletedDate IS NULL
                    ORDER BY rt.CreatedDate DESC
                    """
                ),
                {"aid": aid},
            ).mappings().all()

            return {
                "aspect": dict(aspect),
                "relatedAspects": [dict(r) for r in related],
                "ideas": [dict(i) for i in ideas],
                "workItems": [dict(w) for w in work_items],
                "sessionNotes": [dict(s) for s in session_notes],
                "docRefs": [dict(d) for d in doc_refs],
                "openReviewTasks": [dict(r) for r in open_reviews],
            }

