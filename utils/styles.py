import streamlit as st


def inject_landing_theme() -> None:
    """Injects the global CSS theme used by the landing page across all pages."""
    st.markdown(
        """
<style>
/* --- Navbar Styles --- */
.navbar {
    position: sticky;
    top: 10px;
    margin: 10px 40px;
    background: rgba(30, 144, 255, 0.12);
    backdrop-filter: blur(12px) saturate(150%);
    -webkit-backdrop-filter: blur(12px) saturate(150%);
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.9rem 2rem;
    font-weight: 600;
    font-size: 1.05rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
    color: #1e90ff;
    z-index: 1000;
    margin: 20px auto;
    max-width: 1200px !important;
    width: 100%;
}

.brand-logo {
    font-weight: 800;
    font-size: 1.3rem;
    color: #1e90ff;
    cursor: pointer;
    letter-spacing: 0.5px;
    transition: color 0.3s ease;
}
.brand-logo:hover { color: #ffffff; }

.nav-links { display: flex; gap: 2.5rem; justify-content: center; flex-grow: 1; }
.nav-links a { color: #1e90ff; text-decoration: none; cursor: pointer; transition: all 0.3s ease; position: relative; }
.nav-links a:hover { color: #ffffff; }
.nav-links a::after { content: ""; position: absolute; bottom: -4px; left: 0; width: 0; height: 2px; background-color: #ffffff; transition: width 0.3s ease; }
.nav-links a:hover::after { width: 100%; }

.get-started-btn {
    background-color: #1e90ff; color: #fff; padding: 10px 26px; border-radius: 25px; text-decoration: none; font-weight: 700; cursor: pointer; border: none; font-size: 1rem; user-select: none; transition: all 0.3s ease;
}
.st-emotion-cache-9ajs8n a, .st-emotion-cache-18tdrd9 a { text-decoration: none; color: #fff; }
.get-started-btn:hover { background-color: #104e8b; }

/* Hero Section */
.hero { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 15rem 2rem; color: white; }
.hero h1 { font-size: 3rem; font-weight: 800; margin-bottom: 0.5rem; max-width: 700px; }
.hero p { font-size: 1.35rem; margin-bottom: 2rem; max-width: 650px; line-height: 1.6; }
.hero button { background-color: #1e90ff; color: #fff; border: none; padding: 16px 48px; font-size: 1.2rem; border-radius: 30px; cursor: pointer; font-weight: 700; transition: background-color 0.3s ease; user-select: none; }
.hero button:hover { background-color: #104e8b; }

/* How It Works Section */
#how-it-works { padding: 0 2rem 1rem 2rem; max-width: 900px; margin: 0 auto; text-align: center; }
#how-it-works h2 { font-size: 2.8rem; font-weight: 800; margin-bottom: 1.5rem; color: #fff; }
.steps-container { display: flex; justify-content: space-between; gap: 2rem; flex-wrap: wrap; margin-top: 2rem; }
.step-card { background-color: white; border-radius: 12px; box-shadow: 0 8px 16px rgba(0,0,0,0.1); padding: 2rem 1.5rem; flex: 1 1 250px; max-width: 15rem; display: flex; flex-direction: column; align-items: center; }
.step-number { font-size: 2.5rem; font-weight: 900; color: #1e90ff; margin-bottom: 1rem; user-select: none; }
.step-title { font-size: 1.3rem; font-weight: 700; margin-bottom: 0.75rem; color: #000; }
.step-desc { font-size: 1rem; color: #334155; line-height: 1.5; }

/* Membership Benefits */
#membership-benefits { max-width: 900px; margin: 0 auto 6rem auto; padding: 4rem 1rem 1rem 1rem; text-align: center; }
#membership-benefits h2 { font-size: 2.6rem; font-weight: 800; margin-bottom: 1.8rem; }
.benefits-container { display: flex; justify-content: space-between; gap: 2rem; flex-wrap: wrap; }
.benefit-card { background-color: white; border-radius: 12px; box-shadow: 0 8px 20px rgba(0,0,0,0.08); padding: 1.8rem 1.2rem; flex: 1 1 200px; max-width: 280px; display: flex; flex-direction: column; align-items: center; }
.benefit-icon { font-size: 3.5rem; margin-bottom: 1rem; color: #1e90ff; user-select: none; }
.benefit-title { font-weight: 700; font-size: 1.3rem; margin-bottom: 0.75rem; color: #334155; }
.benefit-desc { font-size: 1rem; color: #334155; line-height: 1.4; }

/* Testimonials */
#testimonials { max-width: 900px; margin: 0 auto 6rem auto; padding: 2rem 1rem; text-align: center; color: #0f172a; }
#testimonials h2 { font-size: 2.6rem; font-weight: 800; margin-bottom: 2rem; color: #fff; }
.testimonials-container { display: flex; overflow-x: auto; gap: 3rem; scroll-behavior: smooth; padding-bottom: 1rem; margin-left: 20px;}
.testimonials-container::-webkit-scrollbar { display: none; }
.testimonials-container { -ms-overflow-style: none; scrollbar-width: none; }
.testimonial-card { background-color: white; border-radius: 14px; box-shadow: 0 8px 20px rgba(0,0,0,0.08); padding: 2rem 1.5rem; flex: 0 0 250px; display: flex; flex-direction: column; align-items: center; user-select: none; }
.testimonial-photo { width: 72px; height: 72px; border-radius: 50%; object-fit: cover; margin-bottom: 1.25rem; box-shadow: 0 4px 12px rgba(30, 144, 255, 0.3); }
.testimonial-quote { font-style: italic; font-size: 1rem; color: #334155; margin-bottom: 1rem; min-height: 80px; }
.testimonial-name { font-weight: 700; font-size: 1.1rem; color: #1e90ff; }

/* Pricing */
#pricing { max-width: 1200px; margin: 0 auto 6rem auto; padding: 2rem 1rem; text-align: center; }
#pricing h2 { font-size: 2.6rem; font-weight: 800; margin-bottom: 2rem; }
.pricing-cards { display: flex; justify-content: center; gap: 2rem; }
.pricing-card { background: white; border-radius: 12px; box-shadow: 0 8px 20px rgba(0,0,0,0.08); padding: 2rem 1.5rem; flex: 1 1 400px; max-width: 350px; width: 100%; text-align: left; color: #334155; display: flex; flex-direction: column; justify-content: space-between; }
.pricing-card h3 { font-weight: 700; font-size: 1.5rem; margin-bottom: 0.5rem; color: #1e90ff; }
.pricing-card p.description { color: #555; font-style: italic; margin-bottom: 1rem; }
.pricing-card ul { line-height: 1.5; margin-bottom: 1.5rem; list-style: none; }
.pricing-card ul li { margin-bottom: 0.4rem; }
.pricing-card p.price { font-weight: 800; font-size: 1.3rem; color: #1e90ff; margin-bottom: 1rem; }
.pricing-card button { background-color: #1e90ff; color: white; padding: 10px 26px; border-radius: 25px; font-weight: 700; border: none; cursor: pointer; width: 100%; user-select: none; transition: background-color 0.3s ease; }
.pricing-card button:hover { background-color: #104e8b; }

/* Responsive */
@media (max-width: 768px) {
  .steps-container, .benefits-container, .pricing-cards { flex-direction: column; align-items: center; }
  .step-card, .benefit-card, .pricing-card { max-width: 90vw; margin-bottom: 1.5rem; }
  .testimonials-container { flex-direction: column; overflow-x: visible; }
  .testimonial-card { flex: none; width: 90vw; max-width: none; margin-bottom: 1.5rem; }
}

#faq { max-width: 900px; margin: 0 auto; padding: 2rem 1rem 0 1rem; color: #0f172a; user-select: none; }
#faq h2 { font-size: 2.6rem; font-weight: 800; margin-bottom: 2rem; text-align: center; color: #fff; }
.stExpander > div[role="button"] { font-weight: 700 !important; font-size: 1.2rem !important; color: #1e90ff !important; user-select: none; cursor: pointer; }
.st-emotion-cache-p6n0jw { max-width: 900px; margin: 0 auto; }
.stExpanderContent { max-width: 900px !important; margin: 0 auto !important; color: #334155; font-size: 1rem; line-height: 1.5; }
.st-emotion-cache-9ajs8n h2{ margin: 0 auto; max-width: 900px; width: 100%; font-size: 2.6rem; font-weight: 800; padding-bottom: 0; color: #fff; }
.st-emotion-cache-zuyloh { max-width: 900px; width: 100%; margin: 0 auto; }

footer { position: sticky; bottom: 0; margin: 10px 40px 20px 40px; background: rgba(30, 144, 255, 0.15); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border-radius: 15px; padding: 1.5rem 2rem; color: #1e90ff; font-size: 0.9rem; user-select: none; box-shadow: 0 8px 32px 0 rgba(30, 144, 255, 0.1); z-index: 1000; max-width: 1200px !important; margin-left: auto; margin-right: auto; }
.footer-links-container { display: flex; align-items: start; justify-content: space-around; margin-top: 30px; }
footer .footer-logo { font-weight: 700; font-size: 1.3rem; cursor: default; }
footer .footer-links { display: flex; flex-direction: column; gap: 7px; flex-wrap: wrap; font-size: 1rem; justify-content: center; }
footer .footer-links a { color: #1e90ff; text-decoration: none; font-weight: 600; position: relative; transition: color 0.3s ease; }
footer .footer-links a::after, { content: ""; position: absolute; bottom: -4px; left: 0; width: 0; height: 2px; background-color: #ffffff; transition: width 0.3s ease; }
footer .footer-links a:hover { color: #fff; }
.footer-links a:hover::after{ width: 100%; }
footer .social-icons { display: flex; gap: 7px; justify-content: center; flex-direction: column; }
footer .social-icons a { color: #1e90ff; font-size: 1rem; text-decoration: none; transition: color 0.3s ease; position: relative; }
footer .social-icons a::after { content: ""; position: absolute; bottom: -4px; left: 0; width: 0; height: 2px; background-color: #ffffff; transition: width 0.3s ease; }
footer .social-icons a:hover::after { width: 100%; }
footer .social-icons a:hover { color: #fff; }
.footer-author {text-align: center; margin-top: 20px; display: relative; transition: all .5s}

@media (max-width: 480px) { footer { flex-direction: column; gap: 1.5rem; } }

/* --- Dashboard Cards --- */
.kpi-grid {
  display: flex;
  gap: 1rem;
  margin: 0.75rem 0 1.25rem 0;
  flex-wrap: wrap;
  overflow-x: visible;
}
.kpi-card {
  background: rgba(255, 255, 255, 0.66);
  backdrop-filter: blur(10px) saturate(160%);
  -webkit-backdrop-filter: blur(10px) saturate(160%);
  border-radius: 16px;
  box-shadow: 0 10px 28px rgba(0,0,0,0.12);
  padding: 1rem 1.2rem;
  border: 1px solid rgba(30,144,255,0.16);
  box-sizing: border-box;
  flex: 1 1 calc(25% - 1rem);
  min-width: 200px;
}
.kpi-card .label { color: #0f172a; font-size: 0.92rem; margin-bottom: 0.35rem; opacity: 0.9; font-weight: 600; }
.kpi-card .value { color: #0f172a; font-size: 1.8rem; font-weight: 900; }
.kpi-card .sub { color: #334155; font-size: 0.85rem; opacity: 0.9; }

/* Card-specific accents */
.kpi-card.meals {
  background: rgba(34, 197, 94, 0.12);
  border-color: rgba(34, 197, 94, 0.25);
}
.kpi-card.meals .label, .kpi-card.meals .value { color: #16a34a; }

.kpi-card.workouts {
  background: rgba(245, 158, 11, 0.12);
  border-color: rgba(245, 158, 11, 0.25);
}
.kpi-card.workouts .label, .kpi-card.workouts .value { color: #d97706; }

.kpi-card.challenges {
  background: rgba(168, 85, 247, 0.12);
  border-color: rgba(168, 85, 247, 0.25);
}
.kpi-card.challenges .label, .kpi-card.challenges .value { color: #a855f7; }

.kpi-card.calories {
  background: rgba(30, 144, 255, 0.12);
  border-color: rgba(30, 144, 255, 0.25);
}
.kpi-card.calories .label, .kpi-card.calories .value { color: #1e90ff; }

/* Responsive layout: 4 → 2 → 1 cards per row */
@media (max-width: 1024px) {
  .kpi-card { flex: 1 1 calc(50% - 1rem); }
}
@media (max-width: 560px) {
  .kpi-card { flex: 1 1 100%; min-width: unset; }
}

.section-card {
  background: rgba(255, 255, 255, 0.66);
  backdrop-filter: blur(10px) saturate(160%);
  -webkit-backdrop-filter: blur(10px) saturate(160%);
  border-radius: 16px; padding: 1.1rem 1.3rem; margin: 0.75rem 0 1.25rem 0;
  box-shadow: 0 10px 28px rgba(0,0,0,0.10);
  border: 1px solid rgba(30,144,255,0.16);
}
.section-card h3 { margin: 0 0 0.75rem 0; color: #0f172a; }
.pill { display: inline-block; padding: 3px 10px; border-radius: 999px; background: rgba(30,144,255,0.16); color: #1e90ff; font-size: 0.78rem; margin-left: 8px; }
.progress-row { display:flex; align-items:center; gap: 10px; margin: 6px 0; }
.progress-label { flex: 0 0 160px; color:#334155; font-size: 0.9rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

/* Year toggle buttons styling (GitHub-style) */
.year-toggle-container {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin: 15px 0;
  flex-wrap: wrap;
}

.year-toggle-container .stButton > button {
  min-width: 60px;
  height: 32px;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 600;
  transition: all 0.2s ease;
  border: 1px solid rgba(30, 144, 255, 0.2);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.year-toggle-container .stButton > button[data-baseweb="button"] {
  background-color: rgba(255, 255, 255, 0.9);
  color: #334155;
}

.year-toggle-container .stButton > button[data-baseweb="button"]:hover {
  background-color: rgba(30, 144, 255, 0.1);
  border-color: rgba(30, 144, 255, 0.4);
  transform: translateY(-1px);
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15);
}

.year-toggle-container .stButton > button[data-baseweb="button"][aria-pressed="true"],
.year-toggle-container .stButton > button[data-baseweb="button"].st-emotion-cache-1aehpvj {
  background-color: #1e90ff;
  color: white;
  border-color: #1e90ff;
  box-shadow: 0 2px 8px rgba(30, 144, 255, 0.3);
}

.year-toggle-container .stButton > button[data-baseweb="button"][aria-pressed="true"]:hover {
  background-color: #1976d2;
  border-color: #1976d2;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(30, 144, 255, 0.4);
}

/* Mobile responsive design for year toggles */
@media (max-width: 480px) {
  .year-toggle-container {
    gap: 6px;
    margin: 10px 0;
  }

  .year-toggle-container .stButton > button {
    min-width: 50px;
    height: 28px;
    font-size: 0.8rem;
  }
}

/* Streak visualization improvements */
.streak-section {
  margin: 20px 0;
}

.streak-info {
  margin-bottom: 15px;
}

/* Heatmap legend styling */
.heatmap-legend {
  margin-top: 15px;
  text-align: center;
  font-size: 0.85rem;
  color: #666;
  padding: 10px;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 8px;
  backdrop-filter: blur(5px);
}

.legend-item {
  display: inline-block;
  margin-right: 20px;
  align-items: center;
}

.legend-color {
  display: inline-block;
  width: 12px;
  height: 12px;
  margin-right: 5px;
  border-radius: 2px;
  vertical-align: middle;
}

/* Responsive design for mobile */
@media (max-width: 480px) {
  .legend-item {
    margin-right: 15px;
    font-size: 0.8rem;
  }

  .legend-color {
    width: 10px;
    height: 10px;
  }
}

.st-emotion-cache-9ajs8n h1,
.st-emotion-cache-vqhohv p,
.st-emotion-cache-9ajs8n h3,
.st-emotion-cache-9ajs8n h3,
.st-emotion-cache-4rp1ik,
.st-emotion-cache-13na8ym,
.st-emotion-cache-a0ovpn,
.st-emotion-cache-v3w3zg,
.st-emotion-cache-8fjoqp,
.st-emotion-cache-1i94pul,
.st-emotion-cache-9ajs8n p,
.st-emotion-cache-18kf3ut,
.st-emotion-cache-18tdrd9 h2,
.st-emotion-cache-tn0cau,
.st-emotion-cache-zy6yx3,
.st-emotion-cache-8fjoqp
{
  max-width: 1100px;
  width: 100%;
  margin-inline: auto;
}

#hero p {
  margin-bottom: 30px;
}

.st-emotion-cache-1i94pul {
  padding: 2rem;
  border-radius: 16px;
}

.st-emotion-cache-zy6yx3 {
    padding-block: 2rem;
}

.st-emotion-c,
.st-emotion-cache-rra9ig > div:first-child,
.st-emotion-cache-1permvm > div:first-child {
  display: none;
}

</style>
        """,
        unsafe_allow_html=True,
    )


