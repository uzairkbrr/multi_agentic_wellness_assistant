from typing import List, Dict, Any
import streamlit as st
from backend.database import get_connection, init_db
from utils.styles import inject_landing_theme


init_db()
inject_landing_theme()


if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please log in to access this page.")
    st.stop()


st.title("Database")
st.caption("Browse tables, schemas, and sample records from the local SQLite database.")


def list_tables() -> List[str]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    rows = [r[0] for r in cur.fetchall()]
    conn.close()
    return rows


def get_table_schema(table: str) -> List[Dict[str, Any]]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info({table})")
    cols = cur.fetchall()
    # PRAGMA table_info returns: cid, name, type, notnull, dflt_value, pk
    schema = [
        {
            "cid": c[0],
            "name": c[1],
            "type": c[2],
            "notnull": bool(c[3]),
            "default": c[4],
            "primary_key": bool(c[5]),
        }
        for c in cols
    ]
    conn.close()
    return schema


def get_row_count(table: str) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) FROM {table}")
    count = cur.fetchone()[0]
    conn.close()
    return int(count or 0)


def fetch_rows(table: str, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table} LIMIT ? OFFSET ?", (limit, offset))
    rows = cur.fetchall()
    # with Row factory set, rows behave like dicts
    result = [dict(r) for r in rows]
    conn.close()
    return result


tables = list_tables()
if not tables:
    st.info("No tables found.")
    st.stop()

left, right = st.columns([2, 3])
with left:
    st.subheader("Tables")
    st.write("Select a table to view details.")
    selected = st.selectbox("Table", options=tables, index=0)
    st.divider()
    st.subheader("Summary")
    counts: Dict[str, int] = {}
    for t in tables:
        try:
            counts[t] = get_row_count(t)
        except Exception:
            counts[t] = -1
    for t in tables:
        c = counts.get(t, 0)
        st.markdown(f"- `{t}` — rows: {c if c >= 0 else 'n/a'}")

with right:
    st.subheader(f"Schema: {selected}")
    schema = get_table_schema(selected)
    if schema:
        st.dataframe(schema, use_container_width=True, hide_index=True)
    else:
        st.write("No schema info available.")

    st.subheader("Preview")
    n = st.slider("Rows", min_value=5, max_value=200, value=50, step=5)
    page = st.number_input("Page", min_value=1, value=1, step=1)
    offset = (page - 1) * n
    try:
        sample = fetch_rows(selected, limit=n, offset=offset)
        if sample:
            st.dataframe(sample, use_container_width=True)
        else:
            st.info("No rows to display.")
    except Exception as e:
        st.error(f"Failed to fetch rows: {e}")


