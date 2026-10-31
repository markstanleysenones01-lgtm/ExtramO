import streamlit as st
import urllib.parse
# --- App Header ---
st.title("⚡ ExtraMo")
st.caption("Turn extra client requests into extra revenue.")

# --- Session State Management ---
if "free_uses_left" not in st.session_state:
    st.session_state["free_uses_left"] = 3

if "is_subscribed" not in st.session_state:
    st.session_state["is_subscribed"] = False

VALID_KEYS = ["EXTRA2026", "PRO_MEMBER_99", "FREELANCE_BOOST"]

# --- Sidebar Pro Activation ---
with st.sidebar:
    st.header("⚡ ExtraMo Pro")
    st.caption("Price: $10.00/ month")
    
    if st.session_state["is_subscribed"]:
        st.success("🟢 Pro Plan Active")
    else:
        st.warning(f"Free Plan: {st.session_state['free_uses_left']} uses remaining")
        
        st.subheader("🔑 Activate Pro Account")
        key_input = st.text_input("Enter License Key", type="password")
        if st.button("Unlock Unlimited Access"):
            if key_input.strip() in VALID_KEYS:
                st.session_state["is_subscribed"] = True
                st.success("Successfully upgraded to Pro!")
                st.rerun()
            else:
                st.error("Invalid Key")

st.divider()

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
    st.info("Subscribe for **$25.00/month** to get unlimited change orders and email exports.")
    st.markdown("[👉 **Click Here to Subscribe ($5.99/mo)**](https://buy.stripe.com/your_checkout_link_here)")
else:
    email_text = f"""Hi {client_name if client_name else 'there'},

Thanks for reaching out! Regarding the additional work requested:

I'd be happy to take care of this for you. Since this request falls outside our original contract scope, here is the estimate to complete it:

• Estimated Hours: {estimated_hours} hrs
• Rate: ${active_rate:.2f}/hr {'(Rush Rate)' if is_rush else ''}
• Additional Fee: ${total_fee:,.2f}

Please let me know if you approve this addition, and I will get started right away!

Best regards,"""
if uploaded_logo is not None:
        st.image(uploaded_logo, width=120)
    st.code(email_text, language="text")
    # Direct Email Button
    encoded_subject = urllib.parse.quote("Change Order Estimate - Additional Requested Work")
    encoded_body = urllib.parse.quote(email_text)
    mailto_url = f"mailto:{client_email}?subject={encoded_subject}&body={encoded_body}"

    st.markdown(f'<a href="{mailto_url}" target="_blank" style="display: inline-block; padding: 10px 20px; background-color: #0088cc; color: white; text-decoration: none; border-radius: 5px; font-weight: bold;">✉️ Open in Email App & Send</a>', unsafe_allow_html=True)
# --- Currency Switcher ---
currency_options = {
    "USD ($)": "$",
    "EUR (€)": "€",
    "GBP (£)": "£",
    "AED (د.إ)": "د.إ",}
selected_currency = st.selectbox("Currency", list(currency_options.keys()))
curr_symbol = currency_options[selected_currency]
st.metric("Effective Rate", f"{curr_symbol}{active_rate:,.2f}/hr")
st.metric("Total Additional Fee", f"{curr_symbol}{total_fee:,.2f}")
email_text = f"""Hi {client_name if client_name else 'there'},

Thanks for reaching out! Regarding the additional work requested:

I'd be happy to take care of this for you. Since this request falls outside our original contract scope, here is the estimate to complete it:

- Estimated Hours: {estimated_hours} hrs
- Rate: {curr_symbol}{active_rate:,.2f}/hr {'(Rush Rate)' if is_rush else ''}
- Additional Fee: {curr_symbol}{total_fee:,.2f}

Please let me know if you approve this addition, and I will get started right away!

Best regards,"""
