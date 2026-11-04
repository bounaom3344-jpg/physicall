# ບົດຮຽນຫຼັກ 5 ຫົວຂໍ້: ການເຄື່ອນທີ່ຊື່, ແຮງ, ງານ, ພະລັງງານ, ແສງສະຫວ່າງ
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st


def style(fig, xt, yt, title, height=460):
    fig.update_layout(
        title=title,
        xaxis_title=xt,
        yaxis_title=yt,
        height=height,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", y=-0.2),
    )
    return fig


# ---------------------------------------------------------------
# 1. Linear motion
# ---------------------------------------------------------------
def linear_motion():
    st.header("ການເຄື່ອນທີ່ຊື່ (Linear Motion)")
    st.latex(r"v = v_0 + at,\qquad x = x_0 + v_0 t + \tfrac12 a t^2,\qquad v^2 = v_0^2 + 2a\,\Delta x")

    presets = {
        "ກຳນົດເອງ": (0.0, 5.0, 1.0),
        "ຕົກອິດສະຫຼະ ຈາກຄວາມສູງ 50 m": (50.0, 0.0, -9.81),
        "ຖິ້ມວັດຖຸຂຶ້ນຕັ້ງ 20 m/s": (0.0, 20.0, -9.81),
        "ລົດເບກ (v₀ = 20 m/s)": (0.0, 20.0, -4.0),
    }
    c1, c2 = st.columns([1, 3])
    with c1:
        preset = st.selectbox("ສະຖານະການ", list(presets.keys()))
        dx0, dv0, da = presets[preset]
        x0 = st.slider("ຕຳແໜ່ງເລີ່ມຕົ້ນ x₀ (m)", -100.0, 100.0, dx0, 1.0, key=f"lm_x0_{preset}")
        v0 = st.slider("ຄວາມໄວຕົ້ນ v₀ (m/s)", -50.0, 50.0, dv0, 0.5, key=f"lm_v0_{preset}")
        a = st.slider("ຄວາມເລັ່ງ a (m/s²)", -15.0, 15.0, da, 0.1, key=f"lm_a_{preset}")
        t_max = st.slider("ເວລາສະແດງ (s)", 1.0, 20.0, 8.0, 0.5)
        t_now = st.slider("ເວລາປັດຈຸບັນ t (s)", 0.0, t_max, 0.0, 0.05)

    t = np.linspace(0, t_max, 400)
    x = x0 + v0 * t + 0.5 * a * t**2
    v = v0 + a * t
    acc = np.full_like(t, a)
    xn = x0 + v0 * t_now + 0.5 * a * t_now**2
    vn = v0 + a * t_now
    tt = np.linspace(0, t_now, 1000)
    xx = x0 + v0 * tt + 0.5 * a * tt**2
    dist = float(np.sum(np.abs(np.diff(xx)))) if t_now > 0 else 0.0
    disp = xn - x0

    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.07,
                        subplot_titles=("ຕຳແໜ່ງ x (m)", "ຄວາມໄວ v (m/s)", "ຄວາມເລັ່ງ a (m/s²)"))
    for r, (yy, yn, col) in enumerate([(x, xn, "#1f77b4"), (v, vn, "#2ca02c"), (acc, a, "#d62728")], 1):
        fig.add_trace(go.Scatter(x=t, y=yy, mode="lines", line=dict(width=3, color=col),
                                 showlegend=False), row=r, col=1)
        fig.add_trace(go.Scatter(x=[t_now], y=[yn], mode="markers",
                                 marker=dict(size=12, color="black"), showlegend=False), row=r, col=1)
    fig.update_xaxes(title_text="ເວລາ t (s)", row=3, col=1)
    fig.update_layout(height=620, margin=dict(l=20, r=20, t=50, b=20))

    pad = max(5.0, 0.1 * (x.max() - x.min()))
    strip = go.Figure()
    strip.add_trace(go.Scatter(x=x, y=np.zeros_like(x), mode="lines", line=dict(color="lightgray", width=6),
                               showlegend=False))
    strip.add_trace(go.Scatter(x=[x0], y=[0], mode="markers", marker=dict(size=12, color="gray"),
                               name="ຈຸດເລີ່ມຕົ້ນ"))
    strip.add_trace(go.Scatter(x=[xn], y=[0], mode="markers", marker=dict(size=22, color="red"),
                               name="ຕຳແໜ່ງປັດຈຸບັນ"))
    strip.update_xaxes(range=[x.min() - pad, x.max() + pad])
    strip.update_yaxes(visible=False, range=[-1, 1])
    style(strip, "ຕຳແໜ່ງ x (m)", "", "ຕຳແໜ່ງຂອງວັດຖຸ", height=200)

    with c2:
        st.plotly_chart(fig, use_container_width=True)
        st.plotly_chart(strip, use_container_width=True)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("ຕຳແໜ່ງ x(t)", f"{xn:.2f} m")
    m2.metric("ຄວາມໄວ v(t)", f"{vn:.2f} m/s")
    m3.metric("ການຍ້າຍທີ່ Δx", f"{disp:.2f} m")
    m4.metric("ໄລຍະທາງທີ່ແລ່ນ", f"{dist:.2f} m")
    st.info("💡 ຄຳຖາມໃຫ້ນັກສຶກສາ: ເລືອກ \"ຖິ້ມວັດຖຸຂຶ້ນຕັ້ງ\" — ເວລາໃດທີ່ v = 0? ເປັນຫຍັງການຍ້າຍທີ່ ແລະ ໄລຍະທາງທີ່ແລ່ນຈຶ່ງຕ່າງກັນເມື່ອວັດຖຸຕົກກັບລົງມາ?")


