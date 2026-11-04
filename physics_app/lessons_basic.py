# ບົດຮຽນພື້ນຖານເພີ່ມເຕີມ (ໂປເຈັກໄທລ໌, ສະປຣິງ, ຄື້ນ, ພື້ນອຽງ, ການຊົນ, ສະໜາມໄຟຟ້າ, RC, ແກັສ)
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff
import streamlit as st



def style(fig, xt, yt, title):
    fig.update_layout(
        title=title,
        xaxis_title=xt,
        yaxis_title=yt,
        height=480,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", y=-0.2),
    )
    return fig


# ---------------------------------------------------------------
# 1. Projectile motion
# ---------------------------------------------------------------
def projectile():
    st.header("ການເຄື່ອນທີ່ແບບໂປເຈັກໄທລ໌ (Projectile Motion)")
    st.latex(r"x = v_0\cos\theta\, t,\qquad y = h_0 + v_0\sin\theta\, t - \tfrac12 g t^2")

    c1, c2 = st.columns([1, 3])
    with c1:
        v0 = st.slider("ຄວາມໄວຕົ້ນ v₀ (m/s)", 1.0, 100.0, 30.0, 1.0)
        theta = st.slider("ມຸມຍິງ θ (ອົງສາ)", 0, 90, 45)
        h0 = st.slider("ຄວາມສູງເລີ່ມຕົ້ນ h₀ (m)", 0.0, 100.0, 0.0, 1.0)
        planet = st.selectbox("ດາວ", ["ໂລກ (9.81)", "ດວງຈັນ (1.62)", "ດາວອັງຄານ (3.71)", "ກຳນົດເອງ"])
        g = {"ໂລກ (9.81)": 9.81, "ດວງຈັນ (1.62)": 1.62, "ດາວອັງຄານ (3.71)": 3.71}.get(planet)
        if g is None:
            g = st.number_input("g (m/s²)", 0.1, 30.0, 9.81)
        compare = st.checkbox("ປຽບທຽບກັບມຸມອື່ນ (15°, 30°, 45°, 60°, 75°)")

    def traj(v, ang_deg):
        a = np.radians(ang_deg)
        vy = v * np.sin(a)
        t_f = (vy + np.sqrt(vy**2 + 2 * g * h0)) / g
        t = np.linspace(0, t_f, 300)
        return v * np.cos(a) * t, h0 + vy * t - 0.5 * g * t**2, t_f

    x, y, t_f = traj(v0, theta)
    y_max = h0 + (v0 * np.sin(np.radians(theta))) ** 2 / (2 * g)
    rng = x[-1]

    fig = go.Figure()
    if compare:
        for a in (15, 30, 45, 60, 75):
            xa, ya, _ = traj(v0, a)
            fig.add_trace(go.Scatter(x=xa, y=ya, mode="lines", name=f"{a}°", line=dict(dash="dot")))
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name=f"θ = {theta}°", line=dict(width=4)))
    fig.update_yaxes(scaleanchor="x", scaleratio=1, rangemode="tozero")
    style(fig, "ໄລຍະທາງ x (m)", "ຄວາມສູງ y (m)", "ເສັ້ນທາງການເຄື່ອນທີ່")

    with c2:
        st.plotly_chart(fig, use_container_width=True)
        m1, m2, m3 = st.columns(3)
        m1.metric("ເວລາບິນ", f"{t_f:.2f} s")
        m2.metric("ຄວາມສູງສູງສຸດ", f"{y_max:.2f} m")
        m3.metric("ໄລຍະທາງໄກສຸດ", f"{rng:.2f} m")

    st.info("💡 ຄຳຖາມໃຫ້ນັກສຶກສາ: ເມື່ອ h₀ = 0, ມຸມໃດໃຫ້ໄລຍະທາງໄກສຸດ? ຖ້າ h₀ > 0 ມຸມນັ້ນປ່ຽນໄປແນວໃດ?")


