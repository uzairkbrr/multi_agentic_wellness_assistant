import streamlit as st
from utils.styles import inject_landing_theme


st.set_page_config(page_title="Multi-Agent Wellness Assistant", layout="wide")
inject_landing_theme()


st.markdown(
    """
<div class="navbar">
    <div class="brand-logo">MA Wellness</div>
    <div class="nav-links">
        <a href="#hero">Home</a>
        <a href="#how-it-works">How It Works</a>
        <a href="#testimonials">Testimonials</a>
        <a href="#membership-benefits">Benefits</a>
        <a href="#pricing">Pricing</a>
        <a href="#contact">Contact</a>
    </div>
    <div class="nav-button">
        <a href="/?signup=1" class="get-started-btn">Get Started</a>
    </div>
</div>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
<section class="hero" id="hero">
    <h1>Multi-Agent Wellness Assistant</h1>
    <p>Your personal AI-driven mental health, diet, and fitness companion — tailored to help you live your best life.</p>
    <div class="nav-button">
        <a href="/?signup=1" class="get-started-btn">Get Started</a>
    </div>
</section>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
<section id="how-it-works">
    <h2>How It Works</h2>
    <div class="steps-container">
        <div class="step-card">
            <div class="step-number">1</div>
            <div class="step-title">Create Your Profile</div>
            <div class="step-desc">Enter your personal details, fitness goals, and preferences to get started.</div>
        </div>
        <div class="step-card">
            <div class="step-number">2</div>
            <div class="step-title">Personalized Plans</div>
            <div class="step-desc">Receive custom diet, exercise, and mental health plans powered by AI.</div>
        </div>
        <div class="step-card">
            <div class="step-number">3</div>
            <div class="step-title">Track & Improve</div>
            <div class="step-desc">Log your progress and get ongoing support and motivation every day.</div>
        </div>
        <div class="step-card">
            <div class="step-number">4</div>
            <div class="step-title">Stay Motivated</div>
            <div class="step-desc">Daily check-ins and personalized tips to keep you inspired and on track.</div>
        </div>
    </div>
</section>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
<section id="membership-benefits">
    <h2>Membership Benefits</h2>
    <div class="benefits-container">
        <div class="benefit-card">
            <div class="benefit-icon">🤖</div>
            <div class="benefit-title">AI-Powered Personalization</div>
            <div class="benefit-desc">Get plans tailored specifically to your body, goals, and preferences.</div>
        </div>
        <div class="benefit-card">
            <div class="benefit-icon">📈</div>
            <div class="benefit-title">Progress Tracking</div>
            <div class="benefit-desc">Monitor your improvements in fitness, diet, and mental health effortlessly.</div>
        </div>
        <div class="benefit-card">
            <div class="benefit-icon">💬</div>
            <div class="benefit-title">24/7 Emotional Support</div>
            <div class="benefit-desc">Daily check-ins and motivational prompts to keep your spirits high.</div>
        </div>
        <div class="benefit-card">
            <div class="benefit-icon">🍎</div>
            <div class="benefit-title">Vision-Based Meal Analysis</div>
            <div class="benefit-desc">Upload meal photos to get instant nutrition breakdowns.</div>
        </div>
        <div class="benefit-card">
            <div class="benefit-icon">🏋️‍♂️</div>
            <div class="benefit-title">Adaptive Workouts</div>
            <div class="benefit-desc">Exercise plans that evolve with your progress and schedule.</div>
        </div>
        <div class="benefit-card">
            <div class="benefit-icon">🔒</div>
            <div class="benefit-title">Privacy & Security</div>
            <div class="benefit-desc">Your data is securely stored and protected with industry-standard encryption.</div>
        </div>
    </div>
</section>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
<section id="testimonials">
    <h2>What Our Clients Say About Us</h2>
    <div class="testimonials-container">
        <div class="testimonial-card">
            <img src="https://randomuser.me/api/portraits/women/65.jpg" alt="Client photo" class="testimonial-photo" />
            <div class="testimonial-quote">“MA Wellness transformed how I approach my health. The personalized plans feel like they were made just for me!”</div>
            <div class="testimonial-name">Sarah L.</div>
        </div>
        <div class="testimonial-card">
            <img src="https://randomuser.me/api/portraits/men/43.jpg" alt="Client photo" class="testimonial-photo" />
            <div class="testimonial-quote">“The daily mental health check-ins keep me grounded and motivated. Truly a game changer.”</div>
            <div class="testimonial-name">James P.</div>
        </div>
        <div class="testimonial-card">
            <img src="https://randomuser.me/api/portraits/women/22.jpg" alt="Client photo" class="testimonial-photo" />
            <div class="testimonial-quote">“I love how the workout plans adapt to my progress. It’s like having a personal trainer in my pocket.”</div>
            <div class="testimonial-name">Emily R.</div>
        </div>
    </div>
</section>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
<section id="pricing">
    <h2>Pricing Plans</h2>
    <div class="pricing-cards">
        <div class="pricing-card">
            <h3>Starter</h3>
            <p class="description">For emerging brands aiming for steady growth</p>
            <ul>
                <li>✔ Basic AI mental health check-ins</li>
                <li>✔ Simple custom diet plans</li>
                <li>✔ Weekly beginner workouts</li>
                <li>✔ Daily motivation quotes</li>
                <li>✔ Progress tracking dashboard</li>
                <li>✔ Secure data storage</li>
            </ul>
            <p class="price">$5 /month</p>
            <button type="button" disabled>Choose Starter</button>
        </div>
        <div class="pricing-card">
            <h3>Growth</h3>
            <p class="description">For established stores seeking solutions to scale further</p>
            <ul>
                <li>✔ All Starter features</li>
                <li>✔ Adaptive AI recommendations</li>
                <li>✔ Meal photo nutrition analysis</li>
                <li>✔ Dynamic workout plans</li>
                <li>✔ Mood-based mental prompts</li>
                <li>✔ Bi-weekly wellness reports</li>
            </ul>
            <p class="price">$10 /month</p>
            <button type="button" disabled>Choose Growth</button>
        </div>
        <div class="pricing-card">
            <h3>Scale</h3>
            <p class="description">For high-growth brands needing enterprise-level solutions</p>
            <ul>
                <li>✔ All Growth features</li>
                <li>✔ Multi-agent AI support</li>
                <li>✔ Real-time coaching feedback</li>
                <li>✔ Custom macro meal plans</li>
                <li>✔ Advanced mood & stress tracking</li>
                <li>✔ Weekly virtual coaching</li>
            </ul>
            <p class="price">$20 /month</p>
            <button type="button" disabled>Choose Scale</button>
        </div>
    </div>
</section>
    """,
    unsafe_allow_html=True,
)

