class ReadaBERT:
  def __init__(self, lang='en'):
    """
    self (object): load the pre-trained model
    """
    if lang == 'en':
      self.tokenizer = AutoTokenizer.from_pretrained('tareknaous/readabert-en')
      self.model = AutoModelForSequenceClassification.from_pretrained('tareknaous/readabert-en')
    elif lang == 'ar':
      self.tokenizer = AutoTokenizer.from_pretrained('tareknaous/readabert-ar')
      self.model = AutoModelForSequenceClassification.from_pretrained('tareknaous/readabert-ar')
    elif lang == 'fr':
      self.tokenizer = AutoTokenizer.from_pretrained('tareknaous/readabert-fr')
      self.model = AutoModelForSequenceClassification.from_pretrained('tareknaous/readabert-fr')
    elif lang == 'ru':
      self.tokenizer = AutoTokenizer.from_pretrained('tareknaous/readabert-ru')
      self.model = AutoModelForSequenceClassification.from_pretrained('tareknaous/readabert-ru')
    elif lang == 'hi':
      self.tokenizer = AutoTokenizer.from_pretrained('tareknaous/readabert-hi')
      self.model = AutoModelForSequenceClassification.from_pretrained('tareknaous/readabert-hi')
    else:
      self.tokenizer = AutoTokenizer.from_pretrained('tareknaous/readabert-en')
      self.model = AutoModelForSequenceClassification.from_pretrained('tareknaous/readabert-en')
      print('Sorry! we currently do not cover this language.')
      print('Don\'t worry though, we\'ve got you covered! Our English model can transfer well to other languages so we\'ve loaded it for you.')
      print('\n')

    #Check if gpu is on
    if torch.cuda.is_available() == False:
      print('We recommend turning on the GPU for faster prediction!')


  def predict(self, text):
    """Run inference using the loaded model and return readability prediction

    Args:
      text (string): input sentence 

    Returns:
      result (int): predicted readability level (1 to 6) based on the CEFR scale

    """
    inputs = tokenizer(text, padding=True, truncation=True, max_length=512, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    prediction = torch.argmax(outputs.logits, dim=1)
    result = prediction.item() +1 #Add one to map to 1-6 cefr scale

    return result