# ---------------------------------------------------------------
# 2. Damped harmonic oscillator
# ---------------------------------------------------------------
def oscillator():
    st.header("ການສັ່ນແບບຮາໂມນິກຂອງສະປຣິງ (Damped Oscillator)")
    st.latex(r"m\ddot{x} + b\dot{x} + kx = 0")

    c1, c2 = st.columns([1, 3])
    with c1:
        m = st.slider("ມວນ m (kg)", 0.1, 10.0, 1.0, 0.1)
        k = st.slider("ຄ່າຄົງທີ່ສະປຣິງ k (N/m)", 1.0, 200.0, 50.0, 1.0)
        b = st.slider("ສຳປະສິດໜ່ວງ b (kg/s)", 0.0, 50.0, 1.0, 0.1)
        A = st.slider("ແອມພລິຈູດເລີ່ມຕົ້ນ A (m)", 0.1, 2.0, 1.0, 0.1)
        t_max = st.slider("ເວລາສະແດງ (s)", 2.0, 30.0, 10.0, 1.0)

    w0 = np.sqrt(k / m)
    gam = b / (2 * m)
    t = np.linspace(0, t_max, 1500)

    if abs(gam - w0) < 1e-6:
        kind = "ໜ່ວງວິກິດ (Critically damped)"
        x = A * (1 + gam * t) * np.exp(-gam * t)
    elif gam < w0:
        wd = np.sqrt(w0**2 - gam**2)
        kind = "ໜ່ວງນ້ອຍ (Underdamped)" if gam > 0 else "ບໍ່ມີການໜ່ວງ (Undamped)"
        x = A * np.exp(-gam * t) * (np.cos(wd * t) + gam / wd * np.sin(wd * t))
    else:
        kind = "ໜ່ວງຫຼາຍ (Overdamped)"
        s = np.sqrt(gam**2 - w0**2)
        r1, r2 = -gam + s, -gam - s
        x = A * (r2 * np.exp(r1 * t) - r1 * np.exp(r2 * t)) / (r2 - r1)

    v = np.gradient(x, t)
    energy = 0.5 * m * v**2 + 0.5 * k * x**2

    with c2:
        fig = go.Figure(go.Scatter(x=t, y=x, mode="lines", line=dict(width=3), name="x(t)"))
        if 0 < gam < w0:
            env = A * np.exp(-gam * t)
            fig.add_trace(go.Scatter(x=t, y=env, mode="lines", line=dict(dash="dash"), name="ເອັນເວໂລບ"))
            fig.add_trace(go.Scatter(x=t, y=-env, mode="lines", line=dict(dash="dash"), showlegend=False))
        style(fig, "ເວລາ t (s)", "ຕຳແໜ່ງ x (m)", f"ປະເພດ: {kind}")
        st.plotly_chart(fig, use_container_width=True)

        tab1, tab2 = st.tabs(["ພະລັງງານ", "Phase portrait"])
        with tab1:
            f2 = go.Figure(go.Scatter(x=t, y=energy, mode="lines", name="E"))
            st.plotly_chart(style(f2, "t (s)", "E (J)", "ພະລັງງານລວມ"), use_container_width=True)
        with tab2:
            f3 = go.Figure(go.Scatter(x=x, y=v, mode="lines"))
            st.plotly_chart(style(f3, "x (m)", "v (m/s)", "x ທຽບ v"), use_container_width=True)

    m1, m2, m3 = st.columns(3)
    m1.metric("ຄວາມຖີ່ທຳມະຊາດ ω₀", f"{w0:.2f} rad/s")
    m2.metric("ຄາບ T₀ = 2π/ω₀", f"{2 * np.pi / w0:.2f} s")
    m3.metric("ປະເພດ", kind.split(" ")[0] + " " + kind.split(" ")[1] if " " in kind else kind)


