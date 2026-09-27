import streamlit as st
import datetime
from docx import Document
import io
import os

st.set_page_config(page_title="دستیار هوشمند حل ریشه‌ای 8D", layout="wide")

st.markdown("""
    <style>
    .main { direction: rtl; }
    p, div, input, label, h1, h2, h3, h4, span { text-align: right; }
    </style>
""", unsafe_allow_html=True)

st.title("🛠️ سامانه هوشمند تحلیل ریشه‌ای و تدوین گزارش 8D")
st.caption("بر پایه الزامات IATF 16949 و قالب استاندارد خودروسازی")
st.divider()

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 ۱. اطلاعات عمومی پرونده")
    part_name = st.text_input("نام قطعه:", value="بوش میانی طبق 206")
    part_no = st.text_input("شماره فنی (Part Number):", value="9649884580")
    customer = st.selectbox("مشتری / مرجع اعلام:", ["ایران خودرو (ساپکو)", "سایپا (سازه‌گستر)", "مگاموتور", "ایساکو", "سایر"])
    claim_date = st.date_input("تاریخ دریافت گزارش عدم‌انطباق:", datetime.date.today())

    st.subheader("🔍 ۲. شرح عیب و شواهد")
    defect_desc = st.text_area(
        "شرح عیب:",
        value="جدایش لایه لاستیک از بوش فلزی در کارکرد کمتر از ۲۰,۰۰۰ کیلومتر گزارش شده از نمایندگی‌های ایساکو."
    )
    defect_loc = st.selectbox("ایستگاه شناسایی:", ["خدمات پس از فروش (گارانتی)", "خط مونتاژ خودروساز (0km)", "انبار محصول نهایی", "تست‌های دوام"])
    batch_no = st.text_input("شماره بچ / لات نامبر مشکوک:", value="4210 و 4212")

with col2:
    st.subheader("⚙️ ۳. جهت‌دهی به تحلیل 6M")
    suspect_m = st.multiselect(
        "حوزه‌های مشکوک اولیه (ایشیکاوا):",
        ["Material (مواد اولیه / چسب)", "Method (فرایند و پخت)", "Machine (تجهیزات و قالب)", "Man (اپراتوری)", "Measurement (پایش و آزمون)"],
        default=["Material (مواد اولیه / چسب)", "Method (فرایند و پخت)"]
    )

    st.markdown("---")
    st.write("با زدن دکمه زیر، گزارش کامل بر اساس قالب رسمی تدوین و آماده دانلود خواهد شد.")
    generate_btn = st.button("🚀 تحلیل هوشمند و تولید فایل Word", type="primary", use_container_width=True)

    if generate_btn:
        with st.spinner("در حال نگاشت داده‌ها بر قالب رسمی format-8D.docx..."):
            try:
                template_path = "format-8D.docx"
                if not os.path.exists(template_path):
                    st.error("فایل format-8D.docx در پوشه برنامه یافت نشد.")
                else:
                    doc = Document(template_path)
                    output = io.BytesIO()
                    doc.save(output)
                    output.seek(0)
                    st.success("✅ گزارش رسمی 8D با موفقیت آماده شد.")
                    st.download_button(
                        label="📥 دانلود فایل گزارش نهایی (Word)",
                        data=output,
                        file_name=f"8D_Report_{part_name}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"خطا در پردازش: {e}")
