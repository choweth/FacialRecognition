from flask import Flask

app = Flask(__name__)
from app import home
from app import meanFaceCalculator
from app import MakePerson
from app import FaceProcessor
from app import WhoAmI
from app import DownloadColoredImage
from app import DownloadGrayImage
from app import DownloadMeanFace
from app import DownloadNetMeanFace