# ---------------------------------------------------------------
# 3. Wave superposition
# ---------------------------------------------------------------
def waves():
    st.header("ການແທກສອດຂອງຄື້ນ (Wave Superposition)")
    st.latex(r"y = A_1\sin(k_1x-\omega_1t) + A_2\sin(k_2x-\omega_2t+\varphi)")

    c1, c2 = st.columns([1, 3])
    with c1:
        st.subheader("ຄື້ນທີ 1")
        A1 = st.slider("A₁", 0.0, 2.0, 1.0, 0.1)
        f1 = st.slider("f₁ (Hz)", 0.5, 10.0, 2.0, 0.1)
        st.subheader("ຄື້ນທີ 2")
        A2 = st.slider("A₂", 0.0, 2.0, 1.0, 0.1)
        f2 = st.slider("f₂ (Hz)", 0.5, 10.0, 2.0, 0.1)
        phi = st.slider("ຜົນຕ່າງເຟສ φ (ອົງສາ)", 0, 360, 0)
        v = 2.0
        t0 = st.slider("ເວລາ t (s)", 0.0, 5.0, 0.0, 0.05)

    x = np.linspace(0, 6, 1500)
    k1, k2 = 2 * np.pi * f1 / v, 2 * np.pi * f2 / v
    w1, w2 = 2 * np.pi * f1, 2 * np.pi * f2
    y1 = A1 * np.sin(k1 * x - w1 * t0)
    y2 = A2 * np.sin(k2 * x - w2 * t0 + np.radians(phi))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y1, name="ຄື້ນ 1", line=dict(dash="dot")))
    fig.add_trace(go.Scatter(x=x, y=y2, name="ຄື້ນ 2", line=dict(dash="dot")))
    fig.add_trace(go.Scatter(x=x, y=y1 + y2, name="ຜົນລວມ", line=dict(width=4)))
    fig.update_yaxes(range=[-4.2, 4.2])
    style(fig, "ຕຳແໜ່ງ x (m)", "y", "ຄື້ນ ແລະ ຜົນລວມ")

    with c2:
        st.plotly_chart(fig, use_container_width=True)
        if abs(f1 - f2) < 1e-9:
            if phi in (0, 360):
                st.success("ການແທກສອດແບບເສີມ (Constructive)")
            elif phi == 180:
                st.warning("ການແທກສອດແບບທຳລາຍ (Destructive)")
        else:
            st.info(f"ຄວາມຖີ່ບີດ (beat frequency) = |f₁ − f₂| = {abs(f1 - f2):.2f} Hz")


