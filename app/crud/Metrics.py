from fastapi import Depends, HTTPException, UploadFile
import pandas as pd
from sqlalchemy.orm import Session
from io import StringIO
from datetime import datetime, timedelta
from .MetricsController import MetricsController
import database as db
import numpy as np

async def calculateMetrics(profileFile: UploadFile, postFile: UploadFile, db: Session):
    if not profileFile.filename.endswith('.csv') or not postFile.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload CSV files.")

    # Read CSV files
    profilesContent=await profileFile.read()
    postsContent= await postFile.read()
    profileDf = pd.read_csv(StringIO(profilesContent.decode('utf-8')))
    postsDF = pd.read_csv(StringIO(postsContent.decode('utf-8')))

    # Tackling NaN and inf cases as the csv file can have some empty fields. This replaces that with 0.
    profileDf.replace([np.inf, -np.inf, np.nan], 0, inplace=True)
    postsDF.replace([np.inf, -np.inf, np.nan], 0, inplace=True)
    profileData = profileDf.to_dict(orient="records")
    postsData = postsDF.to_dict(orient="records")

    dateBeforeThreeMonths = datetime.now() - timedelta(days=90)
    recentPosts = [post for post in postsData if getFormattedDate(post['pub_date']) >= dateBeforeThreeMonths]
    # Initialize controller with DB session
    metricsController = MetricsController(db)

    await metricsController.store_metrics(recentPosts, profileData)
    # Calculate metrics by content category
    metrics_paid, metrics_organic = metricsController.compute_metrics_by_category(profileData,postsData)
    return {
        "metrics_paid": metrics_paid,
        "metrics_organic": metrics_organic,
    }

async def getMetricsByUsername(username: str, db: Session = Depends(db.get_db)):
    metricsController = MetricsController(db)
    return await metricsController.get_metrics_by_username(username)

async def getAllMetrics(db: Session = Depends(db.get_db)):
    metricsController = MetricsController(db)
    return await metricsController.get_all_metrics_from_db()

def getFormattedDate(date_str):
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S.%fZ"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"time data '{date_str}' does not match any expected format")