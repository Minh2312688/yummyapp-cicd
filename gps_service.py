class GPSSignalLostError(Exception):
    """Ngoại lệ tùy chỉnh khi thiết bị mất tín hiệu định vị GPS."""
    pass


def get_current_location():
    """
    Hàm mô phỏng truy cập phần cứng GPS điện thoại để lấy tọa độ.
    Trong môi trường kiểm thử tự động, hàm này sẽ được đóng thế (mock).
    """
    return (10.0, 105.0)