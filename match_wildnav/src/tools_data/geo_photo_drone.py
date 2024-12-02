class GeoPhotoDrone:
    """
        Stores a drone photo and its metadata with GNSS location
        and camera rotation parameters
    """
    def __init__(self,filename, photo=0, latitude=0, longitude = 0 ,altitude = 0 ,\
                 gimball_roll = 0, gimball_yaw = 0, gimball_pitch = 0, flight_roll = 0, flight_yaw = 0, flight_pitch = 0):
        self.filename = filename
        self.photo = photo
        self.latitude = latitude
        self.longitude = longitude
        self.latitude_calculated = -1
        self.longitude_calculated = -1
        self.altitude = altitude
        self.gimball_roll = gimball_roll
        self.gimball_yaw = gimball_yaw
        self.gimball_pitch = gimball_pitch
        self.flight_roll = flight_roll
        self.flight_yaw = flight_yaw
        self.flight_pitch = flight_pitch
        self.corrected = False
        self.matched = False

    def __str__(self):
        return f"{self.filename}; \nlatitude: {self.latitude} \nlongitude: {self.longitude} \naltitude: {self.altitude} \n\
        gimball_roll: {self.gimball_roll} \ngimball_yaw: {self.gimball_yaw} \ngimball_pitch: {self.gimball_pitch}\n\
            flight_roll: {self.flight_roll} \nflight_yaw: {self.flight_yaw} \nflight_pitch: {self.flight_pitch}"
        