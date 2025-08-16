import json
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

class RecommendationListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        schema = connection.schema_name
        limit = int(request.query_params.get("limit", 20))
        offset = int(request.query_params.get("offset", 0))
        rows = []
        with connection.cursor() as cur:
            cur.execute("""
                SELECT id, created_at, kind, title, details::text, status
                  FROM ai.recommendation
                 WHERE tenant_schema = %s
                 ORDER BY created_at DESC
                 LIMIT %s OFFSET %s
            """, [schema, limit, offset])
            rows = cur.fetchall()
        data = [
            {
                "id": r[0],
                "created_at": r[1],
                "kind": r[2],
                "title": r[3],
                "details": (json.loads(r[4]) if isinstance(r[4], str) and r[4] else {}),
                "status": r[5],
            } for r in rows
        ]
        return Response({"count": len(data), "results": data})

class RecommendationActionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, rec_id: int, action: str):
        if action not in ("ack", "dismiss", "apply"):
            return Response({"detail": "invalid action"}, status=status.HTTP_400_BAD_REQUEST)

        schema = connection.schema_name
        with connection.cursor() as cur:
            cur.execute("""
                DELETE FROM ai.recommendation
                 WHERE id=%s AND tenant_schema=%s
            """, [rec_id, schema])
            deleted = cur.rowcount

        if not deleted:
            return Response({"detail": "not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"ok": True})
