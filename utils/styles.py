import streamlit as st


def inject_landing_theme() -> None:
    """Injects the global CSS theme used by the landing page across all pages."""
    st.markdown(
        """
<style>

/* Custom styles for contact form header and faq questions container */
.st-emotion-cache-zy6yx3 {
    padding-block: 2rem;
}
.st-emotion-cache-18kf3ut , .st-emotion-cache-18tdrd9 h2{
    max-width: 800px;
    width: 100%;
    margin: 0 auto;
}

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
#how-it-works { padding: 0 2rem 4rem 2rem; max-width: 900px; margin: 0 auto; text-align: center; }
#how-it-works h2 { font-size: 2.8rem; font-weight: 800; margin-bottom: 1.5rem; color: #fff; }
.steps-container { display: flex; justify-content: space-between; gap: 2rem; flex-wrap: wrap; margin-top: 2rem; }
.step-card { background-color: white; border-radius: 12px; box-shadow: 0 8px 16px rgba(0,0,0,0.1); padding: 2rem 1.5rem; flex: 1 1 250px; max-width: 15rem; display: flex; flex-direction: column; align-items: center; }
.step-number { font-size: 2.5rem; font-weight: 900; color: #1e90ff; margin-bottom: 1rem; user-select: none; }
.step-title { font-size: 1.3rem; font-weight: 700; margin-bottom: 0.75rem; color: #000; }
.step-desc { font-size: 1rem; color: #334155; line-height: 1.5; }

/* Membership Benefits */
#membership-benefits { max-width: 900px; margin: 0 auto 6rem auto; padding: 2rem 1rem; text-align: center; }
#membership-benefits h2 { font-size: 2.6rem; font-weight: 800; margin-bottom: 1.8rem; }
.benefits-container { display: flex; justify-content: space-between; gap: 2rem; flex-wrap: wrap; }
.benefit-card { background-color: white; border-radius: 12px; box-shadow: 0 8px 20px rgba(0,0,0,0.08); padding: 1.8rem 1.2rem; flex: 1 1 200px; max-width: 280px; display: flex; flex-direction: column; align-items: center; }
.benefit-icon { font-size: 3.5rem; margin-bottom: 1rem; color: #1e90ff; user-select: none; }
.benefit-title { font-weight: 700; font-size: 1.3rem; margin-bottom: 0.75rem; color: #334155; }
.benefit-desc { font-size: 1rem; color: #334155; line-height: 1.4; }

/* Testimonials */
#testimonials { max-width: 900px; margin: 0 auto 6rem auto; padding: 2rem 1rem; text-align: center; color: #0f172a; }
#testimonials h2 { font-size: 2.6rem; font-weight: 800; margin-bottom: 2rem; color: #fff; }
.testimonials-container { display: flex; overflow-x: auto; gap: 2rem; scroll-behavior: smooth; padding-bottom: 1rem; }
.testimonials-container::-webkit-scrollbar { display: none; }
.testimonials-container { -ms-overflow-style: none; scrollbar-width: none; }
.testimonial-card { background-color: white; border-radius: 14px; box-shadow: 0 8px 20px rgba(0,0,0,0.08); padding: 2rem 1.5rem; flex: 0 0 250px; display: flex; flex-direction: column; align-items: center; user-select: none; }
.testimonial-photo { width: 72px; height: 72px; border-radius: 50%; object-fit: cover; margin-bottom: 1.25rem; box-shadow: 0 4px 12px rgba(30, 144, 255, 0.3); }
.testimonial-quote { font-style: italic; font-size: 1rem; color: #334155; margin-bottom: 1rem; min-height: 80px; }
.testimonial-name { font-weight: 700; font-size: 1.1rem; color: #1e90ff; }

/* Pricing */
#pricing { max-width: 1200px; margin: 0 auto 6rem auto; padding: 2rem 1rem; text-align: center; }
#pricing h2 { font-size: 2.6rem; font-weight: 800; margin-bottom: 2rem; }
.pricing-cards { display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap; }
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

#faq { max-width: 800px; margin: 0 auto; padding: 2rem 1rem 0 1rem; color: #0f172a; user-select: none; }
#faq h2 { font-size: 2.6rem; font-weight: 800; margin-bottom: 2rem; text-align: center; color: #fff; }
.stExpander > div[role="button"] { font-weight: 700 !important; font-size: 1.2rem !important; color: #1e90ff !important; user-select: none; cursor: pointer; }
.st-emotion-cache-p6n0jw { max-width: 800px; margin: 0 auto; }
.stExpanderContent { max-width: 800px !important; margin: 0 auto !important; color: #334155; font-size: 1rem; line-height: 1.5; }
.st-emotion-cache-9ajs8n h2{ margin: 0 auto; max-width: 800px; width: 100%; font-size: 2.6rem; font-weight: 800; padding-bottom: 0; color: #fff; }
.st-emotion-cache-zuyloh { max-width: 800px; width: 100%; margin: 0 auto; }

footer { position: sticky; bottom: 0; margin: 10px 40px 20px 40px; background: rgba(30, 144, 255, 0.15); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border-radius: 15px; padding: 1.5rem 2rem; color: #1e90ff; font-size: 0.9rem; user-select: none; box-shadow: 0 8px 32px 0 rgba(30, 144, 255, 0.1); z-index: 1000; max-width: 1200px; margin-left: auto; margin-right: auto; }
.footer-links-container { display: flex; align-items: start; justify-content: space-around; margin-top: 30px; }
footer .footer-logo { font-weight: 700; font-size: 1.3rem; cursor: default; }
footer .footer-links { display: flex; flex-direction: column; gap: 7px; flex-wrap: wrap; font-size: 1rem; justify-content: center; }
footer .footer-links a { color: #1e90ff; text-decoration: none; font-weight: 600; position: relative; transition: color 0.3s ease; }
footer .footer-links a::after { content: ""; position: absolute; bottom: -4px; left: 0; width: 0; height: 2px; background-color: #ffffff; transition: width 0.3s ease; }
footer .footer-links a:hover { color: #fff; }
.footer-links a:hover::after { width: 100%; }
footer .social-icons { display: flex; gap: 7px; justify-content: center; flex-direction: column; }
footer .social-icons a { color: #1e90ff; font-size: 1rem; text-decoration: none; transition: color 0.3s ease; position: relative; }
footer .social-icons a::after { content: ""; position: absolute; bottom: -4px; left: 0; width: 0; height: 2px; background-color: #ffffff; transition: width 0.3s ease; }
footer .social-icons a:hover::after { width: 100%; }
footer .social-icons a:hover { color: #fff; }

@media (max-width: 480px) { footer { flex-direction: column; gap: 1.5rem; } }
</style>
        """,
        unsafe_allow_html=True,
    )


