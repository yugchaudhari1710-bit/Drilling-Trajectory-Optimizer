import math
import streamlit as st

def optimize_trajectory_NE(surface_NEZ, target_NEZ):
    Ns, Es, Zs = surface_NEZ
    Nt, Et, Zt = target_NEZ

    HD = math.sqrt((Nt - Ns)**2 + (Et - Es)**2)
    TVD = abs(Zt - Zs)

    MD_J = math.sqrt(TVD**2 + HD**2)
    MD_S = TVD + 1.2 * HD
    MD_L = TVD + 1.5 * HD

    Cm = 28000
    Cc_J = 100000
    Cc_S = 250000
    Cc_L = 500000

    cost_J = Cm * MD_J + Cc_J
    cost_S = Cm * MD_S + Cc_S
    cost_L = Cm * MD_L + Cc_L

    results = {
        "J-Type": {"MD": MD_J, "Cost": cost_J},
        "S-Type": {"MD": MD_S, "Cost": cost_S},
        "L-Type": {"MD": MD_L, "Cost": cost_L}
    }

    best_type = min(results, key=lambda k: results[k]["Cost"])

    return HD, TVD, results, best_type


st.title("Drilling Trajectory Optimization Tool")

st.header("Enter Surface Coordinates")
Ns = st.number_input("Surface Northing (m)")
Es = st.number_input("Surface Easting (m)")
Zs = st.number_input("Surface TVD (m)")

st.header("Enter Target Coordinates")
Nt = st.number_input("Target Northing (m)")
Et = st.number_input("Target Easting (m)")
Zt = st.number_input("Target TVD (m)")

if st.button("Optimize Trajectory"):
    surface = (Ns, Es, Zs)
    target = (Nt, Et, Zt)

    HD, TVD, results, best = optimize_trajectory_NE(surface, target)

    st.subheader("Results")
    st.write(f"Horizontal Displacement (HD): {HD:.2f} m")
    st.write(f"True Vertical Depth (TVD): {TVD:.2f} m")

    for traj, data in results.items():
        st.write(f"**{traj}** → MD: {data['MD']:.2f} m | Cost: ₹{data['Cost']:.2f}")

    st.success(f"Most Economical Trajectory: {best}")