# ---------------------------------------------------------------
# 4. Inclined plane with friction (Newton's laws)
# ---------------------------------------------------------------
def incline():
    st.header("ພື້ນອຽງ ແລະ ແຮງສຽດທານ (Inclined Plane & Friction)")
    st.latex(r"a = g(\sin\theta - \mu_k\cos\theta),\qquad \theta_c = \arctan\mu_s")

    c1, c2 = st.columns([1, 3])
    with c1:
        m = st.slider("ມວນ m (kg)", 0.1, 20.0, 5.0, 0.1)
        theta = st.slider("ມຸມອຽງ θ (ອົງສາ)", 0, 90, 30)
        mu_s = st.slider("ສຳປະສິດສຽດທານສະຖິດ μₛ", 0.0, 1.5, 0.5, 0.05)
        mu_k = st.slider("ສຳປະສິດສຽດທານຈລະສາດ μₖ", 0.0, 1.5, 0.3, 0.05)
        L = st.slider("ຄວາມຍາວພື້ນອຽງ L (m)", 0.5, 10.0, 3.0, 0.5)
    g = 9.81

    if mu_k > mu_s:
        st.warning("ປົກກະຕິ μₖ ≤ μₛ — ກະລຸນາກວດຄ່າທີ່ຕັ້ງ")

    th = np.radians(theta)
    w_par = m * g * np.sin(th)
    N = m * g * np.cos(th)
    slides = w_par > mu_s * N
    if slides:
        f = mu_k * N
        a = (w_par - f) / m
    else:
        f = w_par
        a = 0.0
    theta_c = np.degrees(np.arctan(mu_s))

    with c2:
        tab1, tab2, tab3 = st.tabs(["ແຜນວາດແຮງ", "ຄວາມເລັ່ງ ທຽບ ມຸມ", "ການເຄື່ອນທີ່"])

        with tab1:
            Lx, Ly = 4 * np.cos(th), 4 * np.sin(th)
            u = np.array([np.cos(th), np.sin(th)])
            n = np.array([-np.sin(th), np.cos(th)])
            P = 2 * u + 0.15 * n
            sc = 1.5 / (m * g)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=[0, Lx, Lx, 0], y=[0, 0, Ly, 0], fill="toself",
                                     mode="lines", line=dict(color="gray"), showlegend=False))
            fig.add_trace(go.Scatter(x=[P[0]], y=[P[1]], mode="markers",
                                     marker=dict(size=16, color="black"), showlegend=False))
            arrows = [
                (np.array([0.0, -m * g]), "W = mg", "royalblue"),
                (N * n, "N", "green"),
                (f * u, "f", "red"),
            ]
            for vec, label, col in arrows:
                end = P + sc * vec
                fig.add_annotation(x=end[0], y=end[1], ax=P[0], ay=P[1], xref="x", yref="y",
                                   axref="x", ayref="y", showarrow=True, arrowhead=3,
                                   arrowwidth=3, arrowcolor=col, text=label,
                                   font=dict(color=col, size=14))
            fig.update_yaxes(scaleanchor="x", scaleratio=1)
            style(fig, "x (m)", "y (m)", "ແຜນວາດແຮງທີ່ກະທຳຕໍ່ວັດຖຸ")
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            ang = np.linspace(0, 90, 361)
            ar = np.radians(ang)
            a_curve = np.where(np.tan(ar) > mu_s, g * (np.sin(ar) - mu_k * np.cos(ar)), 0.0)
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=ang, y=a_curve, mode="lines", name="a(θ)", line=dict(width=3)))
            fig2.add_trace(go.Scatter(x=[theta], y=[a], mode="markers", name="ຄ່າປັດຈຸບັນ",
                                      marker=dict(size=14, color="red")))
            fig2.add_vline(x=theta_c, line_dash="dash", annotation_text=f"θc = {theta_c:.1f}°")
            st.plotly_chart(style(fig2, "ມຸມ θ (ອົງສາ)", "ຄວາມເລັ່ງ a (m/s²)", "ຄວາມເລັ່ງຕາມມຸມອຽງ"),
                            use_container_width=True)

        with tab3:
            if slides:
                t_end = np.sqrt(2 * L / a)
                t = np.linspace(0, t_end, 200)
                fig3 = go.Figure()
                fig3.add_trace(go.Scatter(x=t, y=0.5 * a * t**2, name="ໄລຍະທາງ s (m)"))
                fig3.add_trace(go.Scatter(x=t, y=a * t, name="ຄວາມໄວ v (m/s)"))
                st.plotly_chart(style(fig3, "ເວລາ t (s)", "s, v", "ວັດຖຸໄຫຼລົງຕາມພື້ນອຽງ"),
                                use_container_width=True)
                st.write(f"ເວລາໄຫຼລົງຮອດພື້ນ = **{t_end:.2f} s**, ຄວາມໄວຕອນລຸ່ມ = **{a * t_end:.2f} m/s**")
            else:
                st.success("ວັດຖຸຢູ່ນິ່ງ (ແຮງສຽດທານສະຖິດພຽງພໍ) — ບໍ່ມີການເຄື່ອນທີ່")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("ແຮງປົກກະຕິ N", f"{N:.2f} N")
    m2.metric("ແຮງສຽດທານ f", f"{f:.2f} N")
    m3.metric("ຄວາມເລັ່ງ a", f"{a:.2f} m/s²")
    m4.metric("ສະຖານະ", "ໄຫຼລົງ" if slides else "ນິ່ງ")
    st.info("💡 ຄຳຖາມໃຫ້ນັກສຶກສາ: ມຸມວິກິດ θc ຂຶ້ນກັບມວນ m ຫຼືບໍ່? ເປັນຫຍັງ?")


