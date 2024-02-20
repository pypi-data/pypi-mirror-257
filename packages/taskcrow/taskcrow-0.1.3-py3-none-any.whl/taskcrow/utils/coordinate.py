import math


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the Haversine distance between two points on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r


def transform_epsg2097_to_wgs84_coordinate(x, y):
    from pyproj import Proj, transform
    # Projection 정의
    # 중부원점(Bessel): 서울 등 중부지역 EPSG:2097
    proj_1 = Proj(init='epsg:2097')

    # WGS84 경위도: GPS가 사용하는 좌표계 EPSG:4326
    proj_2 = Proj(init='epsg:4326')
    x_, y_ = transform(proj_1, proj_2, x, y)
    return {'x': x_, 'y': y_}


# 주어진 GPS 좌표를 중심으로 반경 1km 내에 100m 간격의 그리드 좌표 셀을 만드는 함수를 정의합니다.
# 각 그리드 셀은 left bottom, right top 그리고 center 좌표를 포함합니다.

def create_grid_with_center(lat, lon, radius_km, cell_size_m):
    # 지구의 반지름 (킬로미터 단위)
    R = 6371.0

    # 셀 크기를 미터에서 킬로미터로 변환
    cell_size_km = cell_size_m / 1000.0

    # 그리드의 셀 개수를 계산
    num_cells = int((radius_km * 2) / cell_size_km)

    # 셀당 위도와 경도 변화량 계산
    delta_lat = (cell_size_km / R) * (180 / np.pi)
    delta_lon = (cell_size_km / R) * (180 / np.pi) / np.cos(lat * np.pi / 180)

    # 그리드 좌표 생성
    grid = []
    for i in range(num_cells):
        row = []
        for j in range(num_cells):
            # 셀의 left bottom 좌표 계산
            bottom_lat = lat - (radius_km * (180 / np.pi) / R) + (i * delta_lat)
            bottom_lon = lon - (radius_km * (180 / np.pi) / R) / np.cos(lat * np.pi / 180) + (j * delta_lon)
            # 셀의 right top 좌표 계산
            top_lat = bottom_lat + delta_lat
            top_lon = bottom_lon + delta_lon
            # 셀의 center 좌표 계산
            center_lat = (top_lat + bottom_lat) / 2
            center_lon = (top_lon + bottom_lon) / 2
            # 셀의 좌표를 튜플로 저장 (left bottom, right top, center)
            cell_coordinates = ((bottom_lat, bottom_lon), (top_lat, top_lon), (center_lat, center_lon))
            # 셀을 행에 추가
            row.append(cell_coordinates)
        # 행을 그리드에 추가
        grid.append(row)
    return grid


def create_grid_in_region(left_bottom, right_top, interval_meters):
    def meters_to_lat(meters):
        radius = 6356752.3142  # Earth's polar radius in meters
        return (meters / radius) * (180 / math.pi)

    def meters_to_lon(meters, lat):
        radius = 6378137  # Earth's equatorial radius in meters
        return (meters / (radius * math.cos(math.pi * lat / 180))) * (180 / math.pi)

    left_bottom_lat, left_bottom_lon = left_bottom
    right_top_lat, right_top_lon = right_top

    grid_coordinates = []
    current_lat = left_bottom_lat
    while current_lat < right_top_lat:
        current_lon = left_bottom_lon
        while current_lon < right_top_lon:
            lat_interval = meters_to_lat(interval_meters)
            lon_interval = meters_to_lon(interval_meters, current_lat)
            cell_rt = (current_lat + lat_interval, current_lon + lon_interval)
            cell_center = ((current_lat + cell_rt[0]) / 2, (current_lon + cell_rt[1]) / 2)
            grid_coordinates.append({"lb": (current_lat, current_lon), "rt": cell_rt, "center": cell_center})
            current_lon += lon_interval
        current_lat += lat_interval

    return grid_coordinates

# Unit test
if __name__ == "__main__":
    left_bottom_test = (37.0, 127.0)
    right_top_test = (37.1, 127.1)
    interval_test = 10000  # 10km interval

    grid_cells_with_centers = create_grid_in_region(left_bottom_test, right_top_test, interval_test)
    for cell in grid_cells_with_centers:
        print(f"LB: {cell['lb']}, RT: {cell['rt']}, Center: {cell['center']}")