st.markdown('<section id="faq"><h2>Frequently Asked Questions</h2></section>', unsafe_allow_html=True)

faq_data = [
    ("What is the Multi-Agent Wellness Assistant?", "It’s an AI-powered platform providing personalized mental health, diet, and fitness plans tailored to you."),
    ("How do I get started?", "Sign up and create your profile to receive your customized wellness plan."),
    ("Can I change my plan later?", "Yes! You can upgrade, downgrade, or pause your membership anytime."),
    ("Is my personal data secure?", "Absolutely, we use industry-standard encryption to keep your data safe and private."),
    ("Do you offer customer support?", "Yes, email and chat support are available 24/7 to help you."),
]

with st.container():
    for question, answer in faq_data:
        with st.expander(question):
            st.write(answer)


st.markdown('<div id="contact-wrapper">', unsafe_allow_html=True)
st.markdown('<section id="contact">', unsafe_allow_html=True)
st.markdown('<h2>Contact Us</h2>', unsafe_allow_html=True)
st.markdown('<div class="contact-form">', unsafe_allow_html=True)

with st.form(key="contact_form"):
    name = st.text_input("Name", placeholder="Your full name")
    email = st.text_input("Email", placeholder="you@example.com")
    message = st.text_area("Message", placeholder="Write your message here...")
    submit_button = st.form_submit_button("Send Message")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</section>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if submit_button:
    if not name or not email or not message:
        st.error("Please fill in all fields.")
    else:
        st.success("Thank you for contacting us!")

st.markdown(
    """
<footer>
    <div class="footer-container">
    <div class="footer-links-container">
        <div class="footer-logo">MA Wellness</div>
            <div class="footer-links">
                <a href="#hero">Home</a>
                <a href="#how-it-works">How It Works</a>
                <a href="#membership-benefits">Benefits</a>
                <a href="#testimonials">Testimonials</a>
                <a href="#contact">Contact</a>
            </div>
            <div class="footer-links">
                <a href="#hero">About</a>
                <a href="#how-it-works">Blog</a>
                <a href="#membership-benefits">Financing</a>
                <a href="#testimonials">Patents</a>
                <a href="#contact">Therapy Locator</a>
            </div>
            <div class="social-icons">
                <a href="https://uzairkbrr.netlify.app/" aria-label="Portfolio" title="Portfolio">Portfolio</a>
                <a href="https://www.linkedin.com/in/uzairkbrr/" aria-label="LinkedIn" title="LinkedIn">Linkedin</a>
                <a href="https://github.com/uzairkbrr " aria-label="GitHub" title="GitHub">GitHub</a>
                <a href="https://x.com/uzairkbrr" aria-label="Twitter" title="Twitter">Twitter</a>
                <a href="https://www.facebook.com/uzairkbrr" aria-label="Facebook" title="Facebook">Facebook</a>
            </div>
        </div>
    </div>

</footer>
    """,
    unsafe_allow_html=True,
)


