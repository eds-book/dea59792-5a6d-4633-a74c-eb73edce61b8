import numpy as np

def gaussian_plume(x, y, sources_x, sources_y, sources_q, u, Ry, ry, Rz, rz, wind_deg, T, P, M, R):
    """
    Gaussian plume model
    ipout：g/h
    output：ppb
    """
    sources_q = np.array(sources_q) / 3600 / 1000  # g/h → kg/s
    theta = -np.radians(wind_deg)
    cos_t, sin_t = np.cos(theta), np.sin(theta)
    c = np.zeros_like(x, dtype=np.float64)

    for sx, sy, q in zip(sources_x, sources_y, sources_q):
        dx = x - sx
        dy = y - sy
        dx_rot = dx * cos_t - dy * sin_t
        dy_rot = dx * sin_t + dy * cos_t
        valid = dy_rot > 0
        if not np.any(valid):
            continue
        sigma_y = Ry * dy_rot[valid] ** ry
        sigma_z = Rz * dy_rot[valid] ** rz
        term1 = q / (np.pi * u * sigma_y * sigma_z)
        term2 = np.exp(-dx_rot[valid] ** 2 / (2 * sigma_y ** 2))
        c[valid] += (term1 * term2).astype(np.float32)

    c = c * R * T * 1e9 / (P * M)
    return c

def inverse_gaussian_plume(x, y, source_x, source_y, c_obs, u, Ry, ry, Rz, rz, wind_deg, T, P, M, R):
    """
    Reverse Gaussian plume model
    - x, y: Observation point location (scalar or array)
    - source_x, source_y: Assuming the single source location
    - c_obs:  observed concentration (ppb)
    - return： source（g/h）
    """

    # Coordinate rotation
    theta = -np.radians(wind_deg)
    cos_t, sin_t = np.cos(theta), np.sin(theta)
    dx = x - source_x
    dy = y - source_y
    dx_rot = dx * cos_t - dy * sin_t
    dy_rot = dx * sin_t + dy * cos_t

    if dy_rot <= 0:
        return 0.0  # 背风方向不考虑

    # σ calculation, adding a lower limit to avoid numerical explosion caused by sigma_y and sigma_z being too small
    sigma_y = Ry * dy_rot ** ry
    sigma_z = Rz * dy_rot ** rz
    sigma_y = max(sigma_y, 1e-3)
    sigma_z = max(sigma_z, 1e-3)

    # ppb to kg/m³
    c_kg_m3 = c_obs * P * M / (R * T * 1e9)

    # Back-calculated source intensity (kg/s)
    exp_term = np.exp(dx_rot**2 / (2 * sigma_y**2))
    q_kg_s = c_kg_m3 * np.pi * u * sigma_y * sigma_z * exp_term

    # to g/h
    q_g_h = q_kg_s * 3600 * 1000
    return q_g_h
