import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Parquet File Path
parquet_file_path = 'data/raw_data/raw_rhythm.csv'
df = pd.read_parquet(parquet_file_path)


