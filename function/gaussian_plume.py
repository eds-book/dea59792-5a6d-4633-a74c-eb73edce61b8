import numpy as np

def gaussian_plume(x, y, sources_x, sources_y, sources_q, u, Ry, ry, Rz, rz, wind_deg, T, P, M, R):
    """
    高斯羽流模型（单位转换版本）
    输入源强单位：g/h
    输出浓度单位：ppb
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
    根据观测浓度反推源强度（单位 g/h）
    - x, y: 观测点位置（标量或数组）
    - source_x, source_y: 假设单一源位置
    - c_obs: 观测浓度 (ppb)
    - 返回源强（g/h）
    """

    # 坐标旋转
    theta = -np.radians(wind_deg)
    cos_t, sin_t = np.cos(theta), np.sin(theta)
    dx = x - source_x
    dy = y - source_y
    dx_rot = dx * cos_t - dy * sin_t
    dy_rot = dx * sin_t + dy * cos_t

    if dy_rot <= 0:
        return 0.0  # 背风方向不考虑

    # σ计算，加下限避免sigma_y、sigma_z过小导致数值爆炸
    sigma_y = Ry * dy_rot ** ry
    sigma_z = Rz * dy_rot ** rz
    sigma_y = max(sigma_y, 1e-3)
    sigma_z = max(sigma_z, 1e-3)

    # ppb转kg/m³的转换系数（注意这里是正向转换）
    c_kg_m3 = c_obs * P * M / (R * T * 1e9)

    # 反推源强度（kg/s），指数符号为正，指数项是放大因子
    exp_term = np.exp(dx_rot**2 / (2 * sigma_y**2))
    q_kg_s = c_kg_m3 * np.pi * u * sigma_y * sigma_z * exp_term

    # 转为 g/h
    q_g_h = q_kg_s * 3600 * 1000
    return q_g_h