# ---------------------------------------------------------------
# 5. 1D Collisions (momentum & energy)
# ---------------------------------------------------------------
def collision():
    st.header("ການຊົນກັນ 1 ມິຕິ (Collisions & Momentum)")
    st.latex(r"m_1v_1+m_2v_2=m_1v_1'+m_2v_2',\qquad e=-\frac{v_1'-v_2'}{v_1-v_2}")

    c1, c2 = st.columns([1, 3])
    with c1:
        m1 = st.slider("ມວນ m₁ (kg)", 0.1, 10.0, 2.0, 0.1)
        v1 = st.slider("ຄວາມໄວ v₁ (m/s)", -10.0, 10.0, 5.0, 0.5)
        m2 = st.slider("ມວນ m₂ (kg)", 0.1, 10.0, 1.0, 0.1)
        v2 = st.slider("ຄວາມໄວ v₂ (m/s)", -10.0, 10.0, -2.0, 0.5)
        e = st.slider("ສຳປະສິດການດີດກັບ e (0 = ຕິດກັນ, 1 = ຍືດຫຍຸ່ນ)", 0.0, 1.0, 1.0, 0.05)

    M = m1 + m2
    approaching = v1 > v2
    if approaching:
        u1 = ((m1 - e * m2) * v1 + (1 + e) * m2 * v2) / M
        u2 = ((m2 - e * m1) * v2 + (1 + e) * m1 * v1) / M
    else:
        u1, u2 = v1, v2

    p0, p1 = m1 * v1 + m2 * v2, m1 * u1 + m2 * u2
    k0 = 0.5 * m1 * v1**2 + 0.5 * m2 * v2**2
    k1 = 0.5 * m1 * u1**2 + 0.5 * m2 * u2**2

    with c2:
        if not approaching:
            st.warning("ວັດຖຸ 1 (ຢູ່ຊ້າຍ) ຕ້ອງໄວກວ່າວັດຖຸ 2 (v₁ > v₂) ຈຶ່ງຈະຊົນກັນ")
        T = 3.0
        tab1, tab2 = st.tabs(["ຕຳແໜ່ງ ທຽບ ເວລາ", "ພະລັງງານຈົນ"])
        with tab1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=[-T, 0, T], y=[-v1 * T, 0, u1 * T], mode="lines",
                                     name="ວັດຖຸ 1", line=dict(width=4, color="#1f77b4")))
            fig.add_trace(go.Scatter(x=[-T, 0, T], y=[-v2 * T, 0, u2 * T], mode="lines",
                                     name="ວັດຖຸ 2", line=dict(width=4, color="#d62728")))
            fig.add_vline(x=0, line_dash="dash", annotation_text="ຈຸດຊົນ")
            st.plotly_chart(style(fig, "ເວລາ t (s)  (0 = ເວລາຊົນ)", "ຕຳແໜ່ງ x (m)", "ກຣາຟ x–t"),
                            use_container_width=True)
        with tab2:
            fig2 = go.Figure(go.Bar(x=["ກ່ອນຊົນ", "ຫຼັງຊົນ"], y=[k0, k1],
                                    marker_color=["#2ca02c", "#ff7f0e"]))
            st.plotly_chart(style(fig2, "", "ພະລັງງານຈົນ (J)", "ພະລັງງານຈົນກ່ອນ ແລະ ຫຼັງຊົນ"),
                            use_container_width=True)

    m_a, m_b, m_c, m_d = st.columns(4)
    m_a.metric("v₁' ຫຼັງຊົນ", f"{u1:.2f} m/s")
    m_b.metric("v₂' ຫຼັງຊົນ", f"{u2:.2f} m/s")
    m_c.metric("ໂມເມັນຕຳລວມ ກ່ອນ → ຫຼັງ", f"{p0:.2f} → {p1:.2f}")
    m_d.metric("ພະລັງງານທີ່ສູນເສຍ", f"{k0 - k1:.2f} J")
    st.info("💡 ຄຳຖາມໃຫ້ນັກສຶກສາ: ເມື່ອ e = 1 ພະລັງງານຈົນຄົງທີ່ບໍ? ເມື່ອ e = 0 ພະລັງງານສູນເສຍໄປໃສ?")


