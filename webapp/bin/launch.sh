#!/bin/bash

cd ../
streamlit run mosef.py --server.port 8501 --server.address 0.0.0.0

log_message "You can now view your Streamlit app in your browser."
log_message "URL: http://localhost:8501"
