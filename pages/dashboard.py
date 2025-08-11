import random
from datetime import datetime, timedelta
from typing import Dict, List
import pandas as pd
import altair as alt
import streamlit as st
from utils.styles import inject_landing_theme
from backend.crud import (
    list_workout_logs,
    list_meal_logs,
    list_activity,
    list_user_challenges,
    insert_workout_log,
    log_activity,
)
from agents.diet import extract_meal_name


if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please log in to access this page.")
    st.stop()

inject_landing_theme()

st.title("Dashboard")
st.write(f"Hello, {st.session_state.user['name']}! Here's your wellness overview.")
st.page_link("pages/challenges.py", label="Go to Challenges ➜", icon="🔥")
st.page_link("pages/report.py", label="Generate Report ➜", icon="📄")

quotes = [
    "Small steps every day lead to big changes.",
    "Your only limit is you.",
    "Progress over perfection.",
    "Be kind to your mind and body.",
    "Consistency beats intensity when intensity fails.",
]
st.info(random.choice(quotes))
st.markdown("<hr>", unsafe_allow_html=True)

# KPI Cards
meals = list_meal_logs(st.session_state.user["id"], limit=200)
workouts = list_workout_logs(st.session_state.user["id"], limit=200)
challenges = list_user_challenges(st.session_state.user["id"]) or []
active_challenges = sum(1 for c in challenges if c.get("status") == "active")

last7 = datetime.utcnow().date() - timedelta(days=6)
last7_meals = [m for m in meals if m.get("date") and str(m["date"]) >= str(last7)]
last7_workouts = [w for w in workouts if w.get("date") and str(w["date"]) >= str(last7)]
meals_7d_count = len(last7_meals)
workouts_7d_count = len(last7_workouts)

avg_kcal7 = None
try:
    vals = [float(m["calories_est"]) for m in last7_meals if m.get("calories_est") is not None]
    avg_kcal7 = round(sum(vals)/len(vals), 1) if vals else None
except Exception:
    avg_kcal7 = None

st.markdown('<div class="kpi-grid">\
  <div class="kpi-card meals">\
    <div class="label">Meals Logged</div>\
    <div class="value">%s</div>\
    <div class="sub">Past 7 days</div>\
  </div>\
  <div class="kpi-card workouts">\
    <div class="label">Workouts Logged</div>\
    <div class="value">%s</div>\
    <div class="sub">Past 7 days</div>\
  </div>\
  <div class="kpi-card challenges">\
    <div class="label">Active Challenges</div>\
    <div class="value">%s</div>\
    <div class="sub">Currently active</div>\
  </div>\
  <div class="kpi-card calories">\
    <div class="label">Avg Daily Calories</div>\
    <div class="value">%s</div>\
    <div class="sub">Avg per day (past 7 days)</div>\
  </div>\
</div>' % (meals_7d_count, workouts_7d_count, active_challenges, (avg_kcal7 if avg_kcal7 is not None else '—')), unsafe_allow_html=True)

