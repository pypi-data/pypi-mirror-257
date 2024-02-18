from geopy.distance import geodesic


def bounding_box_corners(center_point, radius= 1000):
    """
    Generates a bounding box around a center point within a specified radius and returns all four corners.

    Parameters:
    - center_point: tuple of (latitude, longitude)
    - radius: radius in meters

    Returns:
    - A dictionary with the coordinates of the 'north_east', 'south_east', 'south_west', and 'north_west' corners of the bounding box.
    """

    # Calculate the north, south, east, and west points by applying the radius distance to the center point
    north = geodesic(meters=radius).destination(center_point, bearing=0)
    south = geodesic(meters=radius).destination(center_point, bearing=180)
    east = geodesic(meters=radius).destination(center_point, bearing=90)
    west = geodesic(meters=radius).destination(center_point, bearing=270)

    # Calculate corners by combining the north/south with east/west
    # we wanted to be intuitive in the direction calculation but let' reverse it'
    north_east = (east.longitude, north.latitude)
    south_east = (east.longitude, south.latitude)
    south_west = (west.longitude, south.latitude)
    north_west = (west.longitude, north.latitude)

    ne = north_east
    sw = south_east
    se = south_west
    nw = north_west
    return ne, se, sw, nw


# Example usage
center_point = (41.8780025, -93.097702)  # Center point
radius = 1000  # Radius in meters

bbox_corners = bounding_box_corners(center_point, radius)
print("Bounding Box Corners:", bbox_corners)
