from flask import Flask, send_from_directory, render_template, request, url_for, flash
from datetime import datetime
from pytz import timezone
import os
import MySQLdb
import pandas as pd
import numpy as py
from Bio import SeqIO
from Bio import Phylo
import re
import csv
import hashlib
import json
import cgi
from mod_tables.models import TableBuilder
import pylab
import matplotlib
import matplotlib.pyplot as plt
##
# try:
#
# except:
# 	print "PLEASE INSTALL GRAPHVIZ PROGRAM FROM THE WEBSITE, NOT PIP !!!!!!!!!!!!!!!!!!!!!"
# 	print "PLEASE INSTALL pip install pygraphviz !!!!!!!!!!!!!!!!!!!!!!"
# 	print "PLEASE INSTALL pip install matplotlib !!!!!!!!!!!!!!!!!"

table_builder = TableBuilder()
#import xml.etree.ElementTree as ET
#from pyfastaq import sequences
#import fasta

app = Flask(__name__)
from common.routes import main
from mod_tables.controllers import tables
app.register_blueprint(main)
app.register_blueprint(tables)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
#app.secret_key = 'SUPER_SECRET_KEY_BIO_PROJECT'

ALLOWED_EXTENSIONS = set(["xml", "mzid", "mzTab", "mztab" ,"fasta"])
ALLOWED_EX_XML = set(["xml", "mzid"])
ALLOWED_EX_MZTAB = set(["mzTab", "mztab"])
ALLOWED_EX_FASTA = set(["fasta","fa", "faa"])

# Connect to the database
try:
	connection = MySQLdb.connect(host="localhost",
						port=3306,
						user="root",
						passwd="root",
						db="genome_data")#genome_data
except:
	print "Failed to connect to db!!"
	print "Please ensure you have started your MySQL server and the db name is correct"
	print "and that the port is set to 3306 in your server"
	pass


cur = connection.cursor() # May need to open it in each function instead of globally


@app.route("/")
def indexpage():
	now = datetime.now().strftime('%H:%M:%S %d-%m-%Y')#datetime.now(timezone('Europe/London'))
	return render_template("index.html", time = now)
	#return "The time is {}".format(now)

@app.route('/family_table_LINE1')
def family_table_LINE1():
	cur.execute("SELECT repeat_name, no_repeats, no_proteins_found, proteins_found FROM `l1_groupby_repeat_names` ORDER BY `l1_groupby_repeat_names`.`no_proteins_found` DESC")
	HERV_LbR_rows = cur.fetchall()
	return render_template("family_table_LINE1.html", data=HERV_LbR_rows)

@app.route("/protein_table_HERV")
def serverside_table():
    return render_template("erv_proteins.html")

@app.route("/protein_table_L1")
def serverside_table2():
    return render_template("l1_proteins.html")

@app.route("/family_table_HERV_Superfamilies")
def family_table_HERV_Superfamilies():
	cur.execute("SELECT superfamily, description, no_repeats, no_proteins_found, proteins_found FROM `herv_groupby_superfamilies`")
	HERV_GbS_rows = cur.fetchall()
	protlist = []
	countlist = []
	for ele in HERV_GbS_rows:
		countlist.append(int(ele[2]))
		protlist.append(int(ele[3]))
	return render_template("family_table_HERV_Superfamilies.html", data=HERV_GbS_rows, arr_sc=countlist, arr_sc_2=protlist)

@app.route("/family_table_HERV_Families")
def family_table_HERV_Families():
	cur.execute("SELECT * FROM `herv_groupby_families`")
	HERV_GbF_rows = cur.fetchall()
	return render_template("family_table_HERV_Families.html", data=HERV_GbF_rows)


@app.route("/family_table_HERV_Repeats")
def family_table_HERV_Repeats():
	cur.execute("SELECT * FROM `herv_groupby_repeat_names`")
	HERV_GbR_rows = cur.fetchall()
	wisit="Repeat Name"
	return render_template("family_table_HERV_Repeats.html", data=HERV_GbR_rows)


@app.route("/distribution")
def distribution():
	cur.execute("SELECT Count FROM `herv_count`")
	Herv_count=cur.fetchall()
	H=[element for h in Herv_count for element in h] #removes tuple
	cur.execute("SELECT Count FROM `l1_count`")
	L1_count=cur.fetchall()
	L=[element for l in L1_count for element in l] #removes tuple
	return render_template("distribution.html", H=H, L=L)

@app.route("/AA_seq_list")
def AA_seq_list():
	return render_template("AA_seq_list.html")

@app.route("/relationship_AA", methods=["GET", "POST"])
def relationship_AA():
	if request.method == "POST":
		if request.form["rv_button"] == "HERV":
			return render_template("herv_rv.html")
		elif request.form["rv_button"] == "LINE1":
			return render_template("line1_rv.html")
	else:
		return render_template("relationship_AA.html")

