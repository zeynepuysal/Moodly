import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random

# Soft renk paleti
soft_colors = list(mcolors.TABLEAU_COLORS.values()) + list(mcolors.CSS4_COLORS.values())

# Mood eşlemeleri
moods = ["Happy", "Sad", "Angry", "Anxious", "Energetic", "Bored", "Sleepy", "Tired"]
mood_map = {mood: idx + 1 for idx, mood in enumerate(moods)}
reverse_mood_map = {v: k for k, v in mood_map.items()}

# Motivasyon mesajları
morning_quotes = [
    "When you wake up, remember what a great privilege it is to live, to enjoy, to think, and to love. – Marcus Aurelius",
    "Each morning we are born again. What we do today is what matters most. – Buddha",
    "Rise up, start fresh, see the bright opportunity in each new day."
]

evening_quotes = [
    "Be thankful for what you have today, and start fighting for what you will have tomorrow. – William Shakespeare",
    "Reflect on what you did today. Learn and grow. Tomorrow is a new beginning.",
    "Rest now, for tomorrow’s strength grows from today’s recovery."
]

weekly_motivations = [
    "Consistency is the key to emotional balance.",
    "Your emotions are valid — track them, learn from them.",
    "Small steps lead to big emotional insights.",
    "Great job tracking your mood this week — keep it going!"
]

# Session State
if "mood_data" not in st.session_state:
    st.session_state.mood_data = []

# Sayfa Ayarları
st.set_page_config(page_title="Moodly - Mood Tracker", layout="centered")
st.title("🌈 Moodly - Your Mood Tracker")

# Menü
menu = st.sidebar.selectbox("Menu", ["Track My Mood", "Weekly Insights"])

# Mood Kaydetme
if menu == "Track My Mood":
    st.subheader("✨ How are you feeling today?")

    mood = st.selectbox("Select your mood:", moods)
    intensity = st.slider("How strongly do you feel this mood? (1-5)", 1, 5, 3)
    reason = st.text_area("Would you like to share why you feel this way? (optional)")

    if st.button("Save"):
        now = datetime.now()
        entry = {
            "date": now.date().isoformat(),
            "timestamp": now.isoformat(),
            "hour": now.hour,
            "mood": mood,
            "mood_code": mood_map[mood],
            "intensity": intensity,
            "reason": reason
        }
        st.session_state.mood_data.append(entry)
        st.success(f"Your mood has been recorded: {mood} ({intensity}/5)")

        # Günlük motivasyon mesajı
        if 5 <= now.hour < 12:
            st.info(random.choice(morning_quotes))
        else:
            st.info(random.choice(evening_quotes))

# Haftalık Analiz
elif menu == "Weekly Insights":
    st.subheader("📊 Weekly Mood Analysis")

    if not st.session_state.mood_data:
        st.warning("No mood data recorded yet.")
    else:
        df = pd.DataFrame(st.session_state.mood_data)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        one_week_ago = datetime.now() - timedelta(days=7)
        df_week = df[df["timestamp"] >= one_week_ago]

        if df_week.empty:
            st.info("No entries found for the past week.")
        else:
            df_week["date"] = df_week["timestamp"].dt.date

            # Günlük ortalama yoğunluk grafiği - Çizgi grafik
            avg_intensity = df_week.groupby("date")["intensity"].mean()
            st.write("📈 Daily Mood Intensity Over the Week (Line Chart)")
            fig1, ax1 = plt.subplots()
            avg_intensity.plot(kind="line", marker="o", ax=ax1, color="cornflowerblue")
            ax1.set_ylabel("Average Intensity")
            ax1.set_title("Mood Intensity Trend")
            ax1.grid(True)
            st.pyplot(fig1)

            # Günlük ortalama yoğunluk grafiği - Sütun grafik
            st.write("📊 Daily Mood Intensity Over the Week (Bar Chart)")
            fig3, ax3 = plt.subplots()
            avg_intensity.plot(kind="bar", color="lightsalmon", ax=ax3)
            ax3.set_ylabel("Average Intensity")
            ax3.set_xlabel("Date")
            ax3.set_title("Daily Mood Intensity (Bar Chart)")
            ax3.grid(axis="y")
            st.pyplot(fig3)

            # Duygu dağılımı (yoğunlukla ağırlıklı) - Pasta grafiği
            mood_scores = df_week.groupby("mood")["intensity"].sum()
            st.write("🧠 Mood Distribution (Weighted by Intensity)")
            fig2, ax2 = plt.subplots()
            ax2.pie(mood_scores, labels=mood_scores.index, autopct="%1.1f%%",
                    colors=random.sample(soft_colors, len(mood_scores)), startangle=90)
            ax2.axis("equal")
            st.pyplot(fig2)

            # En baskın duygu (yoğunluk dikkate alınarak)
            dominant_mood = mood_scores.idxmax()
            st.success(f"Your most intense mood this week was: **{dominant_mood}**")

            # Haftalık motivasyon
            st.markdown("---")
            st.info("💬 **Weekly Motivation**")
            st.write(random.choice(weekly_motivations))

            # Girişler (nedenler)
            with st.expander("📖 See your notes from this week"):
                for _, row in df_week.iterrows():
                    if row["reason"]:
                        st.markdown(f"**{row['date']} - {row['mood']} ({row['intensity']}/5)**  \n{row['reason']}")