# ---------------------------------------------------------------
# 2. Force (Newton's second law with friction)
# ---------------------------------------------------------------
def force_lesson():
    st.header("ແຮງ ແລະ ກົດຂອງນິວຕັນ (Force & Newton's Laws)")
    st.latex(r"\sum F = ma,\qquad f_s \le \mu_s N,\qquad f_k = \mu_k N")

    c1, c2 = st.columns([1, 3])
    with c1:
        m = st.slider("ມວນ m (kg)", 0.5, 50.0, 10.0, 0.5)
        F = st.slider("ແຮງດຶງ F (N)", 0.0, 200.0, 60.0, 1.0)
        mu_s = st.slider("ສຳປະສິດສຽດທານສະຖິດ μₛ", 0.0, 1.0, 0.5, 0.05)
        mu_k = st.slider("ສຳປະສິດສຽດທານຈລະສາດ μₖ", 0.0, 1.0, 0.3, 0.05)
        t_max = st.slider("ເວລາສະແດງ (s)", 1.0, 20.0, 8.0, 0.5)
    g = 9.81

    if mu_k > mu_s:
        st.warning("ປົກກະຕິ μₖ ≤ μₛ — ກະລຸນາກວດຄ່າທີ່ຕັ້ງ")

    def accel(mass, force):
        n = mass * g
        if force <= mu_s * n:
            return 0.0, force
        fr = mu_k * n
        return (force - fr) / mass, fr

    a, f = accel(m, F)
    N = m * g
    F_net = F - f
    t = np.linspace(0, t_max, 300)

    with c2:
        tab1, tab2, tab3 = st.tabs(["ການເຄື່ອນທີ່", "ແຮງທີ່ກະທຳ", "a ທຽບ F"])
        with tab1:
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                                subplot_titles=("ຕຳແໜ່ງ x (m)", "ຄວາມໄວ v (m/s)"))
            fig.add_trace(go.Scatter(x=t, y=0.5 * a * t**2, mode="lines", line=dict(width=3),
                                     showlegend=False), row=1, col=1)
            fig.add_trace(go.Scatter(x=t, y=a * t, mode="lines", line=dict(width=3, color="#2ca02c"),
                                     showlegend=False), row=2, col=1)
            fig.update_xaxes(title_text="ເວລາ t (s)", row=2, col=1)
            fig.update_layout(height=480, margin=dict(l=20, r=20, t=50, b=20))
            st.plotly_chart(fig, use_container_width=True)
            if a == 0:
                st.success("ແຮງດຶງ ≤ ແຮງສຽດທານສະຖິດສູງສຸດ → ວັດຖຸຢູ່ນິ່ງ (ຕາມກົດຂໍ້ 1)")
        with tab2:
            fig2 = go.Figure(go.Bar(x=["ແຮງດຶງ F", "ແຮງສຽດທານ f", "ແຮງລັບ ΣF"], y=[F, f, F_net],
                                    marker_color=["#1f77b4", "#d62728", "#2ca02c"]))
            st.plotly_chart(style(fig2, "", "ແຮງ (N)", "ແຮງໃນແນວນອນ"), use_container_width=True)
        with tab3:
            Fs = np.linspace(0, 200, 400)
            fig3 = go.Figure()
            for mm, dash in ((m / 2, "dot"), (m, "solid"), (m * 2, "dash")):
                aa = np.array([accel(mm, ff)[0] for ff in Fs])
                fig3.add_trace(go.Scatter(x=Fs, y=aa, mode="lines", name=f"m = {mm:.1f} kg",
                                          line=dict(dash=dash, width=3 if dash == "solid" else 2)))
            fig3.add_trace(go.Scatter(x=[F], y=[a], mode="markers", name="ຄ່າປັດຈຸບັນ",
                                      marker=dict(size=14, color="red")))
            st.plotly_chart(style(fig3, "ແຮງດຶງ F (N)", "ຄວາມເລັ່ງ a (m/s²)", "a ທຽບ F ສຳລັບມວນຕ່າງໆ"),
                            use_container_width=True)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("ນ້ຳໜັກ W = mg", f"{N:.1f} N")
    m2.metric("ແຮງສຽດທານ f", f"{f:.1f} N")
    m3.metric("ແຮງລັບ ΣF", f"{F_net:.1f} N")
    m4.metric("ຄວາມເລັ່ງ a", f"{a:.2f} m/s²")
    st.info("💡 ຄຳຖາມໃຫ້ນັກສຶກສາ: ເປັນຫຍັງເສັ້ນກຣາຟ a–F ຈຶ່ງບໍ່ເລີ່ມຈາກສູນ? ຖ້າເພີ່ມມວນເປັນ 2 ເທົ່າ ຄວາມຊັນເສັ້ນກຣາຟປ່ຽນແນວໃດ?")