# ---------------------------------------------------------------
# 6. Electric field and potential of two point charges
# ---------------------------------------------------------------
def efield():
    st.header("ສະໜາມໄຟຟ້າ ແລະ ສັກຂະໄຟຟ້າ (Electric Field & Potential)")
    st.latex(r"\vec{E}=\sum_i k\frac{q_i}{r_i^2}\hat r_i,\qquad V=\sum_i k\frac{q_i}{r_i}")

    c1, c2 = st.columns([1, 3])
    with c1:
        q1 = st.slider("ຄ່າປະຈຸ q₁ (ໜ່ວຍສົມທຽບ)", -5.0, 5.0, 2.0, 0.5)
        q2 = st.slider("ຄ່າປະຈຸ q₂ (ໜ່ວຍສົມທຽບ)", -5.0, 5.0, -2.0, 0.5)
        d = st.slider("ໄລຍະຫ່າງລະຫວ່າງປະຈຸ d", 0.5, 5.0, 2.0, 0.1)
        dens = st.slider("ຄວາມໜາແໜ້ນເສັ້ນສະໜາມ", 0.5, 3.0, 1.5, 0.1)
        st.subheader("ຈຸດທົດສອບ")
        px = st.slider("x ຂອງຈຸດ", -4.0, 4.0, 0.0, 0.1)
        py = st.slider("y ຂອງຈຸດ", -3.0, 3.0, 1.0, 0.1)

    k = 1.0
    eps = 0.15
    charges = [(-d / 2, 0.0, q1), (d / 2, 0.0, q2)]

    def field(X, Y):
        Ex = np.zeros_like(X)
        Ey = np.zeros_like(X)
        V = np.zeros_like(X)
        for cx, cy, q in charges:
            dx, dy = X - cx, Y - cy
            r = np.sqrt(dx**2 + dy**2 + eps**2)
            Ex += k * q * dx / r**3
            Ey += k * q * dy / r**3
            V += k * q / r
        return Ex, Ey, V

    xs = np.linspace(-4, 4, 81)
    ys = np.linspace(-3, 3, 61)
    X, Y = np.meshgrid(xs, ys)
    Ex, Ey, V = field(X, Y)
    mag = np.sqrt(Ex**2 + Ey**2) + 1e-12
    fig = ff.create_streamline(xs, ys, Ex / mag, Ey / mag, density=dens, arrow_scale=0.12,
                               line=dict(color="black", width=1))
    contour = go.Contour(x=xs, y=ys, z=np.clip(V, -5, 5), colorscale="RdBu", reversescale=True,
                         zmin=-5, zmax=5, opacity=0.55, contours=dict(showlines=False),
                         colorbar=dict(title="V"))
    fig.add_trace(contour)
    fig.data = fig.data[-1:] + fig.data[:-1]

    for cx, cy, q in charges:
        fig.add_trace(go.Scatter(x=[cx], y=[cy], mode="markers+text",
                                 text=["+" if q > 0 else ("−" if q < 0 else "0")],
                                 textfont=dict(color="white", size=16),
                                 marker=dict(size=24, color="red" if q > 0 else "blue",
                                             line=dict(color="black", width=1)),
                                 showlegend=False))
    fig.add_trace(go.Scatter(x=[px], y=[py], mode="markers",
                             marker=dict(size=12, color="gold", symbol="x", line=dict(color="black", width=1)),
                             showlegend=False))
    fig.update_xaxes(range=[-4, 4])
    fig.update_yaxes(range=[-3, 3], scaleanchor="x", scaleratio=1)
    fig.update_layout(showlegend=False)
    style(fig, "x", "y", "ເສັ້ນສະໜາມໄຟຟ້າ (ເສັ້ນດຳ) ແລະ ສັກຂະໄຟຟ້າ (ສີພື້ນ)")

    Exp, Eyp, Vp = field(np.array([px]), np.array([py]))
    with c2:
        st.plotly_chart(fig, use_container_width=True)
        m1, m2, m3 = st.columns(3)
        m1.metric("|E| ທີ່ຈຸດທົດສອບ", f"{np.hypot(Exp[0], Eyp[0]):.3f}")
        m2.metric("ທິດຂອງ E", f"{np.degrees(np.arctan2(Eyp[0], Exp[0])):.1f}°")
        m3.metric("V ທີ່ຈຸດທົດສອບ", f"{Vp[0]:.3f}")
    st.info("💡 ຄຳຖາມໃຫ້ນັກສຶກສາ: ເສັ້ນສະໜາມພຸ່ງອອກຈາກປະຈຸຊະນິດໃດ? ຖ້າ q₁ = q₂ ຈຸດໃດທີ່ E = 0?")


