import cfgrib
import numpy as np
import os
import warnings

warnings.filterwarnings('ignore')

FILE_GRIB = "/home/aithings/ThangNL.202520656/20230101_t00z_f000.grib2"

if not os.path.exists(FILE_GRIB):
    print(f"❌ Không tìm thấy file: {FILE_GRIB}")
    exit()
import cfgrib
import numpy as np
import os
import warnings

warnings.filterwarnings('ignore')

FILE_GRIB = "/home/aithings/ThangNL.202520656/20230101_t00z_f000.grib2"

if not os.path.exists(FILE_GRIB):
    print(f"❌ Không tìm thấy file: {FILE_GRIB}")
    exit()

print("=" * 70)
print("🇻🇳 BẢNG TỔNG QUAN TOÀN DIỆN THỜI TIẾT VIỆT NAM (GFS)")
print("📍 Vĩ độ: 8°N - 24°N | Kinh độ: 102°E - 110°E")
print("=" * 70)

datasets = cfgrib.open_datasets(FILE_GRIB, errors='ignore')

# 🛠️ Hàm "Thợ săn" nâng cấp: Có khả năng nhận diện tầng độ cao
def lay_du_lieu_viet_nam(ten_bien, require_dim=None, exclude_dim=None):
    for ds in datasets:
        if ten_bien in ds.variables:
            dims = list(ds.dims)
            # Lọc theo tầng độ cao nếu có yêu cầu
            if require_dim and require_dim not in dims:
                continue
            if exclude_dim and exclude_dim in dims:
                continue
            
            # Cắt lấy khu vực Việt Nam
            ds_vn = ds.where(
                (ds.latitude >= 8.0) & (ds.latitude <= 24.0) & 
                (ds.longitude >= 102.0) & (ds.longitude <= 110.0), 
                drop=True
            )
            
            if ds_vn[ten_bien].size > 0:
                return ds_vn[ten_bien].values
    return None

# 🛠️ Hàm in thống kê tự động (Cho code gọn gàng, đẹp mắt)
def in_thong_ke(ten_hien_thi, data, don_vi, is_kelvin=False, is_pa=False):
    if data is None:
        print(f"  ⚠️ {ten_hien_thi:<35}: [Không có trong file]")
        return

    # Quy đổi đơn vị cho chuẩn khí tượng
    if is_kelvin:
        data = data - 273.15
    if is_pa:
        data = data / 100.0 # Đổi Pa sang hPa

    min_val = np.nanmin(data)
    max_val = np.nanmax(data)
    mean_val = np.nanmean(data)

    print(f"  🔹 {ten_hien_thi:<35}: Min {min_val:>6.1f} | Max {max_val:>6.1f} | TB {mean_val:>6.1f} {don_vi}")

# ==========================================
print("\n🌱 1. TẦNG DƯỚI LÒNG ĐẤT (Soil Layer)")
print("-" * 70)
in_thong_ke("Nhiệt độ đất (st)", lay_du_lieu_viet_nam('st', require_dim='depthBelowLandLayer'), "°C", is_kelvin=True)
in_thong_ke("Độ ẩm đất (soilw)", lay_du_lieu_viet_nam('soilw', require_dim='depthBelowLandLayer'), "m³/m³")

# ==========================================
print("\n🧍 2. TẦNG SÁT MẶT ĐẤT (Surface & Near-Surface)")
print("-" * 70)
# Nhiệt độ bề mặt (t) KHÔNG ĐƯỢC chứa dimension isobaricInhPa của tầng cao
in_thong_ke("Nhiệt độ da Trái Đất (t)", lay_du_lieu_viet_nam('t', exclude_dim='isobaricInhPa'), "°C", is_kelvin=True)
in_thong_ke("Nhiệt độ 2m (t2m)", lay_du_lieu_viet_nam('t2m'), "°C", is_kelvin=True)
in_thong_ke("Độ ẩm tương đối 2m (r2)", lay_du_lieu_viet_nam('r2'), "%")

u10 = lay_du_lieu_viet_nam('u10')
v10 = lay_du_lieu_viet_nam('v10')
if u10 is not None and v10 is not None:
    in_thong_ke("Tốc độ gió 10m (u10, v10)", np.sqrt(u10**2 + v10**2), "m/s")
else:
    in_thong_ke("Tốc độ gió 10m (u10, v10)", None, "")

u_can = lay_du_lieu_viet_nam('u', require_dim='heightAboveGround')
v_can = lay_du_lieu_viet_nam('v', require_dim='heightAboveGround')
if u_can is not None and v_can is not None:
    in_thong_ke("Gió cận bề mặt 20-100m (u, v)", np.sqrt(u_can**2 + v_can**2), "m/s")
else:
    in_thong_ke("Gió cận bề mặt 20-100m (u, v)", None, "")

in_thong_ke("Gió giật bề mặt (gust)", lay_du_lieu_viet_nam('gust'), "m/s")
in_thong_ke("Áp suất bề mặt (sp)", lay_du_lieu_viet_nam('sp'), "hPa", is_pa=True)
in_thong_ke("Lượng mưa tích lũy (tp)", lay_du_lieu_viet_nam('tp'), "mm")

