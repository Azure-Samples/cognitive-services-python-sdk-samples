from azure.ai.anomalydetector import AnomalyDetectorClient
from azure.ai.anomalydetector.models import DetectRequest, TimeSeriesPoint, TimeGranularity, \
    AnomalyDetectorError
from azure.core.credentials import AzureKeyCredential
import pandas as pd
import os


# Add your Azure Anomaly Detector subscription key to your environment variables.
SUBSCRIPTION_KEY = os.environ["ANOMALY_DETECTOR_SUBSCRIPTION_KEY"]

CSV_FOLDER = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "csv_files")


def get_series_from_file(path):
    df = pd.read_csv(path, header=None, encoding="utf-8", parse_dates=[0])
    series = []
    for index, row in df.iterrows():
        series.append(TimeSeriesPoint(timestamp=row[0], value=row[1]))
    return series


def get_request():
    series = get_series_from_file(os.path.join(
        CSV_FOLDER, "anomaly_detector_daily_series.csv"))
    return DetectRequest(series=series, granularity=TimeGranularity.daily)


def entire_detect(subscription_key):
    print("Sample of detecting anomalies in the entire series.")
    # Add your Azure Anomaly Detector subscription key to your environment variables.
    endpoint = os.environ["ANOMALY_DETECTOR_ENDPOINT"]
    
    client = AnomalyDetectorClient(AzureKeyCredential(subscription_key), endpoint)
    request = get_request()

    try:
        response = client.detect_entire_series(request)
    except AnomalyDetectorError as e:
        print('Error code: {}'.format(e.error.code), 'Error message: {}'.format(e.error.message))
    except Exception as e:
        print(e)

    if any(response.is_anomaly):
        print('Anomaly was detected from the series at index:')
        for i, value in enumerate(response.is_anomaly):
            if value:
                print(i)
    else:
        print('No anomalies were detected in the time series.')


def last_detect(subscription_key):
    print("Sample of detecting whether the latest point in series is anomaly.")
    # Add your Azure Anomaly Detector subscription key to your environment variables.
    endpoint = os.environ["ANOMALY_DETECTOR_ENDPOINT"]
    
    client = AnomalyDetectorClient(AzureKeyCredential(subscription_key), endpoint)
    request = get_request()

    try:
        response = client.detect_last_point(request)
    except AnomalyDetectorError as e:
        print('Error code: {}'.format(e.error.code), 'Error message: {}'.format(e.error.message))
    except Exception as e:
        print(e)

    if response.is_anomaly:
        print('The latest point is detected as anomaly.')
    else:
        print('The latest point is not detected as anomaly.')


if __name__ == "__main__":
    import sys
    import os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))
    from tools import execute_samples
    execute_samples(globals(), SUBSCRIPTION_KEY)
