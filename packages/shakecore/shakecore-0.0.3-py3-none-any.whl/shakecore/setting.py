MAX_DATA_THRESHOLD: int = 15
MAX_PROCESSING_INFO: int = 100

TABLE_STYLES = [
    dict(selector="th", props=[("text-align", "center")]),
    dict(selector="td", props=[("text-align", "center")]),
    dict(
        selector="td",
        props=[
            ("border", "1px solid rgb(211, 211, 211)"),
            ("max-width", "450px"),
            ("overflow", "hidden"),
            ("white-space", "nowrap"),
        ],
    ),
    dict(selector="th", props=[("border", "1px solid rgb(211, 211, 211)")]),
    dict(
        selector="td:hover",
        props=[
            ("white-space", "normal"),
            ("overflow", "auto"),
            ("background-color", "#ffffcc"),
            ("border", "1px solid black"),
            ("transform", "scale(1.0)"),
        ],
    ),
]