@app.route("/herv_rv")
def herv_rv():
	return render_template("herv_rv.html")

@app.route("/herv_rv1")
def herv_rv1():
	return render_template("herv_rv1.html")

@app.route("/custom_tree", methods=["GET", "POST"])
def custom_tree():
	if request.method == "POST":
		if 'file_rv' in request.files:
			# Creates a path to the specified folder
			target = os.path.join(APP_ROOT, "static/assets/img/customtree/")
			# Creates directory if it doesnt already exist
			if not os.path.isdir(target):
				os.mkdir(target)

			  # Saves the file to the target folder explicitly mentioned earlier
			for file in request.files.getlist("file_rv"):
				filename = file.filename
				destination = "/".join([target, filename])
				file.save(destination)

			dpi_type = int(request.form.get('dpi_type'))

				# Checks the current directory and moves to the correct folder
			if os.getcwd() == APP_ROOT:
				os.chdir("static/assets/img/customtree/")
			elif os.getcwd() == APP_ROOT+"/static/assets/img/customtree/":
				pass
			elif os.getcwd() == APP_ROOT+"\uploaded":
				os.chdir("../static/assets/img/customtree/")
			elif os.getcwd() == APP_ROOT+"\sequence_ident":
				os.chdir("../static/assets/img/customtree/")


			tree = Phylo.read(filename, 'newick')
			tree.ladderize()   # Flip branches so deeper clades are displayed at top
			Phylo.draw(tree)
			try:
				Phylo.draw_graphviz(tree)
			except:
				pass
			#pylab.show()
			pylab.savefig("customtree.png", dpi=dpi_type)

			#\static\assets\img\customtree\customtree.png

			# #ptree = Phylo.draw(tree)
			# matplotlib.rc('font', size=6)
		    # # set the size of the figure
			# fig = plt.figure(figsize=(10, 20), dpi=100)
		    # # alternatively
		    # # fig.set_size_inches(10, 20)
			# axes = fig.add_subplot(1, 1, 1)
			# Phylo.draw(tree, axes=axes)
			# plt.savefig("output_file.png", dpi=100)

			return render_template("custom_tree.html")


	else:
		return render_template("relationship_AA.html")

@app.route("/line1_rv")
def line1_rv():
	return render_template("line1_rv.html")