# ---------------------------------------------------------------
# 3. Work
# ---------------------------------------------------------------
def work_lesson():
    st.header("ງານ ແລະ ກຳລັງ (Work & Power)")
    st.latex(r"W = Fd\cos\theta,\qquad W=\int F\,dx,\qquad P = \frac{W}{t}")

    tab_a, tab_b = st.tabs(["ງານຈາກແຮງຄົງທີ່", "ງານຂອງສະປຣິງ"])

    with tab_a:
        c1, c2 = st.columns([1, 3])
        with c1:
            F = st.slider("ແຮງ F (N)", 0.0, 100.0, 50.0, 1.0, key="w_F")
            d = st.slider("ການຍ້າຍທີ່ d (m)", 0.5, 20.0, 5.0, 0.5, key="w_d")
            theta = st.slider("ມຸມລະຫວ່າງແຮງ ແລະ ການຍ້າຍທີ່ θ (ອົງສາ)", 0, 180, 30, key="w_th")
            t_s = st.slider("ເວລາທີ່ໃຊ້ t (s)", 1.0, 60.0, 5.0, 1.0, key="w_t")
        th = np.radians(theta)
        W = F * d * np.cos(th)
        Fx, Fy = F * np.cos(th), F * np.sin(th)

        with c2:
            sub1, sub2 = st.tabs(["ແຜນວາດ", "W ທຽບ θ"])
            with sub1:
                LF = 0.2 * d + 0.5 * d * F / 100
                fig = go.Figure()
                fig.add_shape(type="rect", x0=-0.05 * d, x1=0.05 * d, y0=-0.04 * d, y1=0.04 * d,
                              fillcolor="gray", line=dict(color="black"))
                fig.add_annotation(x=d, y=0, ax=0, ay=0, xref="x", yref="y", axref="x", ayref="y",
                                   showarrow=True, arrowhead=3, arrowwidth=3, arrowcolor="black",
                                   text="ການຍ້າຍທີ່ d", font=dict(color="black"), yshift=-18)
                fig.add_annotation(x=LF * np.cos(th), y=LF * np.sin(th), ax=0, ay=0, xref="x", yref="y",
                                   axref="x", ayref="y", showarrow=True, arrowhead=3, arrowwidth=4,
                                   arrowcolor="#d62728", text="F", font=dict(color="#d62728", size=16))
                fig.add_annotation(x=LF * np.cos(th), y=0, ax=0, ay=0, xref="x", yref="y", axref="x",
                                   ayref="y", showarrow=True, arrowhead=2, arrowwidth=2, arrowcolor="#1f77b4",
                                   text="Fcosθ", font=dict(color="#1f77b4"), yshift=14)
                xlo = min(-0.2 * d, LF * np.cos(th) - 0.2 * d)
                xhi = max(1.15 * d, LF * np.cos(th) + 0.2 * d)
                yr = max(LF, 0.3 * d) * 1.3
                fig.update_xaxes(range=[xlo, xhi])
                fig.update_yaxes(range=[-yr * 0.5, yr], scaleanchor="x", scaleratio=1)
                st.plotly_chart(style(fig, "x (m)", "y (m)", "ແຮງ ແລະ ການຍ້າຍທີ່"), use_container_width=True)
            with sub2:
                ang = np.linspace(0, 180, 361)
                Wc = F * d * np.cos(np.radians(ang))
                fig2 = go.Figure()
                fig2.add_trace(go.Scatter(x=ang, y=Wc, mode="lines", line=dict(width=3), name="W(θ)"))
                fig2.add_trace(go.Scatter(x=[theta], y=[W], mode="markers", name="ຄ່າປັດຈຸບັນ",
                                          marker=dict(size=14, color="red")))
                fig2.add_hline(y=0, line_color="gray")
                st.plotly_chart(style(fig2, "ມຸມ θ (ອົງສາ)", "ງານ W (J)", "ງານ ທຽບ ມຸມ"),
                                use_container_width=True)

        m1, m2, m3 = st.columns(3)
        m1.metric("ງານ W", f"{W:.1f} J")
        m2.metric("ອົງປະກອບ Fₓ", f"{Fx:.1f} N")
        m3.metric("ກຳລັງສະເລ່ຍ P = W/t", f"{W / t_s:.1f} W")
        if theta == 90:
            st.warning("θ = 90°: ແຮງຕັ້ງສາກກັບການຍ້າຍທີ່ → ງານ = 0")
        elif theta > 90:
            st.warning("θ > 90°: ແຮງຕ້ານການເຄື່ອນທີ່ → ງານເປັນລົບ")
        st.info("💡 ຄຳຖາມໃຫ້ນັກສຶກສາ: ມຸມໃດທີ່ງານເປັນສູງສຸດ? ຕົວຢ່າງໃດໃນຊີວິດຈິງທີ່ງານເປັນລົບ?")

    with tab_b:
        c1, c2 = st.columns([1, 3])
        with c1:
            k = st.slider("ຄ່າຄົງທີ່ສະປຣິງ k (N/m)", 10.0, 500.0, 100.0, 10.0, key="ws_k")
            xmax = st.slider("ການຍືດສູງສຸດ (m)", 0.1, 2.0, 0.5, 0.1, key="ws_xmax")
            xc = st.slider("ຍືດເຖິງ x (m)", 0.0, xmax, xmax / 2, 0.01, key=f"ws_xc_{xmax}")
        xs = np.linspace(0, xmax, 200)
        xf = np.linspace(0, xc, 100)
        with c2:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=xs, y=k * xs, mode="lines", name="F = kx", line=dict(width=3)))
            fig.add_trace(go.Scatter(x=xf, y=k * xf, mode="lines", fill="tozeroy", name="ງານ (ເນື້ອທີ່)",
                                     line=dict(width=0), fillcolor="rgba(214,39,40,0.35)"))
            st.plotly_chart(style(fig, "ການຍືດ x (m)", "ແຮງ F (N)", "ແຮງສະປຣິງ — ເນື້ອທີ່ໃຕ້ເສັ້ນ = ງານ"),
                            use_container_width=True)
        m1, m2 = st.columns(2)
        m1.metric("ແຮງທີ່ x", f"{k * xc:.2f} N")
        m2.metric("ງານ W = ½kx²", f"{0.5 * k * xc**2:.3f} J")
        st.info("💡 ຄຳຖາມໃຫ້ນັກສຶກສາ: ຖ້າຍືດເພີ່ມເປັນ 2 ເທົ່າ ງານປ່ຽນເປັນຈັກເທົ່າ? ເປັນຫຍັງ?")


