FROM agrigorev/zoomcamp-model:mlops-3.9.7-slim

WORKDIR /app

COPY [ "predict.py", "predict.py" ]

RUN pip3 install pandas
RUN pip3 install pyarrow
RUN pip3 install scikit-learn==1.0.2