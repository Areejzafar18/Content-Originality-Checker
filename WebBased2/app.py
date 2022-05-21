from os.path import join, exists
from flask import Flask, render_template, request, jsonify, send_file
from work import PlagirismTest

app = Flask(__name__)

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/pagiarism', methods=["POST"])
def check_plagiarism():
  try:
    input_file = request.files.get('document')
    tester = PlagirismTest()
    unique_file_name = tester.add_file_to_temporary(input_file)
    response = tester.get_score(unique_file_name)
    tester.remove_file_from_temporary_folder(unique_file_name)
    return jsonify( {"status": True, "response": response } )
  except Exception as e:
    print(e)
  return jsonify({ "status": False })

@app.route('/document/<filename>')
def load_file(filename):
  filepath = join(PlagirismTest.all_files_path, filename)
  if exists(filepath):
    return send_file(filepath, conditional=True)
  return "404 - file not found"

if __name__=='__main__':
  app.run(debug=True)