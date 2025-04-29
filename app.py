import streamlit as st
import datetime
import random

def main():
    st.set_page_config(page_title="Growth Mindset Challenge", page_icon="🌱")
    
    # Custom CSS for styling
    st.markdown("""
    <style>
    .big-font {
        font-size:20px !important;
        font-weight: bold;
    }
    .quote {
        font-style: italic;
        font-size: 18px;
        color: #2e8b57;
        padding: 10px;
        border-left: 5px solid #2e8b57;
        background-color: #f8f9fa;
    }
    .challenge-card {
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🌱 Growth Mindset Challenge")
    st.markdown("""
    Welcome to your personal Growth Mindset journey! This app will help you develop the belief that 
    your abilities can be developed through dedication and hard work.
    """)
    
    # Navigation
    menu = ["Learn About Growth Mindset", "Daily Challenge", "Progress Tracker", "Inspiration"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Learn About Growth Mindset":
        show_learning_section()
    elif choice == "Daily Challenge":
        show_daily_challenge()
    elif choice == "Progress Tracker":
        show_progress_tracker()
    elif choice == "Inspiration":
        show_inspiration()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    *"Becoming is better than being."* - Carol Dweck
    """)

def show_learning_section():
    st.header("What is a Growth Mindset?")
    st.markdown("""
    <div class="big-font">
    A growth mindset is the belief that your abilities and intelligence can be developed through 
    hard work, perseverance, and learning from your mistakes.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Fixed Mindset vs Growth Mindset")
        st.markdown("""
        - **Fixed Mindset**: Believes intelligence is static
        - Avoids challenges
        - Gives up easily
        - Sees effort as fruitless
        - Ignores useful feedback
        - Feels threatened by others' success
        """)
    
    with col2:
        st.markdown("""
        <br><br>
        - **Growth Mindset**: Believes intelligence can be developed
        - Embraces challenges
        - Persists in setbacks
        - Sees effort as path to mastery
        - Learns from criticism
        - Finds lessons and inspiration in others' success
        """)
    
    st.subheader("Why Adopt a Growth Mindset?")
    st.markdown("""
    - **Embrace Challenges**: View obstacles as opportunities to learn
    - **Learn from Mistakes**: Each error is a chance to improve
    - **Persist Through Difficulties**: Hard work leads to growth
    - **Celebrate Effort**: Reward the process, not just results
    - **Keep an Open Mind**: Stay curious and adaptable
    """)
    
    st.subheader("How to Practice a Growth Mindset")
    st.markdown("""
    1. **Set Learning Goals**: Focus on developing new skills
    2. **Reflect Regularly**: Learn from both successes and challenges
    3. **Seek Feedback**: Use criticism as a tool for improvement
    4. **Stay Positive**: Believe in your capacity to grow
    """)

def show_daily_challenge():
    st.header("Your Daily Growth Mindset Challenge")
    
    # Get or create session state
    if 'last_challenge_date' not in st.session_state:
        st.session_state.last_challenge_date = None
    if 'current_challenge' not in st.session_state:
        st.session_state.current_challenge = None
    
    today = datetime.date.today()
    
    # Check if we need a new challenge
    if st.session_state.last_challenge_date != today or st.session_state.current_challenge is None:
        st.session_state.last_challenge_date = today
        st.session_state.current_challenge = get_random_challenge()
    
    st.markdown(f"""
    <div class="challenge-card">
        <h3>Today's Challenge</h3>
        <p class="big-font">{st.session_state.current_challenge}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Reflect on Your Challenge")
    reflection = st.text_area("How did this challenge help you grow today? What did you learn?")
    
    if st.button("Submit Reflection"):
        if reflection:
            save_reflection(today, reflection)
            st.success("Reflection saved! Come back tomorrow for a new challenge.")
        else:
            st.warning("Please write something about your experience before submitting.")

def get_random_challenge():
    challenges = [
        "Learn something new outside your comfort zone today.",
        "Identify a recent mistake and write down what you learned from it.",
        "Ask a colleague or friend for constructive feedback on your work.",
        "When faced with a challenge today, say 'I can't do this YET' instead of 'I can't do this'.",
        "Help someone else learn something you're good at.",
        "Try a different approach to a problem you've been working on.",
        "List three things that were difficult for you in the past but are easy now.",
        "Spend 15 minutes practicing a skill you want to improve.",
        "Find an example of someone who succeeded through persistence and learn their story.",
        "Write down three ways you've grown in the past year."
    ]
    return random.choice(challenges)

def save_reflection(date, reflection):
    # In a real app, you'd save to a database
    # For this demo, we'll just store in session state
    if 'reflections' not in st.session_state:
        st.session_state.reflections = {}
    st.session_state.reflections[date.isoformat()] = {
        'date': date.isoformat(),
        'challenge': st.session_state.current_challenge,
        'reflection': reflection
    }

def show_progress_tracker():
    st.header("Your Growth Journey")
    
    if 'reflections' not in st.session_state or not st.session_state.reflections:
        st.info("You haven't completed any challenges yet. Check out the Daily Challenge!")
        return
    
    reflections = list(st.session_state.reflections.values())
    reflections.sort(key=lambda x: x['date'], reverse=True)
    
    st.subheader("Your Recent Reflections")
    for entry in reflections[:5]:  # Show most recent 5
        st.markdown(f"""
        <div class="challenge-card">
            <h4>{datetime.date.fromisoformat(entry['date']).strftime('%B %d, %Y')}</h4>
            <p><strong>Challenge:</strong> {entry['challenge']}</p>
            <p><strong>Your Reflection:</strong> {entry['reflection']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Simple streak counter
    dates = sorted([datetime.date.fromisoformat(r['date']) for r in reflections], reverse=True)
    streak = 0
    today = datetime.date.today()
    delta = datetime.timedelta(days=1)
    
    # Check if today's challenge is done
    if dates[0] == today:
        streak += 1
        current_date = today - delta
    else:
        current_date = today - delta
    
    # Count consecutive days
    for i in range(1, len(dates)):
        if dates[i] == current_date:
            streak += 1
            current_date -= delta
        else:
            break
    
    st.subheader("Current Streak")
    st.markdown(f"""
    <h1 style="text-align: center; color: #2e8b57;">{streak} day{'s' if streak != 1 else ''}</h1>
    """, unsafe_allow_html=True)
    st.caption("Keep going! Consistency builds growth.")

def show_inspiration():
    st.header("Inspiration for Your Journey")
    
    quotes = [
        ("The hand you are dealt is just the starting point for development. - Carol Dweck", "dweck"),
        ("It's not that I'm so smart, it's just that I stay with problems longer. - Albert Einstein", "einstein"),
        ("Success is no accident. It is hard work, perseverance, learning, sacrifice and most of all, love of what you are doing. - Pelé", "pele"),
        ("I haven't failed. I've just found 10,000 ways that won't work. - Thomas Edison", "edison"),
        ("The only limit to our realization of tomorrow is our doubts of today. - Franklin D. Roosevelt", "roosevelt"),
        ("You don't have to be great to start, but you have to start to be great. - Zig Ziglar", "ziglar"),
        ("The expert in anything was once a beginner. - Helen Hayes", "hayes"),
        ("Perseverance is failing 19 times and succeeding the 20th. - Julie Andrews", "andrews"),
        ("The only way to discover the limits of the possible is to go beyond them into the impossible. - Arthur C. Clarke", "clarke"),
        ("Continuous effort - not strength or intelligence - is the key to unlocking our potential. - Winston Churchill", "churchill")
    ]
    
    selected_quote = random.choice(quotes)
    
    st.markdown(f"""
    <div class="quote">
        "{selected_quote[0]}"
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Another Inspiring Quote"):
        st.experimental_rerun()
    
    st.subheader("Growth Mindset Tips")
    tips = [
        "Replace 'I'm not good at this' with 'I'm not good at this yet'",
        "View challenges as opportunities rather than obstacles",
        "Celebrate small improvements - progress is progress",
        "When you make a mistake, ask 'What can I learn from this?'",
        "Compare yourself to who you were yesterday, not to others",
        "Focus on the process rather than just the end result",
        "Reward effort and strategy, not just natural talent",
        "See criticism as valuable feedback for improvement",
        "Surround yourself with others who have a growth mindset",
        "Remember that even experts were once beginners"
    ]
    
    for tip in tips:
        st.markdown(f"- {tip}")

if __name__ == "__main__":
    main()