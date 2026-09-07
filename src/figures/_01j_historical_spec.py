"""Historical public-domain imagery specifications."""

from __future__ import annotations

HISTORICAL_ASSETS: tuple[dict[str, str], ...] = (
    {
        "slug": "historical-hexagon-quang-tri",
        "title": "HEXAGON Satellite Image of Vietnam War Bomb Craters",
        "caption": ("Public-domain USGS EROS declassified HEXAGON image used as a historical example of imagery becoming a governed analytic source."),
        "alt_text": "Black-and-white declassified satellite imagery of Quang Tri bomb craters.",
        "source_page": "https://www.usgs.gov/media/images/hexagon-satellite-image-vietnam-war-bomb-craters",
        "asset_url": "https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/media/images/19730320_HEXAGON_QuangTri.png",
        "source_section": "chapter:16",
        "date": "1973-03-20",
    },
    {
        "slug": "historical-forbidden-city",
        "title": "Declassified Satellite Imagery of the Forbidden City",
        "caption": ("Public-domain USGS EROS declassified imagery of the Forbidden City as a local historical image for GEOINT source-provenance discussion."),
        "alt_text": "Black-and-white satellite image of the Forbidden City in Beijing.",
        "source_page": "https://www.usgs.gov/media/images/declassified-satellite-imagery-forbidden-city-beijing-china",
        "asset_url": "https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/media/images/Declassified%20imagery%20D3C1205-100021A081_Bejing_03121973.jpg",
        "source_section": "chapter:11",
        "date": "1966 approx.",
    },
    {
        "slug": "historical-dakar-kh7",
        "title": "KH-7 Imagery of Dakar",
        "caption": ("Public-domain USGS EROS KH-7 image used to show how historical collection becomes reproducible open-source imagery analysis."),
        "alt_text": "Black-and-white KH-7 imagery of the western edge of Dakar, Senegal.",
        "source_page": "https://www.usgs.gov/media/images/declassified-satellite-imagery-declass-1",
        "asset_url": "https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/thumbnails/image/dmiddeclass1senegalafrica.jpg",
        "source_section": "chapter:16",
        "date": "1966 approx.",
    },
    {
        "slug": "historical-missouri-river-kh9",
        "title": "KH-9 Imagery of the Missouri River",
        "caption": ("Public-domain USGS EROS KH-9 image used as a historical example of declassified remote-sensing material with explicit provenance."),
        "alt_text": "Declassified satellite imagery and modern map view of the Missouri River.",
        "source_page": "https://www.usgs.gov/media/images/declassified-satellite-imagery-declass-3",
        "asset_url": "https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/thumbnails/image/dmiddeclass3moriversd.jpg",
        "source_section": "chapter:11",
        "date": "1982-07-22",
    },
)
