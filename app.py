import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd

# ==========================================
# 🛡️ কনফিগারেশন
# ==========================================
st.set_page_config(page_title="Sangs-Karak AI: Digital Auditor", page_icon="🕵️‍♂️", layout="wide")

# এখানে আপনার এপিআই কী বসান
API_KEY = "AIzaSyCnhA3RiEnyIRD0F0ODfCa1K_I3V7rQnpM" 

try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error("API Key missing or invalid!")

# ==========================================
# 🧠 এআই ফোরেনসিক লজিক
# ==========================================
def analyze_corruption_advanced(data, image=None):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    You are 'Sangs-Karak AI', a Digital Forensic Auditor specializing in Bangladesh's Public Sector.
    Analyze this case based on the 'Mymensingh Zila Parishad' corruption patterns (Ghost institutions, Syndicate allocation, No-application grants).

    CASE DATA:
    - Institution: {data['inst_name']}
    - Type: {data['inst_type']}
    - Allocation Amount: {data['amount']} BDT
    - Location: {data['location']}
    - Key Person/Advocate: {data['person']}
    - Allegation: {data['desc']}
    - Verified by User: Has Physical Building? {data['has_build']}, Has Signboard? {data['has_sign']}

    YOUR TASK:
    1. **Risk Score (0-100%):** Calculate the probability of this being a 'Ghost Project' or 'Syndicate Nexus'.
    2. **Pattern Matching:** Does this match the 'Mymensingh Model' (Official-Political nexus)?
    3. **Audit Questions:** What specific documents should the Auditor/ACC ask for?
    4. **ACC Formal Draft:** Write a formal complaint letter to the ACC (দুদক) Chairman in Bangla.

    Format the output in professional Bangla with clear headings.
    """
    
    if image:
        response = model.generate_content([prompt, image])
    else:
        response = model.generate_content(prompt)
    return response.text

# ==========================================
# 🎨 আধুনিক ইউজার ইন্টারফেস (UI)
# ==========================================
st.markdown("<h1 style='text-align: center; color: #E63946;'>🛡️ ডিজিটাল সংস্-কারক (Digital Auditor v2.0)</h1>", unsafe_allow_html=True)
st.write("<h4 style='text-align: center;'>সিস্টেমিক দুর্নীতি ও অস্তিত্বহীন প্রতিষ্ঠান শনাক্তকারী এআই</h4>", unsafe_allow_html=True)
st.markdown("---")

# ইনপুট সেকশন
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🏢 প্রতিষ্ঠানের তথ্য")
    inst_name = st.text_input("প্রতিষ্ঠানের নাম (যেমন: মাদ্রাসার নাম)")
    inst_type = st.selectbox("ধরন", ["শিক্ষা প্রতিষ্ঠান/মাদ্রাসা", "কবরস্থান/মসজিদ", "ক্লাব/লাইব্রেরি", "অন্যান্য"])
    location = st.text_input("অবস্থান (গ্রাম/ইউনিয়ন/উপজেলা)")
    amount = st.number_input("বরাদ্দকৃত টাকার পরিমাণ (BDT)", min_value=0)
    person = st.text_input("বরাদ্দের পেছনে মূল ব্যক্তি (নাম/রাজনৈতিক পরিচয়)")

with col2:
    st.subheader("🕵️ মাঠ পর্যায়ের সত্যতা")
    has_build = st.radio("সেখানে কি কোনো বাস্তব ভবন/ঘর আছে?", ["হ্যাঁ", "না", "অর্ধ-পাকা/অস্পষ্ট"])
    has_sign = st.radio("কোনো সাইনবোর্ড আছে কি?", ["হ্যাঁ", "না", "নতুন লাগানো হয়েছে"])
    desc = st.text_area("অনিয়মের বিবরণ (যেমন: আবেদন না করেই টাকা পেয়েছে, একই ব্যক্তি একাধিক নামে টাকা তুলছে)")
    uploaded_file = st.file_uploader("প্রমাণ হিসেবে ছবি দিন (ঐচ্ছিক)", type=["jpg", "png", "jpeg"])

# সাবমিট বাটন
st.markdown("---")
if st.button("🚀 এআই ফরেনসিক অডিট শুরু করুন", use_container_width=True):
    if not inst_name or not desc:
        st.warning("দয়া করে প্রয়োজনীয় তথ্য দিন।")
    else:
        with st.spinner('🤖 এআই তথ্য বিশ্লেষণ করছে এবং দুর্নীতির প্যাটার্ন খুঁজছে...'):
            # তথ্য গুছিয়ে নেওয়া
            case_data = {
                "inst_name": inst_name, "inst_type": inst_type, "amount": amount,
                "location": location, "person": person, "desc": desc,
                "has_build": has_build, "has_sign": has_sign
            }
            
            image_part = Image.open(uploaded_file) if uploaded_file else None
            
            try:
                result = analyze_corruption_advanced(case_data, image_part)
                st.success("অডিট রিপোর্ট তৈরি হয়েছে!")
                st.markdown(result)
                
                # এক্সপোর্ট অপশন
                st.download_button("ডাউনলোড রিপোর্ট (PDF/Text)", result, file_name="Audit_Report.txt")
                
            except Exception as e:
                st.error(f"Error: {e}")

# Footer
st.markdown("---")
st.caption("© ২০২৫ ডিজিটাল সংস্-কারক প্রজেক্ট | সত্য ও স্বচ্ছতার জন্য এআই")