# Streaks & Consistency (GitHub-style heatmap)
try:
    today = datetime.utcnow().date()
    
    # Year selection with toggle buttons
    current_year = today.year
    
    # Get user join date from session state or default to current year
    user_join_year = st.session_state.user.get("join_date", None)
    if user_join_year:
        try:
            # Parse join date if it's a string
            if isinstance(user_join_year, str):
                join_date = datetime.fromisoformat(user_join_year.split('T')[0])
                user_join_year = join_date.year
            else:
                user_join_year = user_join_year.year
        except:
            user_join_year = current_year
    else:
        # If no join date, assume user joined this year
        user_join_year = current_year
    
    # Only show years from when user joined to current year
    available_years = list(range(user_join_year, current_year + 1))
    
    # Create year toggle buttons
    st.markdown('<div class="section-card"><h3>Streaks & Consistency</h3>', unsafe_allow_html=True)
    
    # Year toggle buttons (GitHub-style)
    st.markdown('<div class="year-toggle-container">', unsafe_allow_html=True)
    year_buttons = st.columns(len(available_years))
    selected_year = current_year
    for i, year in enumerate(available_years):
        with year_buttons[i]:
            if st.button(f"{year}", key=f"year_{year}", 
                       type="primary" if year == current_year else "secondary",
                       use_container_width=True):
                selected_year = year
                st.session_state.selected_year = year
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Use selected year from session state or default to current year
    if "selected_year" in st.session_state:
        selected_year = st.session_state.selected_year
    
    # Calculate date range for selected year
    if selected_year == current_year:
        # Current year: from start of year to today
        start_date = datetime(selected_year, 1, 1).date()
        end_date = today
        days_back = (end_date - start_date).days + 1
    else:
        # Past years: full year
        start_date = datetime(selected_year, 1, 1).date()
        end_date = datetime(selected_year, 12, 31).date()
        days_back = (end_date - start_date).days + 1
    
    # Pull activities for the selected year
    activities = list_activity(st.session_state.user["id"], limit=10000)

    # Aggregate counts per UTC date for selected year
    daily_counts: Dict[datetime.date, int] = {}
    for act in activities:
        ts_raw = str(act.get("created_at", ""))
        if not ts_raw:
            continue
        try:
            # Support ...Z and timezone-aware strings
            ts_parsed = datetime.fromisoformat(ts_raw.replace("Z", "+00:00"))
        except Exception:
            try:
                # Fallback: strip timezone if any
                ts_parsed = datetime.fromisoformat(ts_raw.split("+")[0])
            except Exception:
                continue
        d = ts_parsed.date()
        # Only include dates from selected year
        if start_date <= d <= end_date:
            daily_counts[d] = daily_counts.get(d, 0) + 1

    # Build a complete day series for the selected year
    series: List[Dict] = []
    for i in range(days_back):
        d = start_date + timedelta(days=i)
        series.append({"date": d, "count": int(daily_counts.get(d, 0))})

    # Compute current and best streaks (only for current year)
    current_streak = 0
    best_streak = 0
    if selected_year == current_year:
        streak_running = 0
        consecutive_from_today = True
        for item in reversed(series):
            if item["date"] > today:
                continue
            if item["count"] > 0:
                streak_running += 1
                if consecutive_from_today:
                    current_streak = streak_running
            else:
                best_streak = max(best_streak, streak_running)
                streak_running = 0
                consecutive_from_today = False
        best_streak = max(best_streak, streak_running)
    else:
        # For past years, calculate best streak
        streak_running = 0
        for item in series:
            if item["count"] > 0:
                streak_running += 1
            else:
                best_streak = max(best_streak, streak_running)
                streak_running = 0
        best_streak = max(best_streak, streak_running)

    # Prepare dataframe for heatmap (GitHub-style weeks x weekdays)
    df = pd.DataFrame(series)
    if not df.empty and df["count"].sum() > 0:
        df["date"] = pd.to_datetime(df["date"])  # ensure datetime64
        df["dow"] = df["date"].dt.weekday  # 0=Mon ... 6=Sun
        # Compute week index from the start date so weeks are contiguous across year boundaries
        df["week_index"] = ((df["date"] - df["date"].min()).dt.days // 7).astype(int)

        # Two-color scheme: grey = no activity, green = activity present
        df["active"] = (df["count"].astype(int) > 0).astype(int)
        colors = ["#9e9e9e", "#39d353"]

        heatmap = (
            alt.Chart(df)
            .mark_square(size=40)  # Increased to 40px for even bigger dots
            .encode(
                x=alt.X("week_index:O", axis=None),
                y=alt.Y("dow:O", sort=[0, 1, 2, 3, 4, 5, 6], axis=None),
                color=alt.Color(
                    "active:N",
                    scale=alt.Scale(domain=[0, 1], range=colors),
                    legend=None,
                ),
                tooltip=[
                    alt.Tooltip("date:T", title="Date"),
                    alt.Tooltip("count:Q", title="Activities"),
                ],
            )
            .properties(width=900, height={"step": 10})  # Fixed width of 900px, reduced step size to bring dots closer together
        )

        # Display streak information
        total_activities = df["count"].sum()
        if selected_year == current_year:
            st.markdown(
                f'<div class="progress-row"><div class="progress-label">🔥 Current streak</div>'
                f'<div class="pill">{current_streak} days</div></div>'
                f'<div class="progress-row"><div class="progress-label">🏆 Best streak</div>'
                f'<div class="pill">{best_streak} days</div></div>'
                f'<div class="progress-row"><div class="progress-label">📊 Total activities</div>'
                f'<div class="pill">{total_activities}</div></div>'
                , unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="progress-row"><div class="progress-label">🏆 Best streak in {selected_year}</div>'
                f'<div class="pill">{best_streak} days</div></div>'
                f'<div class="progress-row"><div class="progress-label">📊 Total activities</div>'
                f'<div class="pill">{total_activities}</div></div>'
                , unsafe_allow_html=True,
            )
        
        st.markdown('<div style="margin-top:10px"></div>', unsafe_allow_html=True)
        st.altair_chart(heatmap, use_container_width=True)
        
        # Add legend below the heatmap
        st.markdown(
            '<div class="heatmap-legend">'
            '<span class="legend-item">'
            '<span class="legend-color" style="background-color: #9e9e9e;"></span>'
            'No activity'
            '</span>'
            '<span class="legend-item">'
            '<span class="legend-color" style="background-color: #39d353;"></span>'
            'Activity logged'
            '</span>'
            '</div>',
            unsafe_allow_html=True
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # No activities in selected year
        st.markdown(
            f'<div class="progress-row"><div class="progress-label">📊 Activities in {selected_year}</div>'
            f'<div class="pill">No data</div></div>'
            , unsafe_allow_html=True,
        )
        st.info(f"No activities found for {selected_year}. Start logging your wellness activities to see your streak visualization!")
        st.markdown('</div>', unsafe_allow_html=True)
except Exception as e:
    # Fail quietly if anything goes wrong
    st.error(f"Error loading streak data: {str(e)}")
    pass

col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="section-card"><h3>Recent Meals<span class="pill">last 5</span></h3>', unsafe_allow_html=True)
    _meal_cache = st.session_state.setdefault("meal_name_cache", {})
    for log in list_meal_logs(st.session_state.user["id"], limit=5):
        if log.get("meal_name"):
            display_name = str(log["meal_name"]).strip()
        else:
            raw_text = (log.get("description") or "Meal").strip()
            cached = _meal_cache.get(raw_text)
            if not cached:
                try:
                    cached = extract_meal_name(raw_text)
                except Exception:
                    cached = raw_text
                _meal_cache[raw_text] = cached
            display_name = cached
        kc = f" · {log['calories_est']} kcal" if log.get("calories_est") else ""
        st.markdown(f"- {log['date']}: {display_name}{kc}")
    st.markdown('</div>', unsafe_allow_html=True)

# Removed Last 7 Days charts per request
with col2:
    st.markdown('<div class="section-card"><h3>Recent Workouts<span class="pill">last 5</span></h3>', unsafe_allow_html=True)
    for log in list_workout_logs(st.session_state.user["id"], limit=5):
        kc = f" · {log['calories_burned']} kcal" if log.get("calories_burned") else ""
        st.markdown(f"- {log['date']}: {log['routine']}{kc}")
    st.markdown('</div>', unsafe_allow_html=True)

# Second row: Exercise Checklist and Challenges Progress side-by-side
col3, col4 = st.columns(2)
with col3:
    st.markdown('<div class="section-card"><h3>Exercise Checklist</h3>', unsafe_allow_html=True)
    today = datetime.utcnow().date()
    # Mock suggested exercises for today; in real app, source from AI plan or user profile
    weekday_to_suggested = {
        0: ["30 min jog", "20 squats", "15 push-ups"],
        1: ["Rest or light yoga", "10 min stretch"],
        2: ["Intervals: 4x400m run", "Plank 2x45s"],
        3: ["Upper body: 3x12 rows", "3x10 shoulder press"],
        4: ["Lower body: 3x12 lunges", "Glute bridges 3x15"],
        5: ["Hike or brisk walk 45 min"],
        6: ["Mobility + foam rolling 20 min"],
    }
    suggested = weekday_to_suggested.get(today.weekday(), ["Move for 20 minutes"])

    st.caption(f"Today's suggestions for {today.strftime('%A')}")
    completed_key = f"exercise_completed_{today.isoformat()}"
    completed = st.session_state.setdefault(completed_key, {})
    for ex in suggested:
        done = bool(completed.get(ex, False))
        checkbox_key = f"chk_{today.isoformat()}_{ex}"
        new_value = st.checkbox(ex, value=done, key=checkbox_key, disabled=done)
        # Only transition allowed: False -> True. Ignore any attempt to uncheck.
        if not done and new_value:
            completed[ex] = True
            st.session_state[completed_key] = completed
            try:
                insert_workout_log(
                    user_id=st.session_state.user["id"],
                    date=today.isoformat(),
                    routine=ex,
                    calories_burned=None,
                )
                log_activity(
                    st.session_state.user["id"],
                    "workout_log",
                    {"date": today.isoformat(), "routine": ex, "source": "checklist"},
                )
            except Exception:
                pass
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    # Active Challenges Progress
    active = [c for c in challenges if c.get("status") == "active"]
    if active:
        st.markdown('<div class="section-card"><h3>Challenges Progress</h3>', unsafe_allow_html=True)
        for c in active:
            pct = int(c.get("progress") or 0)
            st.markdown(f"<div class='progress-row'><div class='progress-label'>{c.get('title','Challenge')}</div></div>", unsafe_allow_html=True)
            st.progress(pct)
        st.markdown('</div>', unsafe_allow_html=True)

## Removed interactive weekly overview chart per request

# Activity Stream removed per request

# Quick Actions
st.markdown('<div class="section-card"><h3>Quick Actions</h3>', unsafe_allow_html=True)
qa1, qa2, qa3, qa4 = st.columns(4)
with qa1:
    if st.button("➕ Log Meal"):
        st.switch_page("pages/diet_tracker.py")
with qa2:
    if st.button("🏋️ Log Workout"):
        st.switch_page("pages/exercise_plan.py")
with qa3:
    if st.button("🧠 Check-in"):
        st.switch_page("pages/mental_health.py")
with qa4:
    if st.button("📄 Generate report"):
        st.switch_page("pages/report.py")
st.markdown('</div>', unsafe_allow_html=True)

 