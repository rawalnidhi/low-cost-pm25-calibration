
from pathlib import Path
from urllib.request import Request, urlopen
from zipfile import ZipFile, is_zipfile
import shutil


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
DOWNLOAD_DIR = RAW_DIR / "downloads"

# Official dataset sources
DATASETS = {
    "24hr_collocation": {
        "url": (
            "https://pasteur.epa.gov/uploads/10.23719/"
            "1522388/Data_DevelopmentUSPAcorrection_210408.zip"
        ),
        "archive": "24hr_collocation.zip",
        "main_csv": "Full24hrdataset.csv",
    },
    "hourly_smoke": {
        "url": (
            "https://pasteur.epa.gov/uploads/10.23719/"
            "1528138/Dataset_PurpleAirSmoke_Barkjohn_3_15_23.zip"
        ),
        "archive": "hourly_smoke.zip",
        "main_csv": "Finaldataset_correcteddatasetwholding_10_26_22.csv",
    },
    "aqs_monitors": {
        "url": "https://aqs.epa.gov/aqsweb/airdata/aqs_monitors.zip",
        "archive": "aqs_monitors.zip",
        "main_csv": "aqs_monitors.csv",
    },
}

DAILY_AQS_FILES = {
    year: (
        f"https://aqs.epa.gov/aqsweb/airdata/daily_88101_{year}.zip",
        f"daily_88101_{year}.zip",
        f"daily_88101_{year}.csv",
    )
    for year in (2018, 2019, 2020)
}


def download_file(url: str, destination: Path) -> None:
    """Download a file only when it is not already available."""
    if destination.is_file() and destination.stat().st_size > 0:
        print(f"Already downloaded: {destination.name}")
        return

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = destination.with_suffix(destination.suffix + ".part")

    request = Request(
        url,
        headers={"User-Agent": "PM25-Calibration-Research/1.0"},
    )

    try:
        with urlopen(request, timeout=120) as response:
            with temporary_path.open("wb") as output:
                shutil.copyfileobj(response, output)

        if temporary_path.stat().st_size == 0:
            raise ValueError(f"Downloaded file is empty: {destination.name}")

        temporary_path.replace(destination)
        print(f"Downloaded: {destination.name}")

    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise


def extract_required_csv(
    archive_path: Path,
    destination_dir: Path,
    expected_csv: str,
) -> Path:
    """Validate an archive and extract only the required CSV."""
    destination = destination_dir / expected_csv

    if destination.is_file() and destination.stat().st_size > 0:
        print(f"Already prepared: {destination.relative_to(PROJECT_ROOT)}")
        return destination

    if not is_zipfile(archive_path):
        raise ValueError(f"Invalid ZIP archive: {archive_path}")

    destination_dir.mkdir(parents=True, exist_ok=True)

    with ZipFile(archive_path) as archive:
        bad_file = archive.testzip()
        if bad_file is not None:
            raise ValueError(f"Corrupt file in archive: {bad_file}")

        matches = [
            name
            for name in archive.namelist()
            if Path(name).name == expected_csv
            and not name.endswith("/")
        ]

        if len(matches) != 1:
            raise FileNotFoundError(
                f"Expected exactly one {expected_csv} in "
                f"{archive_path.name}; found: {matches}"
            )

        member = matches[0]

        with archive.open(member) as source, destination.open("wb") as output:
            shutil.copyfileobj(source, output)

    if not destination.is_file() or destination.stat().st_size == 0:
        raise ValueError(f"Extraction failed: {destination}")

    print(f"Prepared: {destination.relative_to(PROJECT_ROOT)}")
    return destination


def prepare_purpleair_dataset(name: str, config: dict) -> None:
    """Download and prepare a PurpleAir research dataset."""
    dataset_dir = RAW_DIR / name
    main_csv = dataset_dir / config["main_csv"]

    if main_csv.is_file() and main_csv.stat().st_size > 0:
        print(f"READY: {main_csv.relative_to(PROJECT_ROOT)}")
        return

    archive_path = DOWNLOAD_DIR / config["archive"]
    download_file(config["url"], archive_path)

    extract_required_csv(
        archive_path,
        dataset_dir,
        config["main_csv"],
    )


def prepare_aqs_monitor_listing() -> None:
    """Download and prepare the EPA AQS monitor listing."""
    config = DATASETS["aqs_monitors"]
    destination = RAW_DIR / config["main_csv"]

    if destination.is_file() and destination.stat().st_size > 0:
        print(f"READY: {destination.relative_to(PROJECT_ROOT)}")
        return

    archive_path = DOWNLOAD_DIR / config["archive"]
    download_file(config["url"], archive_path)

    extract_required_csv(
        archive_path,
        RAW_DIR,
        config["main_csv"],
    )


def prepare_aqs_daily_data() -> None:
    """Download daily PM2.5 ZIP files for 2018–2020."""
    for year, (url, archive_name, _) in DAILY_AQS_FILES.items():
        archive_path = RAW_DIR / archive_name

        download_file(url, archive_path)

        if not is_zipfile(archive_path):
            raise ValueError(
                f"Invalid EPA AQS ZIP archive: {archive_path}"
            )

        with ZipFile(archive_path) as archive:
            bad_file = archive.testzip()

            if bad_file is not None:
                raise ValueError(
                    f"Corrupt file in {archive_name}: {bad_file}"
                )

        print(f"READY: {archive_path.relative_to(PROJECT_ROOT)}")


def main() -> None:
    print("Preparing research datasets...\n")

    for name, config in DATASETS.items():
        if name != "aqs_monitors":
            prepare_purpleair_dataset(name, config)

    prepare_aqs_monitor_listing()
    prepare_aqs_daily_data()

    print("\nAll required datasets are available.")
    print(f"Raw data directory: {RAW_DIR}")


if __name__ == "__main__":
    main()