# ---------------------------------------------------------------
# 4. Energy (pendulum)
# ---------------------------------------------------------------
def energy_lesson():
    st.header("ພະລັງງານກົນ ແລະ ການສະຫງວນພະລັງງານ (Mechanical Energy)")
    st.latex(r"E = KE + PE = \tfrac12 mv^2 + mgh = \text{ຄົງທີ່}")

    c1, c2 = st.columns([1, 3])
    with c1:
        m = st.slider("ມວນ m (kg)", 0.1, 5.0, 1.0, 0.1, key="e_m")
        L = st.slider("ຄວາມຍາວເຊືອກ L (m)", 0.5, 3.0, 1.5, 0.1, key="e_L")
        th0 = st.slider("ມຸມປ່ອຍ θ₀ (ອົງສາ)", 5, 90, 60, key="e_th0")
        cur = st.slider("ມຸມປັດຈຸບັນ θ (ອົງສາ)", -float(th0), float(th0), float(th0), 1.0,
                        key=f"e_cur_{th0}")
    g = 9.81

    E = m * g * L * (1 - np.cos(np.radians(th0)))
    th = np.radians(cur)
    h = L * (1 - np.cos(th))
    PE = m * g * h
    KE = max(E - PE, 0.0)
    vel = np.sqrt(2 * KE / m)

    with c2:
        tab1, tab2, tab3 = st.tabs(["ຕົວແກວ່ງ", "ພະລັງງານ ທຽບ ມຸມ", "ແຖບພະລັງງານ"])
        with tab1:
            ph = np.radians(np.linspace(-th0, th0, 100))
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=L * np.sin(ph), y=-L * np.cos(ph), mode="lines",
                                     line=dict(color="lightgray", dash="dot"), showlegend=False))
            fig.add_trace(go.Scatter(x=[0, L * np.sin(th)], y=[0, -L * np.cos(th)], mode="lines",
                                     line=dict(color="black", width=3), showlegend=False))
            fig.add_trace(go.Scatter(x=[L * np.sin(th)], y=[-L * np.cos(th)], mode="markers",
                                     marker=dict(size=10 + 6 * m, color="#d62728"), showlegend=False))
            fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers", marker=dict(size=8, color="black"),
                                     showlegend=False))
            fig.update_yaxes(scaleanchor="x", scaleratio=1, range=[-L * 1.15, 0.1 * L])
            fig.update_xaxes(range=[-L * 1.1, L * 1.1])
            st.plotly_chart(style(fig, "x (m)", "y (m)", "ຕົວແກວ່ງແບບລູກຕຸ້ມ"), use_container_width=True)
        with tab2:
            angs = np.linspace(-th0, th0, 300)
            pe_c = m * g * L * (1 - np.cos(np.radians(angs)))
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=angs, y=pe_c, name="PE", line=dict(width=3)))
            fig2.add_trace(go.Scatter(x=angs, y=np.maximum(E - pe_c, 0), name="KE", line=dict(width=3)))
            fig2.add_trace(go.Scatter(x=angs, y=np.full_like(angs, E), name="E ລວມ",
                                      line=dict(width=2, dash="dash", color="black")))
            fig2.add_trace(go.Scatter(x=[cur, cur], y=[PE, KE], mode="markers", showlegend=False,
                                      marker=dict(size=12, color="red")))
            st.plotly_chart(style(fig2, "ມຸມ θ (ອົງສາ)", "ພະລັງງານ (J)", "KE, PE ແລະ E ລວມ"),
                            use_container_width=True)
        with tab3:
            fig3 = go.Figure(go.Bar(x=["ພະລັງງານຈົນ KE", "ພະລັງງານສັກ PE", "ລວມ E"], y=[KE, PE, KE + PE],
                                    marker_color=["#2ca02c", "#1f77b4", "#7f7f7f"]))
            fig3.update_yaxes(range=[0, max(E * 1.1, 0.1)])
            st.plotly_chart(style(fig3, "", "ພະລັງງານ (J)", "ພະລັງງານທີ່ມຸມປັດຈຸບັນ"), use_container_width=True)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("ຄວາມສູງ h", f"{h:.3f} m")
    m2.metric("ຄວາມໄວ v", f"{vel:.2f} m/s")
    m3.metric("KE / PE", f"{KE:.2f} / {PE:.2f} J")
    m4.metric("E ລວມ", f"{E:.2f} J")
    st.info("💡 ຄຳຖາມໃຫ້ນັກສຶກສາ: ທີ່ຈຸດໃດ KE ສູງສຸດ? ຖ້າເພີ່ມມວນ m ຄວາມໄວທີ່ຈຸດຕ່ຳສຸດປ່ຽນບໍ? ເປັນຫຍັງ?")


