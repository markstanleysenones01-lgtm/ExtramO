import streamlit as st
import urllib.parse
# --- Custom CSS Styling for Dynamic UI ---
st.markdown(
    """
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        background-color: #ff4b4b;
        color: white;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #ff2222;
        box-shadow: 0 4px 12px rgba(255, 75, 75, 0.4);
    }
    div.stMetric {
        background-color: #1e1e2f;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #2d2d44;
    }
    </style>
""",
    unsafe_allow_html=True,
)
# --- App Header ---
st.title("⚡ ExtraMo")
st.caption("Turn extra client requests into extra revenue.")
# --- Dynamic Personal Greeting ---
st.markdown("### 👋 Welcome back! Ready to turn extra requests into cash?")
# --- Session State Management ---
if "free_uses_left" not in st.session_state:
    st.session_state["free_uses_left"] = 3

if "is_subscribed" not in st.session_state:
    st.session_state["is_subscribed"] = False

VALID_KEYS = ["EXTRA2026", "PRO_MEMBER_99", "FREELANCE_BOOST"]

# --- Sidebar Pro Activation ---
with st.sidebar:
    st.header("⚡ ExtraMo Pro")
    st.caption("Price: $10.00 / month")

    # Check if PayPal redirected back with ?pro=true
    query_params = st.query_params
    if query_params.get("pro") == "true":
        st.session_state["is_subscribed"] = True

    if st.session_state["is_subscribed"]:
        st.success("🟢 Pro Plan Active")
    else:
        st.warning(f"Free Plan: {st.session_state['free_uses_left']} uses remaining")

        st.markdown(
            "[👉 **Upgrade to Pro ($10/mo)**](https://www.paypal.com/ncp/payment/YOUR_PAYPAL_BUTTON_ID)"
        )
        st.divider()
    st.subheader("⏱️ Quick Rate Finder")
    q_hours = st.number_input("Hours Needed", min_value=1.0, value=5.0, step=1.0, key="q_hours")
    q_rate = st.number_input("Desired Rate ($/hr)", min_value=10.0, value=50.0, step=5.0, key="q_rate")
    q_total = q_hours * q_rate
    st.info(f"Recommended Quote: **${q_total:,.2f}**")
# --- Form Inputs ---
st.subheader("1. Request Details")
client_name = st.text_input("Client Name", placeholder="Acme Corp")
client_email = st.text_input("Client Email Address", placeholder="client@example.com")
uploaded_logo = st.file_uploader("Upload Company Logo (Optional)", type=["png", "jpg", "jpeg"])
if uploaded_logo is not None:
    st.image(uploaded_logo, width=150)
default_rate = st.number_input("Standard Hourly Rate ($)", value=120.0, step=10.0, min_value=0.0)
estimated_hours = st.number_input("Extra Hours Needed", min_value=0.5, value=3.0, step=0.5)
is_rush = st.checkbox("Mark as Rush / Priority Work (1.5x Rate)")

# --- Calculations ---
active_rate = default_rate * 1.5 if is_rush else default_rate
total_fee = estimated_hours * active_rate

st.divider()

# --- Financial Impact Display ---
st.subheader("2. Financial Impact")
st.metric("Effective Rate", f"${active_rate:.2f}/hr")
st.metric("Total Additional Fee", f"${total_fee:,.2f}")

if is_rush:
    st.warning("⚡ Priority Rate Applied (+50% surcharge)")

st.divider()

# --- Export & Email Generator Section ---
st.subheader("3. Client Response Generator")

can_access = st.session_state["is_subscribed"] or st.session_state["free_uses_left"] > 0

if not can_access:
    st.error("🔒 Free limit reached! You have used all 3 free change order drafts.")
    st.info("Subscribe for **$10.00/month** to get unlimited change orders and email exports.")
    st.markdown("[👉 **Click Here to Subscribe ($10.00/mo)**](https://buy.stripe.com/your_checkout_link_here)")
else:
    email_text = f"""Hi {client_name if client_name else 'there'},

Thanks for reaching out! Regarding the additional work requested:

I'd be happy to take care of this for you. Since this request falls outside our original contract scope, here is the estimate to complete it:

• Estimated Hours: {estimated_hours} hrs
• Rate: ${active_rate:.2f}/hr {'(Rush Rate)' if is_rush else ''}
• Additional Fee: ${total_fee:,.2f}

Please let me know if you approve this addition, and I will get started right away!

Best regards,"""
    st.code(email_text, language="text")
    if uploaded_logo is not None:
        st.image(uploaded_logo, width=120) 
# Direct Email Button
    encoded_subject = urllib.parse.quote("Change Order Estimate - Additional Requested Work")
    encoded_body = urllib.parse.quote(email_text)
    mailto_url = f"mailto:{client_email}?subject={encoded_subject}&body={encoded_body}"

    st.markdown(f'<a href="{mailto_url}" target="_blank" style="display: inline-block; padding: 10px 20px; background-color: #0088cc; color: white; text-decoration: none; border-radius: 5px; font-weight: bold;">✉️ Open in Email App & Send</a>', unsafe_allow_html=True)
# --- Save to History Button ---
if "scope_history" not in st.session_state:
    st.session_state["scope_history"] = []

if st.button("💾 Save to History"):
    history_item = {
        "client": client_name if client_name else "Unnamed Client",
        "fee": total_fee,
        "hours": estimated_hours,
    }
    st.session_state["scope_history"].append(history_item)
    st.success("Saved to history!")

# --- Display History & Dashboard Stats ---
if st.session_state.get("scope_history"):
    st.divider()
    st.subheader("📂 Saved Change Orders")
    for idx, item in enumerate(st.session_state["scope_history"], 1):
        st.text(f"{idx}. {item['client']} — ${item['fee']:,.2f} ({item['hours']} hrs)")

    # --- Lifetime Dashboard Stats (Calculated safely from history) ---
    total_rev = sum(item["fee"] for item in st.session_state["scope_history"])
    total_hrs = sum(item["hours"] for item in st.session_state["scope_history"])

    st.divider()
    st.subheader("📊 Your ExtraMo Dashboard")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Revenue Quoted", f"${total_rev:,.2f}")
    with col2:
        st.metric("Total Extra Hours", f"{total_hrs} hrs")

# --- Display History Sidebar or Section ---
if st.session_state.get("scope_history"):
    st.divider()
    st.subheader("📂 Saved Change Orders")
    for idx, item in enumerate(st.session_state["scope_history"], 1):
        st.text(
            f"{idx}. {item['client']} — ${item['fee']:,.2f} ({item['hours']} hrs)"
        )
# --- Lifetime Dashboard Stats ---
if "total_revenue_generated" not in st.session_state:
    st.session_state["total_revenue_generated"] = 0.0
if "total_hours_quoted" not in st.session_state:
    st.session_state["total_hours_quoted"] = 0.0

st.session_state["total_revenue_generated"] += total_fee
st.session_state["total_hours_quoted"] += estimated_hours

st.divider()
st.subheader("📊 Your ExtraMo Dashboard")
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Revenue Quoted", f"${st.session_state['total_revenue_generated']:,.2f}")
with col2:
    st.metric("Total Extra Hours", f"{st.session_state['total_hours_quoted']} hrs")
