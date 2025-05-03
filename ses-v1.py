import streamlit as st
import pandas as pd
import qrcode
from PIL import Image
import io
import base64
from datetime import datetime

# Streamlit page configuration
st.set_page_config(page_title="Startup Essentials Suite", layout="wide")

# App title and description
st.title("🚀 Startup Essentials Suite")
st.markdown("""
Welcome to the **Startup Essentials Suite**, an all-in-one toolkit for early-stage startups!  
Access tools to create business plans, generate invoices, craft AI-powered ad copy, track marketing tasks, and create QR codes—all from one dashboard.
""")

# Sidebar for navigation
st.sidebar.header("Navigation")
tool = st.sidebar.selectbox("Select Tool", [
    "Business Plan Writer",
    "Invoice Generator",
    "AI Advertising Writer",
    "Marketing Checklist",
    "QR Code Generator"
])

# Business Plan Writer
if tool == "Business Plan Writer":
    st.header("📝 Business Plan Writer")
    st.write("Create a professional business plan with guided inputs and downloadable output.")

    with st.form("business_plan_form"):
        company_name = st.text_input("Company Name")
        mission = st.text_area("Mission Statement")
        market = st.text_area("Target Market")
        strategy = st.text_area("Business Strategy")
        financials = st.text_area("Financial Projections (e.g., revenue, costs)")
        submit = st.form_submit_button("Generate Business Plan")

        if submit:
            business_plan = f"""
# {company_name} Business Plan
## Mission Statement
{mission}

## Target Market
{market}

## Business Strategy
{strategy}

## Financial Projections
{financials}
"""
            st.session_state['business_plan'] = business_plan
            st.success("Business plan generated!")
            st.markdown(business_plan)

            # Download as text file
            b = io.BytesIO(business_plan.encode())
            st.download_button(
                label="Download Business Plan",
                data=b,
                file_name=f"{company_name}_business_plan.txt",
                mime="text/plain"
            )

# Invoice Generator
elif tool == "Invoice Generator":
    st.header("💸 Simple Invoice Generator")
    st.write("Generate professional invoices for your clients.")

    with st.form("invoice_form"):
        client_name = st.text_input("Client Name")
        client_email = st.text_input("Client Email")
        item_desc = st.text_area("Item/Service Description")
        amount = st.number_input("Amount ($)", min_value=0.0, step=0.01)
        due_date = st.date_input("Due Date")
        submit = st.form_submit_button("Generate Invoice")

        if submit:
            invoice = f"""
# Invoice
**From:** {st.session_state.get('company_name', 'Your Startup')}  
**To:** {client_name}  
**Email:** {client_email}  
**Date:** {datetime.now().strftime('%Y-%m-%d')}  
**Due Date:** {due_date}

## Item/Service
{item_desc}

## Amount
${amount:.2f}

**Payment Instructions:** Pay via [Your Payment Gateway Link]
"""
            st.success("Invoice generated!")
            st.markdown(invoice)

            # Download as text file
            b = io.BytesIO(invoice.encode())
            st.download_button(
                label="Download Invoice",
                data=b,
                file_name=f"invoice_{client_name}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )

# AI Advertising Writer
elif tool == "AI Advertising Writer":
    st.header("📢 AI Advertising Writer")
    st.write("Generate ad copy for your startup's marketing campaigns.")

    with st.form("ad_writer_form"):
        product = st.text_input("Product/Service Name")
        audience = st.text_input("Target Audience (e.g., young professionals)")
        platform = st.selectbox("Platform", ["Google Ads", "Social Media", "Email"])
        tone = st.selectbox("Tone", ["Professional", "Casual", "Exciting"])
        submit = st.form_submit_button("Generate Ad Copy")

        if submit:
            # Simulated AI-generated ad copy
            ad_copy = f"🚀 Discover {product}! Perfect for {audience}. {'Get started now!' if tone == 'Exciting' else 'Learn more today!'} #{'StartupSuccess' if platform == 'Social Media' else product.replace(' ', '')}"
            if platform == "Google Ads":
                ad_copy = f"{product} for {audience} - {tone.lower()} and effective. Click to explore!"
            elif platform == "Email":
                ad_copy = f"Subject: {product} Awaits You!\n\nHi {audience},\n\nExperience {product} with a {tone.lower()} approach. {'Join now!' if tone == 'Exciting' else 'Find out more!'}\n\nBest,\nYour Startup"

            st.success("Ad copy generated!")
            st.markdown(ad_copy)

            # Download as text file
            b = io.BytesIO(ad_copy.encode())
            st.download_button(
                label="Download Ad Copy",
                data=b,
                file_name=f"ad_copy_{product}.txt",
                mime="text/plain"
            )

# Marketing Checklist
elif tool == "Marketing Checklist":
    st.header("✅ Business Marketing Checklist")
    st.write("Track your marketing tasks with this step-by-step checklist.")

    # Sample checklist
    checklist = {
        "Define target audience": False,
        "Create social media profiles": False,
        "Launch website": False,
        "Set up email marketing": False,
        "Run first ad campaign": False
    }

    if 'checklist' not in st.session_state:
        st.session_state['checklist'] = checklist

    with st.form("checklist_form"):
        for task in st.session_state['checklist']:
            st.session_state['checklist'][task] = st.checkbox(task, value=st.session_state['checklist'][task])
        submit = st.form_submit_button("Save Checklist")

        if submit:
            st.success("Checklist updated!")
            progress = sum(st.session_state['checklist'].values()) / len(st.session_state['checklist'])
            st.progress(progress)
            st.write(f"Progress: {progress*100:.0f}% complete")

# QR Code Generator
elif tool == "QR Code Generator":
    st.header("🔲 Static QR Code Generator")
    st.write("Create QR codes for your website, payment pages, or promotional materials.")

    with st.form("qr_form"):
        url = st.text_input("Enter URL (e.g., website, payment link)")
        submit = st.form_submit_button("Generate QR Code")

        if submit and url:
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(url)
            qr.make(fit=True)
            img = qr.make_image(fill="black", back_color="white")

            # Save QR code to bytes
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.image(byte_im, caption="Your QR Code", use_column_width=False)
            st.download_button(
                label="Download QR Code",
                data=byte_im,
                file_name="qrcode.png",
                mime="image/png"
            )

# Footer
st.markdown("---")
st.write("Built with ❤️ by xAI | Startup Essentials Suite © 2025")
