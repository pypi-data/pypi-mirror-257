import pandas as pd
import tldextract

def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [col.lower().replace(" ", "_").replace(".", "") for col in df.columns]
    return df


def clean_domain(url: str) -> str:    
    ext = tldextract.extract(url.strip()) # handled uk.co, and high stars
    return ext.registered_domain

def domain_is_none(url: str) -> bool:
    return url is None or url == ""
