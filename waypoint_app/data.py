from waypoint_core.domain import Distance, DayHike, BackpackingRoute

# Mock database of trails using your waypoint_core domain models
TRAILS_DB = {
    "1": DayHike(
        trail_id="1",
        name="Blue Ridge Summit Trail",
        distance=Distance(8.5, "km"),
        elevation_gain_m=450,
        difficulty="moderate"
    ),
    "2": BackpackingRoute(
        trail_id="2",
        name="Cascade Pass Loop",
        distance=Distance(24.0, "km"),
        elevation_gain_m=1200,
        difficulty="hard"
    ),
    "3": DayHike(
        trail_id="3",
        name="Pine Forest Meadow Trail",
        distance=Distance(4.2, "km"),
        elevation_gain_m=110,
        difficulty="easy"
    )
}