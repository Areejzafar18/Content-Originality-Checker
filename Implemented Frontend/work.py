import os
import uuid
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')


class PlagirismTest:

  all_files_path = "TextFiles"
  temporary_folder_path = "TemporaryFolder"

  def __init__(self):
    self.score_mat={}

  def preprocess(self, query, f, doc):
    tokens_o=word_tokenize(query)
    tokens_p=word_tokenize(doc)
    tokens_o = [token.lower() for token in tokens_o]
    tokens_p = [token.lower() for token in tokens_p]
    stop_words=set(stopwords.words('english'))
    punctuations=['"','.','(',')',',','?',';',':',"''",'``']
    filtered_tokens_o = [w for w in tokens_o if not w in stop_words and not w in punctuations]
    filtered_tokens_p = [w for w in tokens_p if not w in stop_words and not w in punctuations]
    def lcs(l1,l2):
      s1=word_tokenize(l1)
      s2=word_tokenize(l2)
      dp = [[None]*(len(s1)+1) for i in range(len(s2)+1)]   
      for i in range(len(s2)+1): 
        for j in range(len(s1)+1): 
          if i == 0 or j == 0: 
            dp[i][j] = 0
          elif s2[i-1] == s1[j-1]: 
            dp[i][j] = dp[i-1][j-1]+1
          else: 
            dp[i][j] = max(dp[i-1][j] , dp[i][j-1]) 
      return dp[len(s2)][len(s1)] 

    sent_o=sent_tokenize(query)
    sent_p=sent_tokenize(doc)
    max_lcs=0
    sum_lcs=0

    for i in sent_p:
      for j in sent_o:
          l=lcs(i,j)
          max_lcs=max(max_lcs,l)
      sum_lcs+=max_lcs
      max_lcs=0

    score=sum_lcs/len(tokens_p)
    self.score_mat[f]=score
  
  def get_score(self, filename):
    with open(filename, "r", encoding='cp1252') as f:
        sequence_1 = f.read()
    sequence_1 = sequence_1.replace("\n","")
    query_doc = sequence_1.replace(" ","")  

    dict={}

    dir_list = os.listdir(self.all_files_path)

    for f in dir_list:
      with open(self.all_files_path+"/"+f, "r", encoding='cp1252') as file:
        data = file.read()
      data = data.replace("\n","")
      data = data.replace(" ","")    
      dict[f]=data

    for key in dict:
      self.preprocess(query_doc, key, dict[key])

    return self.sorted_perc()

  def sorted_perc(self):
    to_send = {}
    for key in self.score_mat:
      val = int(self.score_mat[key]*100)
      if val in to_send:
        to_send[val].append(key)
      else:
        to_send[val] = [key]
    return to_send

  def add_file_to_temporary(self, file):
    ext = file.filename.split('.')[-1]
    uname = str(uuid.uuid4())
    filename = os.path.join(self.temporary_folder_path, f'{uname}.{ext}')
    file.save( filename )
    return filename
  
  def remove_file_from_temporary_folder(self, filename):
    try:
      os.remove(filename)
      return True
    except:
      return False