{
    "name": "pos restaurant location access",
    "version": "1.0",
    "category": "point_of_sale",
    "summary": "pos restaurant location access",
    "description": """
        pos restaurant location access
    """,
    "author": "Warlock Technologies Pvt Ltd.",
    "website": "http://warlocktechnologies.com",
    "support": "info@warlocktechnologies.com",
    "depends": ['pos_restaurant','pos_hr'],
    "data": [
        "views/assets.xml",
        'views/views.xml'
    ],
    'qweb': [
        'static/src/xml/FloorScreen.xml',
    ],
    "images": ['static/images/screen_image.png'],
    "license": "AGPL-3",
    "installable": True,
}