# ---------------------------------------------------------------
# 5. Light (refraction + thin lens)
# ---------------------------------------------------------------
MEDIA = {
    "ອາກາດ (n = 1.00)": 1.00,
    "ນ້ຳ (n = 1.33)": 1.33,
    "ແກ້ວ (n = 1.52)": 1.52,
    "ເພັດ (n = 2.42)": 2.42,
    "ກຳນົດເອງ": None,
}


def _pick_medium(label, default_idx, key):
    names = list(MEDIA.keys())
    choice = st.selectbox(label, names, index=default_idx, key=key)
    n = MEDIA[choice]
    if n is None:
        n = st.number_input("ດັດຊະນີຫັກເຫ n", 1.0, 3.0, 1.5, 0.01, key=key + "_n")
    return n


def _refraction_tab():
    c1, c2 = st.columns([1, 3])
    with c1:
        n1 = _pick_medium("ຕົວກາງ 1 (ດ້ານເທິງ)", 1, "l_m1")
        n2 = _pick_medium("ຕົວກາງ 2 (ດ້ານລຸ່ມ)", 0, "l_m2")
        th1 = st.slider("ມຸມຕົກກະທົບ θ₁ (ອົງສາ)", 0, 89, 30, key="l_th1")

    t1 = np.radians(th1)
    s2 = n1 * np.sin(t1) / n2
    tir = s2 > 1
    t2 = None if tir else np.arcsin(s2)
    crit = np.degrees(np.arcsin(n2 / n1)) if n1 > n2 else None

    fig = go.Figure()
    fig.add_shape(type="rect", x0=-1.2, x1=1.2, y0=0, y1=1.2, layer="below", line_width=0,
                  fillcolor=f"rgba(100,150,255,{min(0.08 + 0.1 * (n1 - 1), 0.6):.2f})")
    fig.add_shape(type="rect", x0=-1.2, x1=1.2, y0=-1.2, y1=0, layer="below", line_width=0,
                  fillcolor=f"rgba(100,150,255,{min(0.08 + 0.1 * (n2 - 1), 0.6):.2f})")
    fig.add_trace(go.Scatter(x=[0, 0], y=[-1.2, 1.2], mode="lines",
                             line=dict(color="gray", dash="dash"), showlegend=False))
    fig.add_trace(go.Scatter(x=[-1.2, 1.2], y=[0, 0], mode="lines", line=dict(color="black", width=2),
                             showlegend=False))

    def ray(x0, y0, x1, y1, color, text):
        fig.add_annotation(x=x1, y=y1, ax=x0, ay=y0, xref="x", yref="y", axref="x", ayref="y",
                           showarrow=True, arrowhead=3, arrowwidth=4, arrowcolor=color,
                           text=text, font=dict(color=color, size=13))

    ray(-np.sin(t1), np.cos(t1), 0, 0, "#d62728", "ແສງຕົກກະທົບ")
    ray(0, 0, np.sin(t1), np.cos(t1), "#ff7f0e", "ສະທ້ອນ")
    if not tir:
        ray(0, 0, np.sin(t2), -np.cos(t2), "#2ca02c", "ຫັກເຫ")
    fig.add_annotation(x=-1.1, y=1.1, text=f"n₁ = {n1:.2f}", showarrow=False)
    fig.add_annotation(x=-1.1, y=-1.1, text=f"n₂ = {n2:.2f}", showarrow=False)
    fig.update_xaxes(range=[-1.2, 1.2])
    fig.update_yaxes(range=[-1.2, 1.2], scaleanchor="x", scaleratio=1)
    style(fig, "", "", "ການສະທ້ອນ ແລະ ການຫັກເຫຂອງແສງ", height=520)
    fig.update_layout(showlegend=False)

    with c2:
        st.plotly_chart(fig, use_container_width=True)
        if tir:
            st.warning("ການສະທ້ອນພາຍໃນທັງໝົດ (Total Internal Reflection) — ບໍ່ມີແສງຫັກເຫເຂົ້າຕົວກາງ 2")
        elif crit is not None and abs(th1 - crit) < 1.0:
            st.info("ໃກ້ມຸມວິກິດ — ແສງຫັກເຫເກືອບຂະໜານກັບຜິວ")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("θ₁", f"{th1}°")
    m2.metric("θ₂", "—" if tir else f"{np.degrees(t2):.1f}°")
    m3.metric("ມຸມວິກິດ θc", "—" if crit is None else f"{crit:.1f}°")
    m4.metric("v₁ , v₂ (×10⁸ m/s)", f"{3.0 / n1:.2f} , {3.0 / n2:.2f}")
    st.info("💡 ຄຳຖາມໃຫ້ນັກສຶກສາ: ຕັ້ງ ນ້ຳ → ອາກາດ ແລ້ວເພີ່ມມຸມ θ₁ ເທື່ອລະໜ້ອຍ — ເກີດຫຍັງຂຶ້ນທີ່ປະມານ 48.8°? ເຫດການນີ້ນຳໃຊ້ໃນສາຍໄຟເບີແສງແນວໃດ?")


