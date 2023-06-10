from shapely.geometry import shape, Point
import json


def is_inside(polygon, long, lat):
  point = Point(long, lat)
  return polygon_shape.contains(point)