# ---------------------------------------------------------------
# 7. RC circuit
# ---------------------------------------------------------------
def rc_circuit():
    st.header("ວົງຈອນ RC (Charging & Discharging Capacitor)")
    st.latex(r"V_C = V_0\left(1-e^{-t/RC}\right)\ \text{(ສາກ)},\qquad V_C = V_0 e^{-t/RC}\ \text{(ປ່ອຍ)},\qquad \tau = RC")

    c1, c2 = st.columns([1, 3])
    with c1:
        mode = st.radio("ໂໝດ", ["ສາກປະຈຸ", "ປ່ອຍປະຈຸ"])
        V0 = st.slider("ແຮງດັນ V₀ (V)", 1.0, 24.0, 12.0, 0.5)
        R = st.slider("ຄວາມຕ້ານທານ R (kΩ)", 0.1, 100.0, 10.0, 0.1)
        C = st.slider("ຄວາມຈຸ C (µF)", 0.1, 1000.0, 100.0, 0.1)
        n_tau = st.slider("ເວລາສະແດງ (ເທົ່າຂອງ τ)", 2, 10, 5)

    tau = R * C  # kΩ * µF = ms
    t = np.linspace(0, n_tau * tau, 600)
    if mode == "ສາກປະຈຸ":
        Vc = V0 * (1 - np.exp(-t / tau))
        v_tau = 0.632 * V0
    else:
        Vc = V0 * np.exp(-t / tau)
        v_tau = 0.368 * V0
    I = (V0 / R) * np.exp(-t / tau)  # V / kΩ = mA

    with c2:
        tab1, tab2 = st.tabs(["ແຮງດັນ V_C(t)", "ກະແສ I(t)"])
        with tab1:
            fig = go.Figure(go.Scatter(x=t, y=Vc, mode="lines", line=dict(width=4), name="V_C"))
            fig.add_vline(x=tau, line_dash="dash", annotation_text="t = τ")
            fig.add_hline(y=v_tau, line_dash="dot")
            st.plotly_chart(style(fig, "ເວລາ t (ms)", "V_C (V)", f"ແຮງດັນຕົວເກັບປະຈຸ — {mode}"),
                            use_container_width=True)
        with tab2:
            fig2 = go.Figure(go.Scatter(x=t, y=I, mode="lines", line=dict(width=4, color="#d62728"), name="I"))
            fig2.add_vline(x=tau, line_dash="dash", annotation_text="t = τ")
            st.plotly_chart(style(fig2, "ເວລາ t (ms)", "I (mA)", "ກະແສໄຟຟ້າໃນວົງຈອນ"),
                            use_container_width=True)

    m1, m2, m3 = st.columns(3)
    m1.metric("ຄ່າຄົງທີ່ເວລາ τ = RC", f"{tau:.2f} ms")
    m2.metric("V_C ທີ່ t = τ", f"{v_tau:.2f} V")
    m3.metric("ກະແສເລີ່ມຕົ້ນ I₀ = V₀/R", f"{V0 / R:.3f} mA")
    st.info("💡 ຄຳຖາມໃຫ້ນັກສຶກສາ: ຖ້າເພີ່ມ R ເປັນ 2 ເທົ່າ ເວລາສາກປະຈຸປ່ຽນແນວໃດ? ຫຼັງຈາກ 5τ ປະຈຸສາກໄດ້ເທົ່າໃດ %?")


