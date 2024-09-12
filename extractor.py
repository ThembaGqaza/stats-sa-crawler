from pathlib import Path
import requests
import pandas as pd
from tqdm import tqdm


# Data directory
DATA_PATH = Path("data")
DATA_PATH.mkdir(parents=True, exist_ok=True)  # Ensure directory exists

# Base URL for the API
BASE_URL = "https://disseminationapi-a2f6fff8f7a3f3ff.z01.azurefd.net"
TIMEOUT = 10


def fetch_report_data(table_name, muni_id):
    """Fetch data from a specific report based on the municipality ID."""
    url = f"{BASE_URL}/api/{table_name}/get{table_name}Report/1/3/{muni_id}"
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return []


def fetch_provinces():
    """Fetch all provinces."""
    url = f"{BASE_URL}/api/Provinces/getAll/"
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        provinces = response.json()
        return [
            (
                p["provinceId"], p["provinceDesc"],
                p["provinceAbbreviation"]
            ) for p in provinces
        ]
    except requests.exceptions.RequestException:
        return []


def fetch_districts(province_id):
    """Fetch all districts for a given province."""
    url = f"{BASE_URL}/api/Districts/listByProvince/{province_id}"
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        districts = response.json()
        return [(d["districtMdbc"], d["districtName"]) for d in districts]
    except requests.exceptions.RequestException:
        return []


def fetch_municipalities(district_id):
    """Fetch all municipalities for a given district."""
    url = f"{BASE_URL}/api/Municipalities/listByDistrict/{district_id}"
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        municipalities = response.json()
        return [(m["muniCode"], m["muniName"]) for m in municipalities]
    except requests.exceptions.RequestException:
        return []


# List of report types to extract data from
data2extract = [
    "DsAgeGroups",
    "DsPopulationGroups",
    "DsSexes",
    "DsLanguages",
    "DsHighestLevelEducations",
    "DsTypeOfMainDwellings",
    "DsAccessToPipedWaters",
    "DsMainToiletFacilitys",
    "DsRefuseDisposals",
    "DsEnergyForCookings",
    "DsSchoolAttendences"
]


def filter_columns(df, table_name):
    """
    Filter columns by removing those ending with 'String',
    except for DsAgeGroups.
    """
    if table_name == "DsAgeGroups":
        cols = [
            "timeSeriesDesc", "geoLevelValueDesc",
            "label", "countsMales", "countsPercentageMales",
            "countsFemales", "countsPercentageFemales"
        ]
    else:
        cols = [col for col in df.columns if not col.endswith("String")]
    return df.loc[:, cols]


def extract_and_save_reports_by_table():
    """
    Main function to loop through provinces, districts, and municipalities,
    extracting and saving reports.
    """
    provinces = fetch_provinces()

    for (
        province_id, province_name, province_abbreviation
    ) in tqdm(provinces, desc="Provinces"):
        districts = fetch_districts(province_id)

        for district_id, district_name in districts:
            municipalities = fetch_municipalities(district_id)

            for muni_id, muni_name in municipalities:
                for table_name in tqdm(
                    data2extract,
                    desc=f"Processing tables for {province_name}",
                    leave=False
                ):
                    report_data = fetch_report_data(table_name, muni_id)

                    if report_data:
                        df = pd.DataFrame(report_data)
                        df_filtered = filter_columns(df, table_name)
                        df_filtered.loc[:, "Province"] = province_name
                        df_filtered.loc[:, "District"] = district_name
                        df_filtered.loc[:, "Municipality"] = muni_name
                        df_filtered.loc[:, "ReportType"] = table_name

                        file_name = DATA_PATH / f"{table_name}_report.csv"
                        try:
                            df_filtered.to_csv(
                                file_name, mode="a",
                                header=not file_name.exists(),
                                index=False
                            )
                        except Exception:
                            print(
                                f"""Error saving data for {table_name} in
                                {muni_name}: {Exception}"""
                            )
                    else:
                        continue


# Run the extraction process
if __name__ == "__main__":
    try:
        extract_and_save_reports_by_table()
    except Exception as e:
        print(f"Error during extraction process: {e}")