def _lens_tab():
    c1, c2 = st.columns([1, 3])
    with c1:
        kind = st.radio("ຊະນິດເລນ", ["ເລນນູນ (Convex)", "ເລນເວົ້າ (Concave)"], key="lens_kind")
        fabs = st.slider("ໄລຍະໂຟກັດ |f| (cm)", 5, 30, 10, key="lens_f")
        do = st.slider("ໄລຍະວັດຖຸ dₒ (cm)", 3, 60, 25, key="lens_do")
        ho = st.slider("ຄວາມສູງວັດຖຸ hₒ (cm)", 1, 10, 3, key="lens_ho")

    f = float(fabs) if kind.startswith("ເລນນູນ") else -float(fabs)
    if abs(do - f) < 1e-9:
        with c2:
            st.warning("ວັດຖຸຢູ່ທີ່ຈຸດໂຟກັດພໍດີ — ແສງຫັກເຫອອກຂະໜານກັນ ບໍ່ເກີດພາບ")
        return

    di = 1.0 / (1.0 / f - 1.0 / do)
    M = -di / do
    hi = M * ho

    X = min(1.3 * max(do, abs(di), 2 * fabs, 20), 200)
    Y = 1.8 * max(ho, abs(hi), 3)
    fig = go.Figure()
    fig.add_hline(y=0, line_color="gray")
    fig.add_shape(type="line", x0=0, x1=0, y0=-Y, y1=Y, line=dict(color="royalblue", width=5))
    fig.add_trace(go.Scatter(x=[-do, -do], y=[0, ho], mode="lines+markers", name="ວັດຖຸ",
                             line=dict(color="black", width=4), marker=dict(size=[1, 12])))
    fig.add_trace(go.Scatter(x=[-fabs, fabs], y=[0, 0], mode="markers+text", text=["F", "F'"],
                             textposition="top center", marker=dict(size=9, color="royalblue"),
                             showlegend=False))
    # ray 1: parallel to axis, then through focus (direction fixed by image point)
    slope1 = (hi - ho) / di
    fig.add_trace(go.Scatter(x=[-do, 0, X], y=[ho, ho, ho + slope1 * X], mode="lines", name="ລັງສີ 1",
                             line=dict(color="#d62728", width=2)))
    # ray 2: through the optical centre
    slope2 = -ho / do
    fig.add_trace(go.Scatter(x=[-do, X], y=[ho, slope2 * X], mode="lines", name="ລັງສີ 2",
                             line=dict(color="#2ca02c", width=2)))
    real = di > 0
    if not real:
        fig.add_trace(go.Scatter(x=[0, di], y=[ho, hi], mode="lines", showlegend=False,
                                 line=dict(color="#d62728", width=2, dash="dash")))
    fig.add_trace(go.Scatter(x=[di, di], y=[0, hi], mode="lines+markers", name="ພາບ",
                             line=dict(color="#9467bd", width=4, dash="solid" if real else "dot"),
                             marker=dict(size=[1, 12])))
    fig.update_xaxes(range=[-X, X])
    fig.update_yaxes(range=[-Y, Y])
    style(fig, "x (cm)", "y (cm)", "ແຜນວາດລັງສີຂອງເລນບາງ", height=520)

    with c2:
        st.plotly_chart(fig, use_container_width=True)
    m1, m2, m3 = st.columns(3)
    m1.metric("ໄລຍະພາບ dᵢ", f"{di:.1f} cm")
    m2.metric("ກຳລັງຂະຫຍາຍ M", f"{M:.2f}")
    desc = ("ພາບຈິງ, ກັບຫົວ" if real else "ພາບເສມືອນ, ຕັ້ງ") + (", ຂະຫຍາຍ" if abs(M) > 1 else ", ຍໍ່")
    m3.metric("ຊະນິດພາບ", desc)
    st.latex(r"\frac1f=\frac1{d_o}+\frac1{d_i},\qquad M=-\frac{d_i}{d_o}")
    st.info("💡 ຄຳຖາມໃຫ້ນັກສຶກສາ: ເລນນູນ — ເມື່ອ dₒ < f ພາບເປັນແນວໃດ (ເຄື່ອງຂະຫຍາຍ)? ເລນເວົ້າໃຫ້ພາບຊະນິດໃດສະເໝີ?")


def light_lesson():
    st.header("ແສງສະຫວ່າງ (Light & Optics)")
    st.latex(r"n_1\sin\theta_1 = n_2\sin\theta_2,\qquad n = \frac{c}{v},\qquad \sin\theta_c = \frac{n_2}{n_1}")
    tab1, tab2 = st.tabs(["ການສະທ້ອນ ແລະ ການຫັກເຫ", "ເລນບາງ"])
    with tab1:
        _refraction_tab()
    with tab2:
        _lens_tab()