@app.route("/peptide_seq_ident", methods=["GET","POST"])
def peptide_seq_ident():
	# global empty_error
	# global rows_count
	# global result_seq
	# global no_match
	# global recordID
	# global result_seq_one
	# global data11
	result_seq_one=[]
	result_seq_multi=[]
	result_seq=""
	rows_count = ""
	error_empty2 = "This is an empty file! Please upload a populated FASTA file"
	no_match= "No Match was found!"
	error_fasta_1 = "Please Enter only 1 fasta sequence in the search bar, for multiple use upload function"
	error_fasta_2 = "Please Remove the Headers and only Search using the peptide Sequences or use the upload function"


	# If data has been submitted to the page i.e uploaded, then the POST method engages
	if request.method == "POST":
		# If the Textbox has been filled with peptide sequences, DB is searched for matching sequence and FAMILY + sequence returned
		# Otherwise if no match found, displays no match
		if request.form["fasta_content"] != "":
			fasta_check = request.form["fasta_content"]
			fasta_check = fasta_check.count(">")
			# Checks to see if a header exists and rejects the data if it does
			if fasta_check > 1:
				return render_template("peptide_seq_ident.html", empty = error_fasta_1)
			elif fasta_check == 1:
				fastaseq = request.form["fasta_content"]
				return render_template("peptide_seq_ident.html", empty = error_fasta_2)

			else:
				# Saves the peptide sequences and removes all spaces, tabs and new lines
				# Does a MYSQL query for the correctly formatted peptide sequence
				fastaseq = request.form["fasta_content"]
				fastaseq = fastaseq.replace("\n","").replace("\r","").replace(" ","")
				rows_count = cur.execute("SELECT family, sequence FROM all_prot_seqs WHERE sequence = %s", [fastaseq])
				cur.execute("SELECT family, sequence FROM all_prot_seqs WHERE sequence = %s", [fastaseq])
				result_seq =  cur.fetchall()
				result_seq_one.append(result_seq)
				DF_PD=pd.DataFrame(result_seq_one)
				result_seq_df=DF_PD.to_html()
				if not cur.rowcount:
				  return render_template("peptide_seq_ident.html", result_family=no_match)
				else:
				  return render_template("peptide_seq_ident.html", data1=result_seq)

		# If a file has been uploaded (file2 - name of upload form), this if statement occurs
		elif 'file2' in request.files:
			# Creates a path to the specified folder
			target = os.path.join(APP_ROOT, "sequence_ident/")
			# Creates directory if it doesnt already exist
			if not os.path.isdir(target):
				os.mkdir(target)

			  # Saves the file to the target folder explicitly mentioned earlier
			for file in request.files.getlist("file2"):
				filename = file.filename
				destination = "/".join([target, filename])
				file.save(destination)

				# Checks the current directory and moves to the correct folder
			if os.getcwd() == APP_ROOT:
				os.chdir("sequence_ident")
			elif os.getcwd() == APP_ROOT+"\sequence_ident":
				pass
			elif os.getcwd() == APP_ROOT+"\uploaded":
				os.chdir("..\sequence_ident")


			# Goes through fasta file and checks whether if its empty
			seqfile = SeqIO.parse(filename, "fasta")
			if os.stat(filename).st_size == 0:
				return render_template("peptide_seq_ident.html", empty = error_empty2)

			# Checks the file extension, if it is not in the allowed fasta format, it is rejected
			elif filename.rsplit('.', 1)[1].lower() not in ALLOWED_EX_FASTA:
				result_seq_multi = "Incorrect filetype uploaded! Please Upload a Fasta formatted file"
				return render_template("peptide_seq_ident.html", empty=result_seq_multi)


			else:
				# if file contains information, retrieve data from the DB,
				# if request from DB does not have data returned (rowcount=0), show no match,
				# otherwise display Family + sequence
				record_list = list(SeqIO.parse(filename, "fasta"))
				if len(record_list) == 1:
					#If only 1 fasta sequence in file
					for record in SeqIO.parse(filename, "fasta"):
						recordID = record.seq
						rows_count = cur.execute("SELECT family, sequence FROM all_prot_seqs WHERE sequence = %s", [recordID])
						cur.execute("SELECT family, sequence FROM all_prot_seqs WHERE sequence = %s", [recordID])
						result_seq =  cur.fetchall()
						result_seq_one.append(result_seq)
						DF_PD=pd.DataFrame(result_seq_one)
						result_seq_df=DF_PD.to_html()
					if not cur.rowcount:
					  return render_template("peptide_seq_ident.html", empty=no_match)
					else:
						return render_template("peptide_seq_ident.html", data=result_seq_one)
				else:
					for record in SeqIO.parse(filename, "fasta"):
						# Loop which iterates through ever fasta sequence and appends the results
						recordID = record.seq
						rows_count = cur.execute("SELECT family, sequence FROM all_prot_seqs WHERE sequence = %s", [recordID])
						cur.execute("SELECT family, sequence FROM all_prot_seqs WHERE sequence = %s", [recordID])
						result_seq =  cur.fetchall()
						if cur.rowcount > 0:
							result_seq_multi.append(result_seq)
					DF_PD=pd.DataFrame(result_seq_multi)
					result_seq_df=DF_PD.to_html()
					if not cur.rowcount:
					  return render_template("peptide_seq_ident.html", empty=no_match)
					else:
					  return render_template("peptide_seq_ident.html", data=result_seq_multi)
		elif request.form["fasta_content"] == "":
			return render_template("peptide_seq_ident.html", empty = error_empty2)
	else:
		# By default, this GET method is returned and displays 1000 sequences and families from the database
		cur.execute("SELECT family, sequence FROM all_prot_seqs LIMIT 0, 1000")
		result_seq =  cur.fetchall()
		return render_template("peptide_seq_ident.html", data1=result_seq)



