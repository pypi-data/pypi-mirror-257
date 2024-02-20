#!/usr/bin/env python3

import re, os, json, sys
from traceback import format_exc as traceback_format_exc

from .ecuapass_info_manifiesto import Manifiesto
from .ecuapass_data import EcuData
from .ecuapass_utils import Utils
from .ecuapass_extractor import Extractor  # Extracting basic info from text

#----------------------------------------------------------
USAGE = "\
Extract information from document fields analized in AZURE\n\
USAGE: ecuapass_info_manifiesto.py <Json fields document>\n"
#----------------------------------------------------------
def main ():
	args = sys.argv
	fieldsJsonFile = args [1]
	runningDir = os.getcwd ()
	mainFields = Manifiesto.getMainFields (fieldsJsonFile, runningDir)
	Utils.saveFields (mainFields, fieldsJsonFile, "Results")

#----------------------------------------------------------
# Class that gets main info from Ecuapass document 
#----------------------------------------------------------
class ManifiestoNTA (Manifiesto):
	def __init__(self, fieldsJsonFile, runningDir):
		super().__init__ (fieldsJsonFile, runningDir)
		self.empresa   = EcuData.getEmpresaInfo ("NTA")

	#-- Return IMPORTACION or EXPORTACION
	def getTipoProcedimiento (self):
		docNumber = self.getNumeroManifiesto ()
		if "CO" in docNumber:
			return "IMPORTACION"
		elif "EC" in docNumber:
			return "EXPORTACION"
		else:
			print (f"Alerta: No se pudo definir el tipo de procedimiento desde el número '{docNumber}'")
			return "IMPORTACION||LOW"
#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == '__main__':
	main ()