# ==========================================
print("\n✈️ 3. TẦNG KHÍ QUYỂN (Upper Air - Gộp 26 tầng áp suất)")
print("-" * 70)
in_thong_ke("Nhiệt độ tầng cao (t)", lay_du_lieu_viet_nam('t', require_dim='isobaricInhPa'), "°C", is_kelvin=True)

u_up = lay_du_lieu_viet_nam('u', require_dim='isobaricInhPa')
v_up = lay_du_lieu_viet_nam('v', require_dim='isobaricInhPa')
if u_up is not None and v_up is not None:
    in_thong_ke("Gió tầng cao (u, v)", np.sqrt(u_up**2 + v_up**2), "m/s")
else:
    in_thong_ke("Gió tầng cao (u, v)", None, "")

in_thong_ke("Độ ẩm tầng cao (r)", lay_du_lieu_viet_nam('r', require_dim='isobaricInhPa'), "%")
in_thong_ke("Vận tốc thăng/giáng (w)", lay_du_lieu_viet_nam('w', require_dim='isobaricInhPa'), "Pa/s")
in_thong_ke("Độ cao địa thế kỷ (gh)", lay_du_lieu_viet_nam('gh', require_dim='isobaricInhPa'), "gpm")

# ==========================================
print("\n🌍 4. TÍCH HỢP TOÀN KHÍ QUYỂN (Entire Column)")
print("-" * 70)
in_thong_ke("Tổng che phủ mây (tcc)", lay_du_lieu_viet_nam('tcc'), "%")
in_thong_ke("Nước có thể ngưng tụ (pwat)", lay_du_lieu_viet_nam('pwat'), "mm")
in_thong_ke("Áp suất mực nước biển (prmsl)", lay_du_lieu_viet_nam('prmsl'), "hPa", is_pa=True)

print("\n" + "=" * 70)
print("=" * 60)
print("🇻🇳 BẢNG TỔNG QUAN THỜI TIẾT KHU VỰC VIỆT NAM (GFS)")
print("📍 Tọa độ giới hạn: Vĩ độ 8°N - 24°N | Kinh độ 102°E - 110°E")
print("=" * 60)

datasets = cfgrib.open_datasets(FILE_GRIB, errors='ignore')

# 🛠️ Hàm "Thợ săn" phiên bản Bất Bại
def lay_du_lieu_viet_nam(ten_bien):
    for ds in datasets:
        if ten_bien in ds.variables:
            # Dùng .where() để lọc, bất chấp file xếp Vĩ độ xuôi hay ngược
            ds_vn = ds.where(
                (ds.latitude >= 8.0) & (ds.latitude <= 24.0) & 
                (ds.longitude >= 102.0) & (ds.longitude <= 110.0), 
                drop=True
            )
            
            # Kiểm tra chắc chắn mảng dữ liệu có phần tử bên trong
            if ds_vn[ten_bien].size > 0:
                return ds_vn[ten_bien].values
    return None

# ==========================================
# 1. TRÍCH XUẤT NHIỆT ĐỘ & ĐỘ ẨM
# ==========================================
t2m_raw = lay_du_lieu_viet_nam('t2m')
r2_raw = lay_du_lieu_viet_nam('r2')

if t2m_raw is not None:
    t2m_c = t2m_raw - 273.15
    print(f"🌡️  NHIỆT ĐỘ 2m (°C):")
    print(f"    📉 Thấp nhất toàn quốc : {np.nanmin(t2m_c):.1f} °C")
    print(f"    📈 Cao nhất toàn quốc  : {np.nanmax(t2m_c):.1f} °C")
    print(f"    📊 Trung bình          : {np.nanmean(t2m_c):.1f} °C\n")
else:
    print("⚠️ Không tìm thấy biến Nhiệt độ (t2m).")

if r2_raw is not None:
    print(f"💧 ĐỘ ẨM TƯƠNG ĐỐI (%):")
    print(f"    📉 Thấp nhất           : {np.nanmin(r2_raw):.1f} %")
    print(f"    📈 Cao nhất            : {np.nanmax(r2_raw):.1f} %")
    print(f"    📊 Trung bình          : {np.nanmean(r2_raw):.1f} %\n")
else:
    print("⚠️ Không tìm thấy biến Độ ẩm (r2).")

# ==========================================
# 2. TRÍCH XUẤT TỐC ĐỘ GIÓ
# ==========================================
u10 = lay_du_lieu_viet_nam('u10')
v10 = lay_du_lieu_viet_nam('v10')

if u10 is not None and v10 is not None:
    wind_speed = np.sqrt(u10**2 + v10**2)
    print(f"🌬️  TỐC ĐỘ GIÓ 10m (m/s):")
    print(f"    📉 Tĩnh gió nhất       : {np.nanmin(wind_speed):.1f} m/s")
    print(f"    📈 Gió giật mạnh nhất  : {np.nanmax(wind_speed):.1f} m/s")
    print(f"    📊 Trung bình          : {np.nanmean(wind_speed):.1f} m/s\n")
else:
    print("⚠️ Không tìm thấy biến Gió (u10, v10).")

print("=" * 60)