# ---------------------------------------------------------------
# 8. Ideal gas thermodynamic processes
# ---------------------------------------------------------------
def gas():
    st.header("ຂະບວນການຂອງແກັສອຸດົມຄະຕິ (Ideal Gas Processes)")
    st.latex(r"PV = nRT,\qquad W=\int P\,dV,\qquad Q=\Delta U+W")

    c1, c2 = st.columns([1, 3])
    with c1:
        proc = st.radio("ຂະບວນການ", ["ອຸນຫະພູມຄົງທີ່ (Isothermal)", "ຄວາມດັນຄົງທີ່ (Isobaric)",
                                      "ອະດີອາບາຕິກ (Adiabatic)"])
        n = st.slider("ຈຳນວນໂມນ n (mol)", 0.1, 5.0, 1.0, 0.1)
        T1 = st.slider("ອຸນຫະພູມເລີ່ມຕົ້ນ T₁ (K)", 200, 600, 300, 10)
        V1 = st.slider("ປະລິມາດເລີ່ມຕົ້ນ V₁ (L)", 0.5, 20.0, 2.0, 0.5)
        V2 = st.slider("ປະລິມາດສຸດທ້າຍ V₂ (L)", 0.5, 20.0, 6.0, 0.5)
        f = st.radio("ຊະນິດແກັສ", [3, 5], format_func=lambda x: "ອະຕອມດຽວ (f = 3)" if x == 3 else "ສອງອະຕອມ (f = 5)")

    R = 8.314
    gam = (f + 2) / f
    P1 = n * R * T1 / V1  # kPa (V in L)
    Vs = np.linspace(V1, V2, 200)

    if proc.startswith("ອຸນຫະພູມ"):
        P = n * R * T1 / Vs
        P2 = n * R * T1 / V2
        W = n * R * T1 * np.log(V2 / V1)
    elif proc.startswith("ຄວາມດັນ"):
        P = np.full_like(Vs, P1)
        P2 = P1
        W = P1 * (V2 - V1)
    else:
        P = P1 * (V1 / Vs) ** gam
        P2 = P1 * (V1 / V2) ** gam
        W = (P1 * V1 - P2 * V2) / (gam - 1)

    T2 = P2 * V2 / (n * R)
    dU = n * (f / 2) * R * (T2 - T1)
    Q = dU + W

    with c2:
        lo, hi = min(V1, V2) * 0.7, max(V1, V2) * 1.3
        Vg = np.linspace(lo, hi, 200)
        fig = go.Figure()
        for T, nm in ((T1, f"ໄອໂຊເທີມ T₁ = {T1:.0f} K"), (T2, f"ໄອໂຊເທີມ T₂ = {T2:.0f} K")):
            fig.add_trace(go.Scatter(x=Vg, y=n * R * T / Vg, mode="lines", name=nm,
                                     line=dict(dash="dot")))
        fig.add_trace(go.Scatter(x=Vs, y=P, mode="lines", name="ຂະບວນການ", fill="tozeroy",
                                 line=dict(width=4, color="#d62728"), fillcolor="rgba(214,39,40,0.2)"))
        fig.add_trace(go.Scatter(x=[V1, V2], y=[P1, P2], mode="markers+text", text=["1", "2"],
                                 textposition="top center", marker=dict(size=12, color="black"),
                                 showlegend=False))
        fig.update_yaxes(rangemode="tozero")
        st.plotly_chart(style(fig, "ປະລິມາດ V (L)", "ຄວາມດັນ P (kPa)", "ແຜນວາດ P–V (ເນື້ອທີ່ໃຕ້ເສັ້ນ = ງານ W)"),
                        use_container_width=True)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("ງານ W", f"{W:.1f} J")
    m2.metric("ΔU", f"{dU:.1f} J")
    m3.metric("ຄວາມຮ້ອນ Q", f"{Q:.1f} J")
    m4.metric("T₂", f"{T2:.1f} K")
    st.info("💡 ຄຳຖາມໃຫ້ນັກສຶກສາ: ເປັນຫຍັງ ΔU = 0 ໃນຂະບວນການອຸນຫະພູມຄົງທີ່? ເປັນຫຍັງ Q = 0 ໃນອະດີອາບາຕິກ?")
