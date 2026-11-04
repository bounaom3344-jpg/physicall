#python -m streamlit run app.py
import streamlit as st

st.set_page_config(page_title="ສື່ການສອນຟີຊິກ", page_icon="⚛️", layout="wide")

import lessons_basic as lb
import lessons_new as ln
import quiz

LESSONS = {
    "1. ການເຄື່ອນທີ່ຊື່": ln.linear_motion,
    "2. ແຮງ ແລະ ກົດຂອງນິວຕັນ": ln.force_lesson,
    "3. ງານ ແລະ ກຳລັງ": ln.work_lesson,
    "4. ພະລັງງານກົນ": ln.energy_lesson,
    "5. ແສງສະຫວ່າງ (ຫັກເຫ ແລະ ເລນ)": ln.light_lesson,
    "6. ໂປເຈັກໄທລ໌": lb.projectile,
    "7. ການສັ່ນຂອງສະປຣິງ": lb.oscillator,
    "8. ການແທກສອດຂອງຄື້ນ": lb.waves,
    "9. ພື້ນອຽງ ແລະ ແຮງສຽດທານ": lb.incline,
    "10. ການຊົນກັນ ແລະ ໂມເມັນຕຳ": lb.collision,
    "11. ສະໜາມໄຟຟ້າ ແລະ ສັກຂະໄຟຟ້າ": lb.efield,
    "12. ວົງຈອນ RC": lb.rc_circuit,
    "13. ແກັສອຸດົມຄະຕິ": lb.gas,
}

st.sidebar.title("⚛️ ສື່ການສອນຟີຊິກ")
mode = st.sidebar.radio("ໂໝດ", ["📘 ບົດຮຽນ (ສື່ການສອນ)", "📝 ແບບທົດສອບ"])
st.sidebar.divider()

if mode.startswith("📘"):
    topic = st.sidebar.radio("ເລືອກຫົວຂໍ້", list(LESSONS.keys()))
    LESSONS[topic]()
else:
    quiz.main()
