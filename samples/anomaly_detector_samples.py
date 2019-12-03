from azure.cognitiveservices.anomalydetector import AnomalyDetectorClient
from azure.cognitiveservices.anomalydetector.models import Request, Point, Granularity, \
    APIErrorException
from datetime import datetime, timezone
from msrest.authentication import CognitiveServicesCredentials
import pandas as pd
import os

# Add your Azure Anomaly Detector subscription key to your environment variables.
SUBSCRIPTION_KEY = os.environ.get["ANOMALY_DETECTOR_SUBSCRIPTION_KEY"]

CSV_FOLDER = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "csv_files")


def get_series_from_file(path):
    df = pd.read_csv(path, header=None, encoding="utf-8", parse_dates=[0])
    series = []
    for index, row in df.iterrows():
        series.append(Point(timestamp=row[0], value=row[1]))
    return series


def get_request():
    series = get_series_from_file(os.path.join(
        CSV_FOLDER, "anomaly_detector_daily_series.csv"))
    return Request(series=series, granularity=Granularity.daily)


def entire_detect(subscription_key):
    print("Sample of detecting anomalies in the entire series.")
    # Add your Azure Anomaly Detector subscription key to your environment variables.
    endpoint = os.environ.get["ANOMALY_DETECTOR_ENDPOINT"]
    
    try:
        client = AnomalyDetectorClient(
            endpoint, CognitiveServicesCredentials(subscription_key))
        request = get_request()
        response = client.entire_detect(request)
        if True in response.is_anomaly:
            print("Anomaly was detected from the series at index:")
            for i in range(len(request.series)):
                if response.is_anomaly[i]:
                    print(i)
        else:
            print("There is no anomaly detected from the series.")
    except Exception as e:
        if isinstance(e, APIErrorException):
            print("Error code: {}".format(e.error.code))
            print("Error message: {}".format(e.error.message))
        else:
            print(e)


def last_detect(subscription_key):
    print("Sample of detecting whether the latest point in series is anomaly.")
    # Add your Azure Anomaly Detector subscription key to your environment variables.
    endpoint = os.environ.get["ANOMALY_DETECTOR_ENDPOINT"]
    
    try:
        client = AnomalyDetectorClient(
            endpoint, CognitiveServicesCredentials(subscription_key))
        request = get_request()
        response = client.last_detect(request)
        if response.is_anomaly:
            print("The latest point is detected as anomaly.")
        else:
            print("The latest point is not detected as anomaly.")
    except Exception as e:
        if isinstance(e, APIErrorException):
            print("Error code: {}".format(e.error.code))
            print("Error message: {}".format(e.error.message))
        else:
            print(e)


if __name__ == "__main__":
    import sys
    import os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))
    from tools import execute_samples
    execute_samples(globals(), SUBSCRIPTION_KEY)