@app.route("/upload_peptide", methods=["GET","POST"])
def upload_peptide():
	# global filename2
	# global pepseq
	# global list_of_matches
	# global list_of_pep_seqs
	# global empty_error
	# global rows_count
	# global result_seq
	# global no_match
	# global recordID
	global result_seq_multi
	result_seq_multi=[]
	result_seq_multi2=[]
	result_seq=""
	rows_count = ""
	no_match= "No Match was found"
	list_of_matches = []
	list_of_pep_seqs = []
	rowlist=[]
	rowlist2=[]

	# Checks for post method (data submitted)
	if request.method == "POST":
		target = os.path.join(APP_ROOT, "uploaded/")

		#Creates the folder if it doesnt exist
		if not os.path.isdir(target):
			os.mkdir(target)

		#Saves the file into the specified location above
		for file in request.files.getlist("file"):
			filename2 = file.filename
			destination = "/".join([target, filename2])
			file.save(destination)

		#Checks current folder and opens the correct location
		if os.getcwd() == APP_ROOT:
			os.chdir("uploaded")
		elif os.getcwd() == APP_ROOT+"\uploaded":
			pass
		elif os.getcwd() == APP_ROOT+"\sequence_ident":
			os.chdir("..\uploaded")

		#Checks to see if any file has been uploaded, if it has not then error returned
		if 'file' not in request.files:
			result_seq_multi = "No File uploaded! Please Upload a MzIdent or mzTab formatted file"
			return render_template("upload_peptide.html", result_family=result_seq_multi)

		# If the filetype is allowed, the file is read in and then regex match used to locate the peptide
		if filename2.rsplit('.', 1)[1].lower() in ALLOWED_EX_XML:
			file_mz_seq = open(filename2, "r")
			whole_file = file_mz_seq.read()

			regex = r">[a-zA-z]+"
			matches = re.finditer(regex, whole_file)
			for matchNum, match in enumerate(matches):
			    matchNum = matchNum + 1
			    list_of_matches.append(match.group())

			list_of_pep_seqs = [character.replace('>', '') for character in list_of_matches]

		# Checks to see filetype for MZTAB format
		elif filename2.rsplit('.', 1)[1].lower() in ALLOWED_EX_MZTAB:

			file_mztab_seq = open(filename2, "r")
			whole_file = file_mztab_seq.read()

			regex = r"[A-Z]+\S\B[A-Z]"
			matches = re.finditer(regex, whole_file)
			for matchNum, match in enumerate(matches):
			    matchNum = matchNum + 1
			    list_of_matches.append(match.group())
			list_of_words = ["UNIMOD", "PSM", "COM", "TRAQ", "MTD", "PRIDE"]
			mztab_seq_mixed = [word for word in list_of_matches if word not in list_of_words]
			list_of_pep_seqs = [sequence for sequence in mztab_seq_mixed if len(sequence) > 5]

		else:
			#If the file extension does not match mztab or mzident, an error stating wrong filetype uploaded relayed back
			result_seq_multi = "Incorrect filetype uploaded! Please Upload a MzIdent or mzTab formatted file"
			return render_template("upload_peptide.html", result_family=result_seq_multi)

		if len(list_of_pep_seqs) == 1:
			#If only 1 fasta sequence in file
			for seqs in list_of_pep_seqs:
				rows_count = cur.execute("SELECT Family, Sequence FROM prelim2 WHERE Sequence = %s", [seqs])
				cur.execute("SELECT Family, Sequence FROM prelim2 WHERE Sequence = %s", [seqs])
				result_seq =  cur.fetchall()
			if not cur.rowcount:
			  return render_template("upload_peptide.html", result_family=no_match)
			else:
				return render_template("upload_peptide.html", data=result_seq)#, result_seq1=result_seq[0][1])
		else:
			for seqs in list_of_pep_seqs:
				rows_count = cur.execute("SELECT Family, Sequence FROM prelim2 WHERE Sequence = %s", [seqs])
				cur.execute("SELECT Family, Sequence FROM prelim2 WHERE Sequence = %s", [seqs])
				result_seq =  cur.fetchall()
				if cur.rowcount > 0:
					result_seq_multi.append(result_seq)
			DF_PD=pd.DataFrame(result_seq_multi)
			result_seq_df=DF_PD.to_html()
			if result_seq_multi != "":
				#If data has been saved into memory, a hash check is conducted on the original file that was read in
				#If the unique hash check is not duplicate, the data is saved for the atlas expression
				#otherwise the data is not saved (due to it already existing from the same source file)
				hashed = str(hashlib.sha224(whole_file).hexdigest())

				with open("hash_checker.csv", "r+b") as f:
					reader = csv.reader(f)
					writer = csv.writer(f)
					for row in reader:
						rowlist2.append(row[0])
					if hashed not in rowlist2:
						rowlist.append(hashed)
						writer.writerow(rowlist)
						result_seq_multi2 = result_seq_multi
						with open("atlas_seqs.csv", "a") as csvfile:
							writer = csv.writer(csvfile)
							writer.writerow(result_seq_multi)

			return render_template("upload_peptide.html", data=result_seq_multi, empty = hashed)#result_seq_multi)
	else:
		return render_template("upload_peptide.html")


@app.route("/expression_atlas")
def atlas():
	try:
		atlas_seqs = result_seq_multi2
	except:
		pass
	return render_template("expression_atlas.html")

@app.route("/documentation")
def documentation():
	return render_template("documentation.html")

@app.route("/about_us")
def about_us():
	return render_template("about_us.html")

###############################################

@app.route("/profile/<name>")
def profile(name):
    return render_template("profile2.html", name=name)


@app.route('/user/<username>')
def show_user_profile(username):
	return render_template("style.html", username=username)
    # show the user profile for that user
    #return 'User %s' % username

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pass
    else:
        show_the_login_form()

@app.route("/visualise")
def visualise():
    return "lolnope"



#@app.route("/static")
#def static1():
#	url_for('static', filename='style.css')

@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

#if __name__ == "__main__":
#	app.run(debug=True)
