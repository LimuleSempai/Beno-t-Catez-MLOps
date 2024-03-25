from typing import Optional

import streamlit as st
from prometheus_client import REGISTRY, Counter, start_http_server
from prometheus_client.registry import Collector


@st.cache_resource # It is important to add a cache for streamlit to not load several time the metric server
def init_metrics():
    start_http_server(9090)
    # The counter will create 2 metrics. Here page_loaded_total and page_loaded_created
    # page_loaded_total is the value of the counter
    # page_loaded_created is the unix time of the creation of the counter (https://en.wikipedia.org/wiki/Unix_time)
    Counter("page_loaded", "Number of times the data app is loaded", registry=REGISTRY)
    # TODO: Declare metrics

def get_metric(metric_name: str) -> Optional[Collector]:
    return REGISTRY._names_to_collectors.get(metric_name, None)


def get_metric_value(metric_name: str) -> Optional[float]:
    return REGISTRY.get_sample_value(metric_name)

get_metric("page_loaded").inc()
st.write(get_metric_value("page_loaded_total"))