import enum


# ----------------------------------------------------------------------------------------------------------------------
# Database Definitions
# ----------------------------------------------------------------------------------------------------------------------


class DatabaseEnv(str, enum.Enum):
    DATABASE_API_KEY = "ZYNHinvWEIjTsjPZnfZxFKj7JpdFcRqd7qSdITbqTPRPUKtb7Ynd2hyoE5FedBf4"
    DATABASE_API = "https://sa-east-1.aws.data.mongodb-api.com/app/data-eoplo/endpoint/data/v1/action/"
    DATABASE_ADDRESS_PROD = "mongodb+srv://dev:mulJCizXkNhTUYa4@mulJCizXkNhTUYa4cluster0.efian0n.mongodb.net/"
    DATABASE_ADDRESS_DEBUG = "mongodb://localhost:27017/"
    DATABASE_NAME = "smart_energy"
    DATA_SOURCE = "Cluster0"


# ----------------------------------------------------------------------------------------------------------------------
# Firebase Config
# ----------------------------------------------------------------------------------------------------------------------

class FirebaseConfig(str, enum.Enum):
    CERTIFICATE = {
        "type": "service_account",
        "project_id": "smart-energy-3e7aa",
        "private_key_id": "a28437b42ed9938a47bd6eb468d7800bfffd8722",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDdieSndjL6L6uw\nRFwQN0ayMq7bmpMkmOcc7oyoWgpOEDQMtNDLFs6P4Xx7UBkiA1PLHKtxAflqy3U4\n2e1o/O264grzOK+qmRVNO+jILP2pZSJtl6FPLku8vPzwrU545FdhEGXAPaPnPGVM\nYQ0++TykmhsPk0OsfJYdut5LEV1vc8PGW9D9iOcakdD9sOvdwLX/3HF5ZzSW4/2b\nLSxz1wFnBSn6kvYFlDpuERa9NUd78g9SBDzLrjiEfs7kGvfQ6fb/8qo6ZunEKmhQ\nPgEWipmabG9G2lHS48SWKG6FOGwMVPwWQ8SnaqJqA2VXSAxYU0ma42JWWfOw0BOc\nBGI9r8E/AgMBAAECggEAEFiBxfdbKImG5fENR+cEMNa7fxmHHM6pUsGpICzQkNTy\nOjPHKgzrPcN531FYIWHUd2qMncBzCjWr1v+BXFs5IS5Xd32pvHEiGLpAYTCsoKiF\nI0fqT4DPdsQM96cZ4KKcbd17XHVP2BplMP8CLrDOECkMsRgBCMOCgfwNNcW4uqXR\nT9tR83lNZcpzmuknLrnslE13MGBmNu+x5VeOj/irxMa2I9Ed5NkGbcfl0PsZcH1v\n96tmtNPsH4e/nGIOPmj05PQEJ90D+F0UFSCYG0VotXsusE6lKrSz8mBzzglbeeG+\nITt77GKBozbMKDog88+584l9dNL/yZl+ndgEkxbB6QKBgQD5woEJEX73ZsuFUM7H\ndU09khG9t7i/mTM3Rju0dNpPF6cmP+R155SqntO38/fQ68rt8e/Hr1MiteuvB/Jc\nYp2fxVXyAu76M2wGl2g1kKWcA5QKFro+GX9ipyIGLPCwpNlhb8f8bxyzFtMHOAfI\nwkHRWMOKwZzDqFsp3OAJg/m8RwKBgQDjEuISE/GJd3tcrUsRYb+O3Ttc3GmTLS8h\nEnNrXjDHTeLMCHCFXDxTBCNDys5sBeAcePgxcGThy0yScg3xuk/fKWkszQUdJ5lF\nuzwQ79SG2Lyynauvl7pg3uIUdYxlmXLDICoIIKttyoy0eATu6LNuZa2KiLk80DDs\no/nJJEPnSQKBgCLgxqQ9jT1/XWyAnF++QcsXWuLjhSk8e6p8ZFoO922UIAN3aLAO\nZvRsuaQ2raS/SNdxscpw8WsnfII02eOM4fYt2JKzViwagjtpaWQRjw76cPH3uopx\nhRiBvn6eR/5jBvhUY9kcqyVXSqD3ch7XAdn6S1RVNU8dc52k+qRZicaBAoGAIjm4\nZW0oHMYri9560BXhn5Ds36RBLXPEBMIZL3e09nVg18v12cP7O7AF+LPaxSFllCUP\nk7QTII1Z70DNpT+lxkchmSUVvj03tvDvrsXXTLPiTTHCrOa7qtotTVQiYzXrvEle\nzHbQH+5FovXsGG5ujRc6PwU4llfy59gXUB/tNDECgYBQFgZAw01OLk5sPzJR2piO\nt/+5F9jsilCe18HdOVw2dHUK5QUA6jpqcUoUST07pOOmKHDefk//TZavVvWAaDgk\nv9y9+hvB1ugQuv/8U6+TVoLuupZnZKsOd1CS3ybgye1lTQXwx1gJ63yiFD9ZOmfD\nij1ORKVcOS7vOAyUdASWVw==\n-----END PRIVATE KEY-----\n",
        "client_email": "python-dataset@smart-energy-3e7aa.iam.gserviceaccount.com",
        "client_id": "102996860316558247871",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/python-dataset%40smart-energy-3e7aa.iam.gserviceaccount.com"
    }
    CONFIG = {
        "apiKey": "AIzaSyCxujiFsfdNZEH8zIxIQwaAXvujQvSFyA4",
        "authDomain": "smart-energy-3e7aa.firebaseapp.com",
        "databaseURL": "https://smart-energy-3e7aa-default-rtdb.firebaseio.com",
        "projectId": "smart-energy-3e7aa",
        "storageBucket": "smart-energy-3e7aa.appspot.com",
        "messagingSenderId": "8984393302",
        "appId": "1:8984393302:web:e1d193912f96b7d68d6df7",
        "measurementId": "G-RKB971HGGY"
    }
