class GeoPhotoSate:
    """
        Stores a satellite photo and its latitude and longitude at top-left and bottom-right corner.
    """
    def __init__(self, filename, photo, geo_top_left, geo_bottom_right):
        self.filename = filename
        self.photo = photo
        self.top_left_coord = geo_top_left
        self.bottom_right_coord = geo_bottom_right

    def __lt__(self, other):
         return self.filename < other.filename

    def __str__(self):
        return  f"{self.filename}; \n\ttop_left_latitude: {self.top_left_coord[0]} \n\ttop_left_lon: {self.top_left_coord[1]} \n\t\
        bottom_right_lat: {self.bottom_right_coord[0]} \n\tbottom_right_lon {self.bottom_right_coord[1]}"