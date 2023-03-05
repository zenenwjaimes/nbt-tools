import json


def get_color_data():
    color_json = """
[
    {
        "id": "0",
        "color_name": 0,
        "colors": [
            0,
            0,
            0,
            1
        ]
    },
    {
        "id": "1",
        "color_name": 1,
        "colors": [
            127,
            178,
            56,
            1
        ]
    },
    {
        "id": "2",
        "color_name": 1,
        "colors": [
            247,
            233,
            163,
            1
        ]
    },
    {
        "id": "3",
        "color_name": 1,
        "colors": [
            199,
            199,
            199,
            1
        ]
    },
    {
        "id": "4",
        "color_name": 1,
        "colors": [
            255,
            0,
            0,
            1
        ]
    },
    {
        "id": "5",
        "color_name": 1,
        "colors": [
            160,
            160,
            255,
            1
        ]
    },
    {
        "id": "6",
        "color_name": 1,
        "colors": [
            167,
            167,
            167,
            1
        ]
    },
    {
        "id": "7",
        "color_name": 1,
        "colors": [
            0,
            124,
            0,
            1
        ]
    },
    {
        "id": "8",
        "color_name": 1,
        "colors": [
            255,
            255,
            255,
            1
        ]
    },
    {
        "id": "9",
        "color_name": 1,
        "colors": [
            164,
            168,
            184,
            1
        ]
    },
    {
        "id": "10",
        "color_name": 1,
        "colors": [
            151,
            109,
            77,
            1
        ]
    },
    {
        "id": "11",
        "color_name": 1,
        "colors": [
            112,
            112,
            112,
            1
        ]
    },
    {
        "id": "12",
        "color_name": 1,
        "colors": [
            64,
            64,
            255,
            1
        ]
    },
    {
        "id": "13",
        "color_name": 1,
        "colors": [
            143,
            119,
            72,
            1
        ]
    },
    {
        "id": "14",
        "color_name": 1,
        "colors": [
            255,
            252,
            245,
            1
        ]
    },
    {
        "id": "15",
        "color_name": 1,
        "colors": [
            216,
            127,
            51,
            1
        ]
    },
    {
        "id": "16",
        "color_name": 1,
        "colors": [
            178,
            76,
            216,
            1
        ]
    },
    {
        "id": "17",
        "color_name": 1,
        "colors": [
            102,
            153,
            216,
            1
        ]
    },
    {
        "id": "18",
        "color_name": 1,
        "colors": [
            229,
            229,
            51,
            1
        ]
    },
    {
        "id": "19",
        "color_name": 1,
        "colors": [
            127,
            204,
            25,
            1
        ]
    },
    {
        "id": "20",
        "color_name": 1,
        "colors": [
            242,
            127,
            165,
            1
        ]
    },
    {
        "id": "21",
        "color_name": 1,
        "colors": [
            76,
            76,
            76,
            1
        ]
    },
    {
        "id": "22",
        "color_name": 1,
        "colors": [
            153,
            153,
            153,
            1
        ]
    },
    {
        "id": "23",
        "color_name": 1,
        "colors": [
            76,
            127,
            153,
            1
        ]
    },
    {
        "id": "24",
        "color_name": 1,
        "colors": [
            127,
            63,
            178,
            1
        ]
    },
    {
        "id": "25",
        "color_name": 1,
        "colors": [
            51,
            76,
            178,
            1
        ]
    },
    {
        "id": "26",
        "color_name": 1,
        "colors": [
            102,
            76,
            51,
            1
        ]
    },
    {
        "id": "27",
        "color_name": 1,
        "colors": [
            102,
            127,
            51,
            1
        ]
    },
    {
        "id": "28",
        "color_name": 1,
        "colors": [
            153,
            51,
            51,
            1
        ]
    },
    {
        "id": "29",
        "color_name": 1,
        "colors": [
            25,
            25,
            25,
            1
        ]
    },
    {
        "id": "30",
        "color_name": 1,
        "colors": [
            250,
            238,
            77,
            1
        ]
    },
    {
        "id": "31",
        "color_name": 1,
        "colors": [
            92,
            219,
            213,
            1
        ]
    },
    {
        "id": "32",
        "color_name": 1,
        "colors": [
            74,
            128,
            255,
            1
        ]
    },
    {
        "id": "33",
        "color_name": 1,
        "colors": [
            0,
            217,
            58,
            1
        ]
    },
    {
        "id": "34",
        "color_name": 1,
        "colors": [
            129,
            86,
            49,
            1
        ]
    },
    {
        "id": "35",
        "color_name": 1,
        "colors": [
            112,
            2,
            0,
            1
        ]
    },
    {
        "id": "36",
        "color_name": 1,
        "colors": [
            209,
            177,
            161,
            1
        ]
    },
    {
        "id": "37",
        "color_name": 1,
        "colors": [
            159,
            82,
            36,
            1
        ]
    },
    {
        "id": "38",
        "color_name": 1,
        "colors": [
            149,
            87,
            108,
            1
        ]
    },
    {
        "id": "39",
        "color_name": 1,
        "colors": [
            112,
            108,
            138,
            1
        ]
    },
    {
        "id": "40",
        "color_name": 1,
        "colors": [
            186,
            133,
            36,
            1
        ]
    },
    {
        "id": "41",
        "color_name": 1,
        "colors": [
            103,
            117,
            53,
            1
        ]
    },
    {
        "id": "42",
        "color_name": 1,
        "colors": [
            160,
            77,
            78,
            1
        ]
    },
    {
        "id": "43",
        "color_name": 1,
        "colors": [
            57,
            41,
            35,
            1
        ]
    },
    {
        "id": "44",
        "color_name": 1,
        "colors": [
            135,
            107,
            98,
            1
        ]
    },
    {
        "id": "45",
        "color_name": 1,
        "colors": [
            87,
            92,
            92,
            1
        ]
    },
    {
        "id": "46",
        "color_name": 1,
        "colors": [
            122,
            73,
            88,
            1
        ]
    },
    {
        "id": "47",
        "color_name": 1,
        "colors": [
            76,
            62,
            92,
            1
        ]
    },
    {
        "id": "48",
        "color_name": 1,
        "colors": [
            76,
            50,
            35,
            1
        ]
    },
    {
        "id": "49",
        "color_name": 1,
        "colors": [
            76,
            82,
            42,
            1
        ]
    },
    {
        "id": "50",
        "color_name": 1,
        "colors": [
            142,
            60,
            46,
            1
        ]
    },
    {
        "id": "51",
        "color_name": 1,
        "colors": [
            37,
            22,
            16,
            1
        ]
    },
  {
    "id": "52",
    "color_name": 1,
    "colors": [
      189,
      48,
      49,
      255
    ]
  },
  {
    "id": "53",
    "color_name": 1,
    "colors": [
      148,
      63,
      97,
      255
    ]
  },
  {
    "id": "54",
    "color_name": 1,
    "colors": [
      92,
      25,
      29,
      255
    ]
  },
  {
    "id": "55",
    "color_name": 1,
    "colors": [
      22,
      126,
      134,
      255
    ]
  },
  {
    "id": "56",
    "color_name": 1,
    "colors": [
      58,
      142,
      140,
      255
    ]
  },
  {
    "id": "57",
    "color_name": 1,
    "colors": [
      86,
      44,
      62,
      255
    ]
  },
  {
    "id": "58",
    "color_name": 1,
    "colors": [
      20,
      180,
      133,
      255
    ]
  },
  {
    "id": "59",
    "color_name": 1,
    "colors": [
      100,
      100,
      100,
      255
    ]
  },
  {
    "id": "60",
    "color_name": 1,
    "colors": [
      216,
      175,
      147,
      255
    ]
  },
  {
    "id": "61",
    "color_name": 1,
    "colors": [
      127,
      167,
      150,
      255
    ]
  }
]
    """

    return json.loads(color_json)


def get_expanded_color(base_color, colorId):
    mults = {0: 180, 1: 220, 2: 255, 3: 135}
    mult = mults[colorId]
    color = base_color['colors']

    return list(map(lambda c: int(c * mult/255), color))


def get_all_colors(color_data):
    all_colors = []

    for base_color in color_data:
        all_colors.extend([
            get_expanded_color(base_color, 0),
            get_expanded_color(base_color, 1),
            get_expanded_color(base_color, 2),
            get_expanded_color(base_color, 3)
        ])
    return all_colors
