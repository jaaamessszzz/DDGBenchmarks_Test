import common.ddgproject
import common.colortext as colortext
from ddglib import help, dbapi
from ddglib.ddgfilters import *

#help.help()

def simpleRunExample(self):
	# Step 1: Open a database connection
	ddGdb = common.ddgproject.ddGDatabase()

	# Step 2: Select database records
	sr = StructureResultSet(ddGdb, AdditionalIDs = ['2BQC', '1LAW', '1LHH', '1LHI'])
	
	# Step 3: Add filters
	sr.addFilter(StructureFilter.TotalBFactors(0,16) | StructureFilter.WithNullResolution(True))
	
	# Step 4: Retrieve full database records. 
	# results will be a list each of whose elements is a dict representing a database record.
	results = sr.getFilteredResults()
	
	# Step 5: Optionally print summary
	print("\nSummary: %s\n" % sr)


# Create a result set
class Examples:
	
	@staticmethod
	def printOutput(resultset):
		print("Applying filters")
		results = resultset.getFilteredResults()
		print("After application")
		print("\nSummary: %s\n" % resultset)

	@staticmethod
	def openDB():
		if not globals().get("ddGdb"):
			globals()["ddGdb"] = common.ddgproject.ddGDatabase()

	@staticmethod
	def help():
		help.ShowDatabaseStructure()
		help.ShowResultSet()
		help.ShowFilter()

	# UnionFilter examples

	@staticmethod
	def unionFilterExample1():
		print("** All structures with null OR non-null resolution **") 
		Examples.openDB()
		sr = StructureResultSet(ddGdb)
		sr.addFilter(StructureFilter.WithNullResolution(False) | StructureFilter.WithNullResolution(True))
		Examples.printOutput(sr)

	@staticmethod
	def unionFilterExample2():
		print("** All structures with null AND non-null resolution**") 
		Examples.openDB()
		sr = StructureResultSet(ddGdb)
		sr.addFilter(StructureFilter.WithNullResolution(False))
		sr.addFilter(StructureFilter.WithNullResolution(True))
		Examples.printOutput(sr)


	# StructureResultSet examples

	@staticmethod
	def allStructures():
		'''Select all Structure records.'''
		print("** All strucures **") 
		Examples.openDB()
		sr = StructureResultSet(ddGdb)
		Examples.printOutput(sr)

	@staticmethod
	def getStructuresWithNullResolutionSQL():
		print("** All structures with null resolution **") 
		Examples.openDB()
		sr = StructureResultSet(ddGdb, SQL = "WHERE Resolution IS NULL")
		Examples.printOutput(sr)

	@staticmethod
	def getStructuresWithNullResolutionFilter():
		print("** All structures with null resolution **") 
		Examples.openDB()
		sr = StructureResultSet(ddGdb)
		sr.addFilter(StructureFilter.WithNullResolution(True))
		Examples.printOutput(sr)

	@staticmethod
	def pickSpecific():
		'''Select four specific Structure records and apply a filter.''' 
		print("** 4 specific structures **") 
		Examples.openDB()
		sr = StructureResultSet(ddGdb, AdditionalIDs = ['2BQC', '1LAW', '1LHH', '1LHI'])
		sr.addFilter(StructureFilter.TotalBFactors(0,16) | StructureFilter.WithNullResolution(True))
		Examples.printOutput(sr)

	@staticmethod
	def getStructuresInResolutionRange():
		print("** All structures with null resolution **") 
		Examples.openDB()
		sr = StructureResultSet(ddGdb)
		sr.addFilter(StructureFilter.Resolution(1, 2))
		Examples.printOutput(sr)
	
	@staticmethod
	def getStructuresWithUniProtIDs():
		print("** All structures with null resolution **") 
		Examples.openDB()
		sr = StructureResultSet(ddGdb)
		sr.addFilter(StructureFilter.WithUniProtIDs(["P0A7Y4"], ["RNH_ECOLI", "RNP30_RANPI"]))
		Examples.printOutput(sr)

	@staticmethod
	def getStructuresFilteredByStructures():
		'''Select all Structure records.'''
		print("** Experiments filtered by structures **") 
		Examples.openDB()
		
		sr1 = StructureResultSet(ddGdb, SQL = "WHERE PDB_ID LIKE %s", parameters = "1A%")
		Examples.printOutput(sr1)
		
		sr2 = StructureResultSet(ddGdb, SQL = "WHERE PDB_ID LIKE %s", parameters = "1AY%")
		Examples.printOutput(sr2)
		
		sr = sr1.filterBySet(sr2)
		Examples.printOutput(sr)


	# ExperimentResultSet examples

	@staticmethod
	def getExperimentsWithSQL():
		'''Select all Structure records.'''
		print("** All structures **") 
		Examples.openDB()
		er = ExperimentResultSet(ddGdb, SQL = "WHERE Structure LIKE %s", parameters = "1A%")
		Examples.printOutput(er)
		print(er.structure_map.keys())
		
		er.addFilter(StructureFilter.Resolution(1, 1.7))
		
		Examples.printOutput(er)
		
	@staticmethod
	def getExperimentsFilteredByStructures():
		'''Select all Structure records.'''
		print("** Experiments filtered by structures **") 
		Examples.openDB()
		
		sr = StructureResultSet(ddGdb, SQL = "WHERE PDB_ID LIKE %s", parameters = "1AY%")
		Examples.printOutput(sr)
		
		er = ExperimentResultSet(ddGdb, SQL = "WHERE Structure LIKE %s", parameters = "1A%")
		Examples.printOutput(er)
		
		er = er.filterBySet(sr)
		Examples.printOutput(er)
		
		er = ExperimentResultSet(ddGdb, SQL = "WHERE Structure LIKE %s", parameters = "1AY%")
		Examples.printOutput(er)
		
		#print(er.structure_map.keys())
		
		er.addFilter(StructureFilter.Resolution(1, 1.7))
		
		Examples.printOutput(er)
	
	@staticmethod
	def getExperimentsFilteredBySource():
		'''Select all Structure records.'''
		print("** Experiments filtered by structures **") 
		Examples.openDB()
		
		er = ExperimentResultSet(ddGdb)
		Examples.printOutput(er)
		
		er.addFilter(ExperimentFilter.OnSource(ExperimentFilter.ProTherm))
		
		Examples.printOutput(er)

	
	@staticmethod
	def getExperimentsFilteredByMutationSize():
		'''Select all Structure records.'''
		print("** Experiments filtered by mutation size **") 
		Examples.openDB()
		
		er = ExperimentResultSet(ddGdb)
		Examples.printOutput(er)
		
		#er.addFilter(ExperimentFilter.MutationsBetweenAminoAcidSizes('small', 'large'))
		#er.addFilter(ExperimentFilter.MutationsBetweenAminoAcidSizes(ExperimentFilter.large, ExperimentFilter.small))
		er.addFilter(ExperimentFilter.MutationsBetweenAminoAcidSizes(ExperimentFilter.large, ExperimentFilter.large))
		
		Examples.printOutput(er)

	@staticmethod
	def getExperimentsFilteredByAminoAcids1():
		'''Select all Structure records.'''
		print("** Experiments filtered by residue (from ALA) **") 
		Examples.openDB()
		
		er = ExperimentResultSet(ddGdb)
		Examples.printOutput(er)
		
		er.addFilter(ExperimentFilter.MutationsBetweenAminoAcids('ALA', 'G'))
		
		Examples.printOutput(er)

	@staticmethod
	def getExperimentsFilteredByAminoAcids2():
		'''Select all Structure records.'''
		print("** Experiments filtered by residue (from ALA) **") 
		Examples.openDB()
		
		er = ExperimentResultSet(ddGdb)
		Examples.printOutput(er)
		
		er.addFilter(ExperimentFilter.MutationsBetweenAminoAcids('A', 'GLY'))
		
		Examples.printOutput(er)

	@staticmethod
	def getExperimentsFilteredBySourceAndResolution():
		'''Select all Structure records.'''
		print("** Experiments filtered by structures **") 
		Examples.openDB()
		
		er = ExperimentResultSet(ddGdb)
		Examples.printOutput(er)
		
		er.addFilter(ExperimentFilter.OnSource(ExperimentFilter.ProTherm))
		
		Examples.printOutput(er)
		
		er.addFilter(StructureFilter.Resolution(1, 2))
		Examples.printOutput(er)
		
		
	# PredictionResultSet examples

	@staticmethod
	def getPredictionsWithSQL():
		'''Select all Structure records.'''
		print("** All structures **") 
		Examples.openDB()
		pr = PredictionResultSet(ddGdb, SQL = "WHERE PredictionSet=%s AND ID=12595", parameters = "testrun")
		Examples.printOutput(pr)

	@staticmethod
	def getPredictionsUsingMultipleFilters():
		'''This demonstrates the use of multiple filters.'''
		print("** Multiple filter example **") 
		Examples.openDB()
		pr = PredictionResultSet(ddGdb, SQL = "WHERE PredictionSet=%s", parameters = "testrun")
		pr.addFilter(StructureFilter.Techniques(StructureFilter.XRay))
		#Examples.printOutput(pr)
		pr.addFilter(StructureFilter.Resolution(1, 1.5) | StructureFilter.Resolution(3.9, 4))
		#Examples.printOutput(pr)
		pr.addFilter(StructureFilter.TotalBFactors(0, 10))
		Examples.printOutput(pr)

	@staticmethod
	def getPredictionsUsingMultipleFilters_Speed():
		'''This demonstrates how slow separate filters are.'''
		print("** Multiple filter example **") 
		Examples.openDB()

		import time
		
		t1 = time.time()
		pr = PredictionResultSet(ddGdb, SQL = "WHERE PredictionSet=%s", parameters = "testrun")
		pr.addFilter(StructureFilter.Techniques(StructureFilter.XRay))
		pr.addFilter(StructureFilter.Resolution(1, 1.5) | StructureFilter.Resolution(3.9, 4))
		pr.addFilter(StructureFilter.TotalBFactors(0, 10))
		Examples.printOutput(pr)
		t2 = time.time()

		print("Time taken: %0.2fs" % (t2 - t1))

		t1 = time.time()
		pr = PredictionResultSet(ddGdb, SQL = "WHERE PredictionSet=%s", parameters = "testrun")
		sf = StructureFilter()
		sf.setTechniques(StructureFilter.XRay)
		sf.setResolution(1, 1.5)
		sf.setTotalBFactors(0, 10)
		pr.addFilter(sf | StructureFilter.Resolution(3.9, 4))
		Examples.printOutput(pr)
		t2 = time.time()
		print("Time taken: %0.2fs" % (t2 - t1))

	@staticmethod
	def getPredictionsUsingMultipleFilters2():
		print("** Multiple filter example **") 
		Examples.openDB()
		
	@staticmethod
	def showResultSetOperations():
		'''Demonstrates how to union, intersect, subtract, and XOR ResultSets.'''
		print("\n** ResultSet SR1 **\n")
		Examples.openDB()
		sr1 = StructureResultSet(ddGdb)
		sr1.addFilter(StructureFilter.Resolution(1, 1.3))
		Examples.printOutput(sr1)
		
		print("\n** ResultSet SR2 **\n")
		sr2 = StructureResultSet(ddGdb)
		sr2.addFilter(StructureFilter.Resolution(2, 2.3))
		Examples.printOutput(sr2)
		
		print("\n** ResultSet SR3 **\n")
		sr3 = StructureResultSet(ddGdb)
		sr3.addFilter(StructureFilter.Resolution(1.2, 2))
		Examples.printOutput(sr3)
		
		print("\n** ResultSet union - SR1 | SR2 **\n")
		srUnion = sr1 | sr2
		print(join(srUnion._log, "\n"))
		
		print("\n** ResultSet union - SR1 - SR3 **\n")
		
		srUnion = sr1 | sr3
		print(join(srUnion._log, "\n"))

		print("\n** ResultSet intersection - SR1 & SR3 **\n")
		
		srIntersection = sr1 & sr3
		print(join(srIntersection._log, "\n"))
		
		print("\n** ResultSet intersection sanity check **\n")
		
		sr4 = StructureResultSet(ddGdb)
		sr4.addFilter(StructureFilter.Resolution(1.2, 1.3))
		Examples.printOutput(sr4)
		
		print("\n** ResultSet difference - SR1 - SR3 **\n")
		
		#srDifference = sr1 - sr3
		srDifference = sr1 / sr3
		print(join(srDifference._log, "\n"))

		print("\n** ResultSet exclusive or - SR1 ^ SR3 **\n")
		
		srXOR = sr1 ^ sr3
		print(join(srXOR._log, "\n"))
	
	@staticmethod
	def showAllEligibleProTherm(PredictionSet, ProtocolID, KeepHETATMLines):
		#inserter = JobInserter()
		colortext.printf("\nAdding ProTherm mutations to %s prediction set." % PredictionSet, "lightgreen")
		#ddGdb = ddgproject.ddGDatabase()
		
		from webparser import MAX_NUMRES_PROTHERM, MAX_STANDARD_DEVIATION, MAX_RESOLUTION
		
		Examples.openDB()
		
		import time
		if False:
			t1 = time.time()
			er1 = ExperimentResultSet(ddGdb)
			er1.addFilter(ExperimentFilter.OnSource(ExperimentFilter.ProTherm))
			er1.addFilter(ExperimentFilter.NumberOfMutations(1, 1))
			er1.addFilter(ExperimentFilter.NumberOfChains(1, 1))
			er1.addFilter(ExperimentFilter.StandardDeviation(None, MAX_STANDARD_DEVIATION))
			er1.addFilter(StructureFilter.Resolution(None, MAX_RESOLUTION))
			er1.addFilter(StructureFilter.Techniques(StructureFilter.XRay))
			Examples.printOutput(er1)
			t2 = time.time()
			print(t2 - t1)
		
		# This method usually takes around 65% of the time as the method above 
		t1 = time.time()
		ef1 = ExperimentFilter()
		ef1.setSource(ExperimentFilter.ProTherm)
		ef1.setNumberOfMutations(1, 1)
		ef1.setNumberOfChains(1, 1)
		ef1.setStandardDeviation(None, MAX_STANDARD_DEVIATION)
		sf1 = StructureFilter()
		sf1.setResolution(None, MAX_RESOLUTION)
		sf1.setTechniques(StructureFilter.XRay)
		er1 = ExperimentResultSet(ddGdb)
		er1.addFilter(ef1)
		er1.addFilter(sf1)
		Examples.printOutput(er1)
		t2 = time.time()
		print(t2 - t1)
		
		experimentIDs = sorted(list(er1.getFilteredIDs()))
		colortext.message("\nThe number of unique ProTherm experiments with:\n\t- one mutation;\n\t- structures solved by X-ray diffraction and with <= %d residues;\n\t- a maximum standard deviation in experimental results of <= %0.2f;\n\t- and a resolution of <= %0.2f Angstroms.\nis %d.\n" % (MAX_NUMRES_PROTHERM, MAX_STANDARD_DEVIATION, MAX_RESOLUTION, len(experimentIDs)))
		ddG_connection = dbapi.ddG()
		count = 0
		print("")
		for experimentID in experimentIDs:
			ddG_connection.addPrediction(experimentID, PredictionSet, ProtocolID, KeepHETATMLines, StoreOutput = True)
			count += 1
			if count >= 10:
				colortext.write(".")
				colortext.flush()
				count = 0
		print("")
		
	@staticmethod
	def testAnalysis():
		ddG_connection = dbapi.ddG()
		pr = PredictionResultSet(ddGdb, SQL = "WHERE ID >= 12804 and ID <= 12903")
		ddG_connection.analyze(pr)
	
	@staticmethod
	def testPublications():
		ddG_connection = dbapi.ddG()
		pr = PredictionResultSet(ddGdb, SQL = "WHERE ID >= 12804 and ID <= 12903")
		er = ExperimentResultSet(ddGdb, SQL = "WHERE ID >= 73534 and ID <= 73561")
		ddG_connection.getPublications(pr)
		ddG_connection.getPublications(er)
	
	
ddGdb = common.ddgproject.ddGDatabase()

Examples.help()

#ddG_connection = dbapi.ddG()
#ddG_connection.dumpData("testzip.zip", 12803)


#Examples.testAnalysis()
Examples.testPublications()

#Examples.showAllEligibleProTherm("kellogg16-A", "Kellogg:10.1002/prot.22921:protocol16:32231", False)
#Examples.getExperimentsFilteredByStructures()
#Examples.getStructuresFilteredByStructures()
#Examples.showResultSetOperations()
#Examples.getStructuresWithUniProtIDs()
#Examples.getExperimentsFilteredByStructures()
#Examples.getExperimentsFilteredBySource()
#Examples.getExperimentsFilteredBySourceAndResolution()
#Examples.getExperimentsFilteredByMutationSize()
#Examples.getExperimentsFilteredByAminoAcids1()
#Examples.getExperimentsFilteredByAminoAcids2()
#Examples.help()
#Examples.getPredictionsUsingMultipleFilters_Speed()
#help.ShowFilter()
#Examples.allStructures()
#Examples.pickSpecific()
